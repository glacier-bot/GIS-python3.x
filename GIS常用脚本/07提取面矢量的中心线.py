import arcpy


print("开始")
arcpy.topographic.PolygonToCenterline(
    in_features=r"D:\生态廊道建设_Clip补面",
    out_feature_class=r"D:\生态廊道建设_Clip补面线"
)

print("\n结束")