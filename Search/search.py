from Pdf.util import get_PDFs
from ElasticSearch.elasticSearch import ElasticSearch

import time


def search(root_path, keyword, search_type):
    """
    搜索root_path下pdf文件
    :param search_type:
    :param root_path:
    :param keyword:
    :return:
    """
    #  文件夹下PDF对象list
    PDFs = get_PDFs(root_path)

    #  预览读取结果
    # for i in PDFs:
    #     print(i.path)
    #     print(i.text)

    es = ElasticSearch()
    Name = "temp-index"
    es.create(Name)
    es.bulk(Name, PDFs)
    time.sleep(1)
    result = es.search(Name, keyword, search_type)
    es.delete(Name)
    return result


if __name__ == '__main__':
    root = '..\\resource'
    print(search(root, "cluster", "term"))
    print(search(root, "Cluster", "match"))
    print(search(root, "cluste*", "wildcard"))
