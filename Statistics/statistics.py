from Pdf.util import get_PDFs

from nltk.corpus import stopwords
import nltk


try:
    sw = set(stopwords.words("english"))
except LookupError:
    print('未下载停用词，downloading')
    nltk.download('stopwords')
    sw = set(stopwords.words("english"))
except Exception as e:
    raise e


def statistics(path):
    PDFs = get_PDFs(path)

    # 聚合成一个text
    text = ' '.join(x.text for x in PDFs)
    # 去停用词
    text = [word for word in text.lower().split() if word not in sw]
    # 提取词干
    text = map(lambda x: nltk.PorterStemmer().stem(x), text)
    # 统计词频
    result = nltk.FreqDist(text).most_common(100)
    for k, v in result:
        print("%s %d" % (k, v))


root = '..\\resource'
statistics(root)
