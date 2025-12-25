# coding=utf-8
# def change(x):
#     return x.split(u"镇")[0][4:]+u"镇"

import arcpy
import os
from safeprint import safe_print
safe_print(u"开始执行")


def select_uniq(x):
    return list(set(x))


path = r"D:\测试.mdb"

feature_class = [u"图层1"]

# 要排除的镇名
ex_name = []

arcpy.env.workspace = path

for s_feature in feature_class:
    safe_print(u"开始导出：{}".format(s_feature))
    names = []
    with arcpy.da.SearchCursor(s_feature, [u'镇名']) as cursor:
        for row in cursor:
            if row[0] not in ex_name:
                names.append(row[0])

    safe_print(u"筛选镇名")
    uniq_names = select_uniq(names)
    safe_print(u"制作图层")
    lyr_name = u'selected_lyr_{}'.format(s_feature)
    arcpy.MakeFeatureLayer_management(s_feature, lyr_name)
    safe_print(u"开始导出")
    for name in uniq_names:
        safe_print(u"导出镇名：{}".format(name))
        sql_query = u"[镇名]='{}'".format(name)
        arcpy.SelectLayerByAttribute_management(
            lyr_name, "NEW_SELECTION", sql_query)
        dest_path = u"D:/成果/{0}/{1}/导出_{2}.mdb".format(
            s_feature, name, name )
        arcpy.CreatePersonalGDB_management(os.path.dirname(dest_path), os.path.basename(dest_path))
        arcpy.env.workspace = dest_path
        arcpy.CopyFeatures_management(lyr_name, u"{1}_{0}".format(name, s_feature))

safe_print(u"Finished")
