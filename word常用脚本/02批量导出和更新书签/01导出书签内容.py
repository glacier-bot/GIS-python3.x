from win32com import client
import pandas as pd

app = client.Dispatch('Word.Application')
app.Visible = False

word = app.Documents.Open(
    r"D:\正文.docx")

bookmarks = word.Bookmarks

# 创建列表存储书签数据
bookmark_data = []

# 遍历所有书签
for i in range(1, bookmarks.Count + 1):
    print(f"正在导出第 {i} 个书签")
    bookmark = bookmarks(i)
    name = bookmark.Name
    content = bookmark.Range.Text
    bookmark_data.append({"书签名称": name, "书签内容": content})

# 创建DataFrame
df = pd.DataFrame(bookmark_data)

# 保存为Excel文件
excel_path = r"D:\书签导出.xlsx"
df.to_excel(excel_path, index=False)

print(f"成功导出 {bookmarks.Count} 个书签到 {excel_path}")

word.Save()

# 退出当前word
word.Close(SaveChanges=True)
app.Quit()
