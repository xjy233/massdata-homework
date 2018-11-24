import time
from gensim import corpora, models, similarities

"""
函数说明：文件预处理
输入：要打开的文件名
输出：
documents - 处理过后的词空间列表
"""
def load_data(filename ='199801_clear.txt'):
    # 文档分词列表
    documents = []
    #文档分词
    doc = []
    # 打开语料库文件，逐行读取语料，将同一篇文章的不同章节合并，并过滤掉无意义的词和符号
    fr_open = open(filename, 'r', encoding='GBK')

    for line in fr_open:
        if line.strip():   # 跳过空行,这里strip（）无参数是去掉首尾空格
            words = line.split()
            # 过滤掉无意义的词和符号
            for i in range(len(words)):
                word = words[i]
                if 'w' not in word and 'y' not in word and 'u' not in word \
                        and 'c' not in word and 'm' not in word:    doc.append(word)
        else: #出现空行，即将开始下一篇文档读入，所以把上一篇文档添加进documents，并将doc置为初始
            documents.append(doc)
            doc = []
    #将统计数大于一的词加入词袋
    fre = {}
    for doc in documents:
        for word in doc:
            if word in fre:
                fre[word] += 1
            else:
                fre[word] = 1
    documents = [[word for word in doc if fre[word] > 1] for doc in documents]

    return documents


"""
函数说明：统计并计算tf_idf权重值
输入：documents - 处理过后的词空间列表
输出：corpus_tfidf - tfidf的词向量空间
"""
def tf_idf(documents):
    # 将documents放入一个字典,这个字典按照拼音字母a-z的顺序排列documents
    dictionary = corpora.Dictionary(documents)
    #转换成词频，会去掉每个文本的重复词，并自动生成词向量空间
    corpus = [dictionary.doc2bow(text) for text in documents]
    # 将corpus作为初始化的参数，得到tfidf关于corpus的模型
    tfidf = models.TfidfModel(corpus)
    # 通过tfidf【】将词频转换成tfidf值
    corpus_tfidf = tfidf[corpus]

    return corpus_tfidf

"""
函数说明：进行LSI分析，并计算各个文档之间的相似度
输入：corpus_tfidf - tfidf的词向量空间
输出：CSV格式的LSI下三角相似度矩阵
"""
def LSI(corpus_tfidf):
    # 构造LSI模型并将待检索的query和文本转化为LSI主题向量
    # 转换之前的corpus是BOW向量
    lsi_model = models.LsiModel(corpus_tfidf,num_topics=80)
    corpus_lsi = lsi_model[corpus_tfidf]
    # 转换成潜语义文档向量列表并持久化
    corpora.MmCorpus.serialize('./lsi_test.mm', corpus_lsi)
    corpus_lsi = corpora.MmCorpus('./lsi_test.mm')
    # 构建文档相似度矩阵索引用于查询，再使用文档列表本身进行相似度查询（默认使用 Cosine）
    index = similarities.MatrixSimilarity(corpus_lsi)
    # 输出下三角矩阵
    with open('./lsi.csv', 'w') as fr:
        i = 1
        for sims in index[corpus_lsi]:
            a = sims[:i]
            fr.write(','.join(map(str, a)) + '\n')
            i += 1
"""
函数说明：进行LSI分析，并计算各个文档之间的相似度
输入：corpus_tfidf - tfidf的词向量空间
输出：CSV格式的VSM下三角相似度矩阵
"""
def VSM(corpus_tfidf):
    # 必须先把corpus_tfidf写入磁盘，因为矩阵太大，直接在内存计算相似度会导致内存不够
    corpora.MmCorpus.serialize('./vsm_test.mm', corpus_tfidf)
    corpus_tfidf = corpora.MmCorpus('./vsm_test.mm')
    # 用文档向量初始化一个相似度计算的对象
    # index = similarities.MatrixSimilarity(corpus_tfidf)
    index = similarities.SparseMatrixSimilarity(corpus_tfidf)
    #输出下三角矩阵
    with open('./vsm.csv', 'w') as fr:
        i = 1
        for sims in index[corpus_tfidf]:
            a = sims[:i]
            fr.write(','.join(map(str, a)) + '\n')
            i += 1
    num = 1 #查找第num篇文档的相似度，可自行修改
    query = sorted(enumerate(index[corpus_tfidf[num]]), key=lambda x: x[1], reverse=True)
    #返回最相似的前三个文档的序号
    print(query[:4])

"""
函数说明：进行测试
"""
def test():
    #加载数据并生成tfidf词向量空间
    documents = load_data('199801_clear.txt')
    corpus_tfidf = tf_idf(documents)
    #对词向量空间进行VSM的相应处理并计时
    VSMstart_time = time.time()
    VSM(corpus_tfidf)
    VSMend_time = time.time()
    print('VSM耗时：' + str(VSMend_time - VSMstart_time) + 's')
    # 对词向量空间进行LSI的相应处理并计时
    LSIstart_time = time.time()
    LSI(corpus_tfidf)
    LSIend_time = time.time()
    print('LSI耗时：' + str(LSIend_time - LSIstart_time) + 's')

if __name__ == '__main__':
    test()
