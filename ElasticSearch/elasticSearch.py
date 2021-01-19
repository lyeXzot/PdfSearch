from elasticsearch import Elasticsearch as Es
from datetime import datetime
from Pdf.pdf import PDF


class ElasticSearch:
    def __init__(self):
        # self.__host = host
        # self.__port = port
        self.es = Es()

    def create(self, indexName):
        self.es.indices.create(index=indexName, ignore=400)

    def add(self, indexName, pdf):
        if not isinstance(pdf, PDF):
            raise TypeError("参数错误")
        self.es.index(index=indexName, body={"path": pdf.path, "content": pdf.text, "timestamp": datetime.now()})

    def search(self, indexName):
        return self.es.search(index=indexName)


ins_es = ElasticSearch()
Name = "temp-index"
# ins_es.create(Name)
# for i in range(10):
#     ins_es.add(Name, PDF("path"+str(i), "context"+str(i)))
print(ins_es.search(Name))
# print(ins_es.es.search(index=Name, filter_path=['hits.hits._*']))
