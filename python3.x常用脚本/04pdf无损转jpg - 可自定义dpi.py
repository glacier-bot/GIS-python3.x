try:
    import fitz  # PyMuPDF
except ImportError:
    import os
    os.system('pip install PyMuPDF')
    import fitz  # PyMuPDF
from os.path import join
from os import listdir


def pdf2jpg(pdf_path, jpg_path, dpi):
    pdf_document = fitz.open(pdf_path)
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        pix = page.get_pixmap(dpi=dpi)
        pix.save(jpg_path)


if __name__ == '__main__':
    root = r"D:\新建文件夹 (2)"
    dpi = 150

    print('开始')
    for pdf in listdir(root):
        if pdf.endswith('.pdf'):
            pdf2jpg(join(root, pdf), join(root, pdf.split('.')[0]+'.jpg'), dpi)
        else:
            print('文件格式错误，请检查文件格式')
            break
    ## 单个文件转换测试
    # print('开始')
    # pdf2jpg(join(root, '测试.pdf'),
    #         join(root, '测试.jpg'), dpi)