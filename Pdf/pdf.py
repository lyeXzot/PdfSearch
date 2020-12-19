from ElasticSearch import connect


class PDF:
    def __init__(self, content, path):
        self.text = content
        self.path = path

    def upload(self):
        """
        上传内容到ES服务器
        :return:
        """
        # connect.add()
        pass
