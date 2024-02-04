import os
import pandas as pd
import math
import arcpy
class P:
    printable=""
try:
    import xlwt
except:
    print("缺少xlwt，正在安装...")
    os.system("pip install xlwt --user")
    import xlwt
try:
    import exifread
except:
    print("缺少exifread，正在安装...")
    os.system("pip install exifread --user")
    import exifread

def extract_photo(pth):
    with open(pth,'rb') as photo_img:
        tags=exifread.process_file(photo_img)
    try:
        #高度
        Altitude=tags["GPS GPSAltitude"].printable
        #纬度
        LatRef=tags["GPS GPSLatitudeRef"].printable
        Lat=tags["GPS GPSLatitude"].printable[1:-1].replace(" ","").replace("/",",").split(",")
        if len(Lat)==3:
            Lat.append("1.0")
        Lat=float(Lat[0])+float(Lat[1])/60+float(Lat[2])/float(Lat[3])/3600
        if LatRef != "N":
            Lat=Lat*(-1)
        #经度
        LonRef=tags["GPS GPSLongitudeRef"].printable
        Lon=tags["GPS GPSLongitude"].printable[1:-1].replace(" ","").replace("/",",").split(",")
        if len(Lon)==3:
            Lon.append("1.0")
        Lon=float(Lon[0])+float(Lon[1])/60+float(Lon[2])/float(Lon[3])/3600
        if LonRef!="E":
            Lon=Lon*(-1)
        return round(Lat,5),round(Lon,5),round(eval(Altitude),5)
    except:
        print("文件 ",os.path.basename(pth)," 没有坐标信息，已跳过")
        return []
        # return os.path.basename(pth)
    
def find_orentation(pth):
    with open(pth,'rb') as img:
            tags=exifread.process_file(img)
    try:
        date=tags['EXIF DateTimeOriginal']
    except:
        try:
            date=tags["GPS GPSDate"]
        except:
            p=P()
            date=p
    try:
        meta_direction=tags["GPS GPSImgDirection"].printable.split("/")
        direction=int(meta_direction[0])/int(meta_direction[1])
        def get_Sin(x):
            return math.cos(math.radians(int(direction)))
        def get_Cos(x):
            return math.sin(math.radians(int(direction)))
        if get_Sin(direction)>0 and get_Cos(direction)>0:
            return "东北",date.printable
        elif get_Sin(direction)>0 and get_Cos(direction)<0:
            return "西北",date.printable
        elif get_Sin(direction)<0 and get_Cos(direction)>0:
            return "东南",date.printable
        elif get_Sin(direction)<0 and get_Cos(direction)<0:
            return "西南",date.printable
        elif get_Sin(direction)==1 and get_Cos(direction)==0:
            return "正北",date.printable
        elif get_Sin(direction)==0 and get_Cos(direction)==1:
            return "正东",date.printable
        elif get_Sin(direction)==-1 and get_Cos(direction)==0:
            return "正南",date.printable
        elif get_Sin(direction)==0 and get_Cos(direction)==-1:
            return "正西",date.printable
    except:
        print("{}没有朝向信息，已跳过".format(os.path.basename(pth)))
        return date.printable

def extract_exif(heic_path,jpeg_path,excel_path):
    if heic_path is None:
        heic_path=jpeg_path
    heics=os.listdir(heic_path)
    infos=[]
    for heic in heics:
        heic_pth=os.path.join(heic_path,heic)
        info=extract_photo(heic_pth)
        oren=find_orentation(heic_pth)
        info=list(info)+list(oren)
        # print((info))
        if info is not None:
            infos.append(info)
    workbook=xlwt.Workbook()
    sheet=workbook.add_sheet("Sheet1")
    head=["Lat","Lon","Altitude","Orentation","Date"]
    for id,ele in enumerate(head):
        sheet.write(0,id,ele)
    start=1
    for info in infos:
        for id,ele in enumerate(info):
            sheet.write(start,id,ele)
        start+=1
    workbook.save(excel_path)

