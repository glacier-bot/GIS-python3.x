# coding=utf-8
# def change(x):
#     return x.split(u"镇")[0][4:]+u"镇"

import os
import arcpy
print(u"开始执行")


def select_uniq(x):
    return list(set(x))


path = r"D:\测试.mdb"

feature_class = [u"图层1"]

# 要排除的镇名
ex_name = []

arcpy.env.workspace = path

for s_feature in feature_class:
    print(u"开始导出：", s_feature)
    names = []
    with arcpy.da.SearchCursor(s_feature, [u'镇名']) as cursor:
        for row in cursor:
            if row[0] not in ex_name:
                names.append(row[0])

    print(u"筛选镇名")
    uniq_names = select_uniq(names)
    for name in uniq_names:
        dest_path = u"D:/成果/{0}/{1}".format(
            s_feature, name)
        os.mkdir(dest_path)

print("Finished")
