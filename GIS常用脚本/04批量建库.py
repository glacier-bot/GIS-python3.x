feature_fields={
    #耕地保护目标
    "GDBHMB":[
        ["BSM","TEXT","标识码",18],
        ["TBMJ","FLOAT","图斑面积",15],
        ["GDDB","SHORT","耕地等别",2]
    ],
    #近期重大项目(点)
    "JQZDXMD":[
        ["BSM","TEXT","标识码",18]
    ],
    #近期重大项目(线)
    "JQZDXMX":[
        ["BSM","TEXT","标识码",18]
    ],
    #近期重大项目(面)
    "JQZDXMM":[
        ["BSM","TEXT","标识码",18]
    ]
}

feature_title={
    "GDBHMB":"耕地保护目标",
    "JQZDXMD":"近期重大项目(点)",
    "JQZDXMX":"近期重大项目(线)",
    "JQZDXMM":"近期重大项目(面)"
}

print("初始化完成")

import arcpy

def cmain(k,v,feature_fields,out_path):
    print("新建要素类：",k)
    arcpy.management.CreateFeatureclass(
        out_path=out_path,
        out_name=k,
        geometry_type=geometry_type,
        has_m="DISABLED",
        has_z="DISABLED",
        spatial_reference=arcpy.Describe(
            r"D:\identity.gdb\DLTB"
        ).spatialReference
    )
    print("设置别名：",v)
    arcpy.AlterAliasName(k,v)
    print("写入字段")
    arcpy.management.AddFields(k,feature_fields[k])

print("设置输出路径")
#arcpy.env.workspace = r"D:\空库.gdb"
out_path=r"D:\空库.gdb"

print("开始建库")
for k,v in feature_title.items():
    if "(点)" in v[-3:]:
        print("新建点")
        geometry_type="POINT"
        cmain(k,v,feature_fields,out_path)
    elif "(线)" in v[-3:]:
        print("新建线")
        geometry_type="POLYLINE"
        cmain(k,v,feature_fields,out_path)
    else:
        print("新建面")
        geometry_type="POLYGON"
        cmain(k,v,feature_fields,out_path)

print("完成")