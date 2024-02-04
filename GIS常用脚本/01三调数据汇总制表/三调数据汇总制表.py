import os
try:
    import pandas as pd
except:
    print("缺少pandas库，正在安装...")
    os.system("pip install pandas --user")
    print("安装完成")
    import pandas as pd
def change(x,data):
    try:
        # return round(data[x]*0.0001,2)  #平方米换算成公顷，保留2位小数
        # x="0"*4-len(x)+str(x)
        # print(x)
        if len(x)==3:
            x="0"+x
            print(x)
        if "A" in x:
            if len(x)-1<=3:
                   x="0"+x         
        return data[x]
    except:
        # print("地类信息不全，请在总表中增加{}地类".format(x))
        # print(type(x))
        pass
def main(input_path,output_path,field):
    data=pd.read_csv(input_path)
    area=list(data)[-1]
    table=pd.read_excel("土地利用现状总表.xlsx",dtype="str")
    data=data[[field,area]].groupby(field).sum()
    data=data.set_index(data.index)[area].to_dict()
    data={str(k):v for k,v in data.items()}
    # print(data["101"])
    # table["面积"]=table["类型编码"].apply(lambda x:change(x,data))
    table["面积"]=table["补全编码"].apply(lambda x:change(x,data))
    print(table)
    sum_area=table[["三大类","面积"]].groupby("三大类").sum()
    sum_area=sum_area.drop(labels=["小计","总计"],axis=0)
    table.iloc[26,4]=sum_area.loc["农用地","面积"]
    table.iloc[51,4]=sum_area.loc["建设用地","面积"]
    table.iloc[63,4]=sum_area.loc["未利用地","面积"]
    table.iloc[64,4]=sum_area.sum()[0]
    table=table.dropna()
    table.replace("！","",inplace=True)
    try:
        del table["补全编码"]
    except:
        pass
    table.to_excel(output_path,index=None)
if __name__=="__main__":
    print("开始")
    #输入属性表
    # input_path=r"D:\Users\GJSJY\My Document\0--范德强--0\20220815金山吕巷\图表导出\吕巷三调交减量化地块1518.txt"
    input_path=r"D:\Users\GJSJY\Desktop\20240108城中村补划\图表导出\NG_SI_LAND_USE_Clip整理区范围.txt"
    # input_path=r"D:\Users\GJSJY\My Document\0--范德强--0\20221014安亭土地整治规划各版本文件\图表导出\统计用\城市开发边界外三调.txt"
    #输入输出位置和名称
    output_path=r"D:\Users\GJSJY\Desktop\20240108城中村补划\图表导出\NG_SI_LAND_USE_Clip整理区范围.xlsx"
    #输入三调字段名称
    field="LAND_USE_GB"

    main(input_path,output_path,field)
    print("完成")