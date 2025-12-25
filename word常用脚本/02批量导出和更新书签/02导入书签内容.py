from win32com import client
import pandas as pd
import os

# 读取修改后的Excel文件
excel_path = r"D:\书签填写后.xlsx"
if not os.path.exists(excel_path):
    print(f"错误：找不到Excel文件 {excel_path}")
    exit(1)

df = pd.read_excel(excel_path)
print(f"已读取Excel文件，包含{len(df)}个书签")

# 创建Word应用
app = client.Dispatch('Word.Application')
app.Visible = False

# 打开文档
doc_path = r"D:\正文.docx"
word = app.Documents.Open(doc_path)

# 计数器
updated_count = 0
error_count = 0

# 遍历Excel中的书签数据，更新到Word中
for index, row in df.iterrows():
    bookmark_name = row["书签名称"]
    bookmark_content = row["书签内容"]

    try:
        # 检查书签是否存在
        if word.Bookmarks.Exists(bookmark_name):
            # 保存书签的范围
            bookmark_range = word.Bookmarks(bookmark_name).Range
            # 更新内容
            bookmark_range.Text = bookmark_content
            # 重新添加书签(因为更新内容后书签可能会丢失)
            word.Bookmarks.Add(bookmark_name, bookmark_range)
            updated_count += 1
            print(f"已更新书签: {bookmark_name}")
        else:
            print(f"警告：书签不存在: {bookmark_name}")
            error_count += 1
    except Exception as e:
        print(f"更新书签 {bookmark_name} 时出错: {str(e)}")
        error_count += 1

# 保存Word文档
word.Save()

# 关闭Word
word.Close(SaveChanges=True)
app.Quit()

print(f"完成！成功更新了{updated_count}个书签，{error_count}个书签更新失败")
