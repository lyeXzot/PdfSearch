import os
from Pdf.pdf import PDF
from pdfminer.high_level import extract_text


def get_all_PdfPath(root):
    """
    获取root文件下所有pdf文件目录
    :param root: 查找根目录
    :return: 所有pdf文件路径的list
    """
    result = []
    for i in os.listdir(root):
        path = os.path.join(root, i)
        if os.path.isdir(path):                             # 目录，递归获取
            result.extend(get_all_PdfPath(path))
        elif os.path.isfile(path) and path[-3:] == 'pdf':   # 为pdf文件
            result.append(path)
    return result


def get_PDFs(root):
    """
    获取root目录下所有pdf文件文本内容，转化为PDF对象list
    :param root:
    :return: PDF对象list
    """
    PDFs = []
    for pdf_path in get_all_PdfPath(root):
        # 读取pdf文件内容,生成PDF对象
        PDFs.append(PDF(extract_text(pdf_path), pdf_path))
    return PDFs