def excel_to_point(excel_path,point_name):
    arcpy.conversion.ExcelToTable(
        Input_Excel_File=excel_path,
        Output_Table=point_name+"表"
    )
    arcpy.MakeXYEventLayer_management(
        table=point_name+"表",
        in_x_field="Lon",
        in_y_field="Lat",
        out_layer="坐标点图层",
        spatial_reference=r"China Geodetic Coordinate System 2000.prj",
        # spatial_reference=r"Beijing 1954.prj",
        in_z_field="Altitude"
    )
    arcpy.FeatureToPoint_management(
        in_features="坐标点图层",
        out_feature_class=point_name
    )

def point_link_photo(point_name,jpeg_path):
    arcpy.management.AddFields(point_name,[["imgpth","TEXT","",500,"",""],["imgtemp","TEXT","",500,"",""]])
    data=pd.read_excel(excel_path)
    ls_oren=data["Orentation"].tolist()
    imgs=os.listdir(jpeg_path)
    ls_pth=[]
    for img in imgs:
        img_path=os.path.join(jpeg_path,img)
        ls_pth.append(img_path)
    with arcpy.da.UpdateCursor(point_name,["OBJECTID","imgpth","imgtemp"]) as cursor:
        for row in cursor:
            # print(row)
            row[1]=ls_pth[row[0]-1]
            row[2]='<img src="'+ls_pth[row[0]-1]+'" width='+"'350'"+' height=350/>'
            cursor.updateRow(row)



def main(overwrite,heic_path,jpeg_path,db_path,excel_path,point_name):
    print("开始提取文件坐标")
    extract_exif(heic_path,jpeg_path,excel_path)
    print("设置arcgis工作路径为：",db_path)
    arcpy.env.workspace=db_path
    if overwrite==True:
        print("arcgis重名覆盖已开启，不改变坐标点的名称会覆盖已有点要素数据")
    else:
        print("arcgis重名覆盖已关闭，不改变坐标点的名称可能会报错")
    print("开始将坐标转为点要素")
    excel_to_point(excel_path,point_name)
    print("连接点要素文件路径")
    point_link_photo(point_name,jpeg_path)
    print("操作完成")
    print("已将点要素输出至：",db_path+r"\\"+point_name)
    print("已将点坐标输出至：",excel_path)
    print("**重复运行但不改变点坐标的excel文件名会覆盖之前的excel文件**")

if __name__=='__main__':
    #是否开启arcgis的重名覆盖，默认关闭（False），若要开启请改为True
    overwrite=True
    #照片所在文件夹
    ##iOS系统heic文件所在文件夹，如果是安卓系统，设置为None
    # heic_path=r"D:\Users\GJSJY\My Document\0--范德强--0\20220815安亭项目\范现状调研\heic0923"
    # heic_path=r"D:\Users\GJSJY\My Document\0--范德强--0\20230109安亭调研\安亭调研0109原图\iCloud 照片"
    heic_path = None
    ##iOS系统和安卓系统jpeg文件所在文件夹，安卓系统不能用微信导出，只能用数据线复制粘贴
    # jpeg_path=r"Y:\07、金山区吕巷镇土整\现状调研\8.2324调研--李\村庄"
    # jpeg_path=r"D:\Users\GJSJY\My Document\0--范德强--0\20220815安亭项目\范现状调研\jpeg0923"
    # jpeg_path=r"D:\Users\GJSJY\My Document\0--范德强--0\20230109安亭调研\安亭调研0109压缩\iCloud 照片"
    jpeg_path=r"Y:\08、嘉定华亭全域土整\现状调研照片"
    #保存点要素的数据库
    # db_path=r"D:\Users\GJSJY\My Document\0--范德强--0\实用工具\处理照片坐标\测试用数据库.gdb"
    # db_path=r"D:\Users\GJSJY\My Document\0--范德强--0\20220815安亭项目\调研图片转点.gdb"
    db_path=r"Y:\08、嘉定华亭全域土整\现状调研照片点位集合.gdb"
    #点坐标的保存路径，默认是在当前文件夹
    excel_path=r"Y:\08、嘉定华亭全域土整\调研坐标点带朝向.xls"
    #点要素的名称
    point_name="调研坐标点带朝向"

    main(overwrite,heic_path,jpeg_path,db_path,excel_path,point_name)