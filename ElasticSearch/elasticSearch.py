from elasticsearch import Elasticsearch as Es
from datetime import datetime
from elasticsearch import helpers

import json


class ElasticSearch:
    def __init__(self):
        # self.__host = host
        # self.__port = port
        self.es = Es()

    def create(self, indexName):
        self.es.indices.create(index=indexName, ignore=400)

    def delete(self, indexName):
        self.es.indices.delete(index=indexName, ignore=400)

    def upload(self, indexName, pdf):
        self.es.index(index=indexName, body={"path": pdf.path, "content": pdf.text, "timestamp": datetime.now()})

    def bulk(self, indexName, PDFs):
        actions = []
        for i in PDFs:
            actions.append({
                "_index": indexName,
                "_source": {"path": i.path, "content": i.text, "timestamp": datetime.now()}
            })
        helpers.bulk(self.es, actions)

    def search(self, indexName, keyword):
        body = json.dumps(
            {
                "query": {
                    "fuzzy": {
                        "content": keyword
                    }
                },
                "highlight": {
                    "fields": {
                        "content": {}
                    }
                }
            }
        )

        return self.es.search(body=body,
                              index=indexName,
                              filter_path=['hits.total', 'hits.hits._score',
                                           'hits.hits._source.path', 'hits.hits.highlight'])
