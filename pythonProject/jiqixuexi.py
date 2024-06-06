###特征工程
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import jieba#分词
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.feature_selection import VarianceThreshold
from scipy.stats import pearsonr
from sklearn.decomposition import PCA

###一、特征抽取
def datasets_demo():
    """
    sklearn数据集使用
    :return:
    """
    #获取数据集
    iris=load_iris()
    print("鸢尾花数据集: \n",iris)
    print("查看数据集描述: \n",iris["DESCR"])
    print("查看特征值的名字:\n",iris.feature_names)
    print("查看特征值:\n", iris.data,iris.data.shape)


    #数据集划分
    x_train,x_test,y_train,y_test=train_test_split(iris.data, iris.target,test_size=0.2,random_state=22)
    print("训练集的特征值 :\n",x_train,x_train.shape)
    return None
def dict_demo():
    """
    字典特征抽取
    :return:
    """
    data=[{'city':"北京",'temperature':100},{'city':'上海','temperature':60},{'city':'深圳','temperature':30}]
    #1实例化一个转换器类
    transfer=DictVectorizer(sparse=False)
    #2调用fit_transform()
    data_new=transfer.fit_transform(data)
    print("data_new:\n",data_new)
    print("特征名字:\n",transfer.get_feature_names_out())


    return None
def count_demo():
    """
    文本特征抽取
    :return:
    """
    data=["life is short, i like  like python",
          "life is too long, i   dislike python"]
    #1.实例化一个转换器类
    transfer=CountVectorizer()#包括stop_words停用词      #特征出现次数
    #2.调用fit_transform()
    data_new=transfer.fit_transform(data)
    print("特征名字:\n", transfer.get_feature_names_out())
    print("data_new:\n",data_new.toarray())

def count_chinese_demo():
    """
    中文文本特征抽取
    :return:
    """
    # data1=["我 爱 北京 天安门",
    #       "天安门 上 太阳 升"]
    data1=("我爱北京天安门,天安门上太阳升")
    data=jieba.cut(data1,cut_all=False)
    print("精确模式:"+"/".join(data))
    #1.实例化一个转换器类
    transfer=CountVectorizer()      #特征出现次数
    #2.调用fit_transform()
    data_new=transfer.fit_transform(data)
    print("特征名字:\n", transfer.get_feature_names_out())
    print("data_new:\n",data_new.toarray())
    return None
def count_chinese_demo2():
    """
    中文文本特征抽取，自动分词
    :return:
    """
    #1.将中文文本进行分词
    data=["马云说：“今天很残酷，明天更残酷，后天很美好。”这句话是说给两种人听的。一种是拼命努力而尚未看到希望的人。马云告诉他们要继续坚持，希望不在明天，而在后天。另一种是得过且"]
    data_new=[]
    for sent in data:
       data_new.append(cut_word(sent))
    # print(data_new)
    #1.实例化一个转换器类
    transfer=CountVectorizer()      #特征出现次数
    #2.调用fit_transform()
    data_final=transfer.fit_transform(data_new)
    print("特征名字:\n", transfer.get_feature_names_out())
    print("data_new:\n",data_final.toarray())
    return None

def cut_word(text):
    """
    进行中文分词"我爱北京天安么"->"我 爱 北京 天安门"
    :param text:
    :return:
    """
    text=" ".join(list(jieba.cut(text,cut_all=False)))
    return text
def tfidf_demo():
    """
    用tfidf的方法进行文本特征抽取
    :return:
    """
    data=["马云说,今天很残酷，明天更残酷，后天很美好。",
          "这句话是说给两种人听的。一种是拼命努力而尚未看到希望的人。",
          "马云告诉他们要继续坚持，希望不在明天，而在后天。另一种是得过且过。"]
    data_new=[]
    for sent in data:
       data_new.append(cut_word(sent))
    # print(data_new)
    #1.实例化一个转换器类
    transfer=TfidfVectorizer()      #特征出现次数
    #2.调用fit_transform()
    data_final=transfer.fit_transform(data_new)
    print("特征名字:\n", transfer.get_feature_names_out())
    print("data_new:\n",data_final.toarray())
    return None



###二、特征预处理
def minmax_demo():
    """
    归一化#(x-min)/(max-min)=X    X‘’=X*
    :return:
    """
    #1.获取数据
    data=pd.read_csv("data.txt")
    data=data.iloc[:,:3]
    print("data:\n",data)
    #2.实例化一个转换器类
    transfer=MinMaxScaler(feature_range=[0,1])
    #3.调用fit_transform()
    data_new=transfer.fit_transform(data)
    print("data_new:\n",data_new)
    return None

def  stand_demo():
    """
    标准化 #X'=(x-mean(平均值))/标准差
    :return: 
    """
    #1.获取数据
    data=pd.read_csv("data.txt")
    data=data.iloc[:,:3]
    print("data:\n",data)
    #2.实例化一个转换器类
    transfer=StandardScaler()
    #3.调用fit_transform()
    data_new=transfer.fit_transform(data)
    print("data_new:\n",data_new)
    return None
###三、特征降维（特征选择、主成分分析）
#特征选择：Filter过滤式 （低方差过滤）Embeded嵌入式
def variance_demo():
    """
    过滤低方差特征
    :return:
    """
    #1.获取数据
    data=pd.read_csv("")
    data=data.iloc[:,1:-2]
    #2.实例化一个转换器类
    transfer=VarianceThreshold(threshold=0)
    #3.调用fit_transform()
    data_new=transfer.fit_transform(data)
    print("data_new:\n",data_new)
    #计算某两个变量之间的相关系数
    r=pearsonr(data[""],data_new[""])  #pearson算法
    print("相关系数:\n",r)
    return None
###主成分分析(降维后尽可能减少特征数):
def pca_demo():
    """
    PCA降维
    :return:
    """
    data=[[2,8,4,5],[6,3,0,8],[5,4,9,1]]
    #1.实例化一个转换器类
    transfer=PCA(n_components=0.95)#n_components小数则保留百分比，整数则减少至多少
    #2.调用fit_transform()
    data_new=transfer.fit_transform(data)
    print("data_new:\n",data_new)

    return  None




if __name__=="__main__":
    #代码1:sklearn的数据集使用
    # datasets_demo()
    #代码2:字典特征抽取
    #dict_demo()
    #代码3:文本特征抽取
    #count_chinese_demo()
    #代码4:中文文本特征抽取
    #count_chinese_demo()
    #代码5:中文文本特征抽取，自动分词
    # count_chinese_demo2()
    #代码6:中文分词
    # cut_word("我爱北京天安门")
    #代码7：用tfidf的方法进行文本特征抽取
    # tfidf_demo()
    #代码8:归一化
    # minmax_demo()
    #代码9:标准化
    #stand_demo()
    #代码10：低方差特征过滤
    # variance_demo()
    #代码11：PCA降维
    pca_demo()