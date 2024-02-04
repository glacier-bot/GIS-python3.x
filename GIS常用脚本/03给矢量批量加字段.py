import arcpy

arcpy.env.workspace =r"D:\Users\GJSJY\My Document\0--范德强--0\20230103廊下试点入库\加字段后廊下土整试点.gdb"

print("开始")
database="CZGHTB"
fields=[
    ["BSM","TEXT","标识码",18],
    ["XZQDM","TEXT","行政区代码",9],
    ["XZQMC","TEXT","行政区名称",100],
    ["ZLDWDM","TEXT","坐落单位代码",19],
    ["ZLDWMC","TEXT","坐落单位名称",255],
    ["GHDLBM","TEXT","规划地类编码",5],
    ["GHDLMC","TEXT","规划地类名称",60],
    ["GHDLMJ","FLOAT","规划地类面积",15],
    ["BZ","TEXT","备注",2147483647]
]
arcpy.management.AddFields(database,fields)

# databases=["SDQYZZHDLTB","YJJBNTTZTB","ZZQY"]
# fields=[
#     [
#         ["GDPDJB","TEXT","耕地坡度级别",2],
#         ["XZGDLYDLBM","TEXT","新增耕地来源地类编码",5],
#         ["XZGDLYDLMC","TEXT","新增耕地来源地类名称",18],
#         ["XZGDMJ","FLOAT","新增耕地面积",15],
#         ["XZGDDB","SHORT","新增耕地等别",2],
#         ["XZGDLYXM","TEXT","新增耕地来源项目",100],
#         ["FRDBS","TEXT","飞入地标识",1],
#         ["CZCSXM","TEXT","城镇村属性码",4],
#         ["SJNF","SHORT","数据年份",4],
#         ["BZ","TEXT","备注",2147483647]
#     ],
#     [
#         ["BSM","TEXT","标识码",18],
#         ["TZYNDKBH","TEXT","调整永久基本农田地块编号",10],
#         ["TZLX","TEXT","调整类型",5],
#         ["SJCZMC","TEXT","涉及村庄名称",100],
#         ["TZQDLBM","TEXT","调整前地类编码",5],
#         ["TZQDLMC","TEXT","调整前地类名称",60],
#         ["TZHDLBM","TEXT","调整后地类编码",5],
#         ["TZHDLMC","TEXT","调整后地类名称",60],
#         ["TZYNDKMJ","FLOAT","调整永久基本农田地块面积",15],
#         ["BZ","TEXT","备注",2147483647]
#     ],
#     [
#         ["BSM","TEXT","标识码",18],
#         ["XZQDM","TEXT","行政区代码",9],
#         ["XZQMC","TEXT","行政区名称",100],
#         ["SDBH","TEXT","试点编号",12],
#         ["SDMC","TEXT","试点名称",100],
#         ["ZZQYBH","TEXT","整治区域编号",15],
#         ["ZZQYMJ","FLOAT","整治区域面积",15],
#         ["SJCZMC","TEXT","涉及村庄名称",80],
#         ["SJDCZLX","TEXT","涉及的村庄类型",15],
#         ["BZ","TEXT","备注",2147483647]
#     ]
# ]
# for database,field in zip(databases,fields):
#     print("正在添加：",database)
#     arcpy.management.AddFields(database,field)

print("添加完毕")
