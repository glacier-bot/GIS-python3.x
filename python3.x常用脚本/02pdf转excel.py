import os

#尝试导入pdfplumber库，如果没有安装则自动安装
try:
    import pdfplumber
except:
    os.system('pip install pdfplumber')
    import pdfplumber

#尝试导入xlwt库，如果没有安装则自动安装
try:
    import xlwt
except:
    os.system('pip install xlwt')
    import xlwt

def pdf_to_excel(pdf_path,save_path):
    # 定义保存Excel的位置
    workbook = xlwt.Workbook()  #定义workbook
    sheet = workbook.add_sheet('Sheet1')  #添加sheet
    i = 0 # Excel起始位置

    print('\n')
    print('开始读取数据')
    print('\n')

    # 读取PDF文件
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 获取当前页面的全部文本信息，包括表格中的文字
            for table in page.extract_tables():
                # print(table)
                for row in table:            
                    # print(row)
                    for j in range(len(row)):
                        sheet.write(i, j, row[j])
                    i += 1
                # print('---------- 分割线 ----------')

    # 保存Excel表
    workbook.save(save_path)
    print('\n')
    print('写入excel成功')
    print('保存位置：')
    print(save_path)
    print('\n')
    print('PDF转换完毕')

if __name__ == '__main__':
    pdf_path=r"D:\全域矢量数据.pdf"
    save_path=r"D:\全域矢量数据.xls"
    pdf_to_excel(pdf_path,save_path)