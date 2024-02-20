import arcpy

print("开始")
# arcpy.env.workspace = r"D:\基础数据0614.gdb"
arcpy.env.workspace=r"D:\冲突合并.gdb"


def unique_values(table, field):
    with arcpy.da.SearchCursor(table, field) as cursor:
        return sorted({row[0] for row in cursor})


#=============================需要修改的参数===========================
feature = "冲突合并2"     #"道路编号新0704"
numbers = unique_values(feature, "融合字段")     #"编号0704"
fields = ["与蓝线","与红线","与建设用地","与202","与开发边界"]     #["长度", "宽度", "是否连接主要公路", "是否连接桥梁", "路面结构"]
#=====================================================================

for num in numbers:
    print("合并编号={}属性".format(num))
    #=============================需要修改的参数=======================
    type_of_fields = ["", "", "", "", ""]     #[0, 0, "", "", ""]
    statement = "融合字段='{}'".format(num)     #"编号0704={}".format(num)
    #=================================================================
    results = []
    with arcpy.da.UpdateCursor(feature, fields,
                               where_clause=statement) as cursor:
        for row in cursor:
            results.append(row)
    for i in range(len(fields)):
        #=============================针对特定字段的处理方式=======================
        # if i == 1:
        #     for j in range(len(results)):
        #         type_of_fields[i] += results[j][i]
        #     type_of_fields[i] = round(type_of_fields[i] / len(results), 0)
        #     continue
        #=============================末尾的continue不能删========================
        for j in range(len(results)):
            if isinstance(type_of_fields[i], str) and len(results) > 1:
                type_of_fields[i] += (results[j][i] + "、")
            else:
                type_of_fields[i] += results[j][i]
        if isinstance(type_of_fields[i], str) and len(results) > 1:
            _ = {k for k in type_of_fields[i].split("、") if k != ""}
            type_of_fields[i] = "、".join(list(_))
            type_of_fields[i] = type_of_fields[i].strip("、")
    with arcpy.da.UpdateCursor(feature, fields,
                               where_clause=statement) as cursor:
        for row in cursor:
            row = type_of_fields
            cursor.updateRow(row)

print("融合要素")
arcpy.management.Dissolve(in_features=feature,
                          out_feature_class=feature + "_Dissolved",
                          #=============================需要修改的参数===========================
                          dissolve_field= ["融合字段"]+fields     #["编号0704"] + fields
                          )
                          #=====================================================================
print("结束")