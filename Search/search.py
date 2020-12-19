from Pdf.util import get_PDFs


def search(root_path, keyword):
    """
    搜索root_path下pdf文件
    :param root_path:
    :param keyword:
    :return:
    """
    # keyword = input("input keyword:")

    #  文件夹下PDF对象list
    PDFs = get_PDFs(root_path)
    #  预览读取结果
    for i in PDFs:
        print(i.path)
        print(i.text)

    #  search


if __name__ == '__main__':
    root = '..\\resource'
    search(root, None)
