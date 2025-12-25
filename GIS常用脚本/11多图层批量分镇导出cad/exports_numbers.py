# coding=utf-8
# def change(x):
#     return x.split(u"镇")[0][4:]+u"镇"

import arcpy
print(u"开始执行")


def select_uniq(x):
    return list(set(x))


path = r"D:\测试.gdb"

feature_class = [u"图层1"]

# 过滤掉的镇名
ex_name = []

arcpy.env.workspace = path

for s_feature in feature_class:
    print(u"开始导出：{0}".format(s_feature))
    names = []
    with arcpy.da.SearchCursor(s_feature, [u'镇名']) as cursor:
        for row in cursor:
            if row[0] not in ex_name:
                names.append(row[0])

    print(u"筛选镇名")
    uniq_names = select_uniq(names)
    # print(len(uniq_names))
    print(u"制作图层")
    lyr_name = u'selected_lyr_{}'.format(s_feature)
    arcpy.MakeFeatureLayer_management(s_feature, lyr_name)
    print(u"开始导出")
    for name in uniq_names:
        sql_query = u"镇名='{}'".format(name)
        # print(sql_query)
        arcpy.SelectLayerByAttribute_management(
            lyr_name, "NEW_SELECTION", sql_query)
        dest_path = u"D:/成果/序号cad/{0}.dwg".format(
            name)
        print(u"导出：", name)
        arcpy.ExportCAD_conversion(lyr_name, "DWG_R2000", dest_path)
