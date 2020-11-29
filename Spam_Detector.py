import os 
import nltk
import joblib
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer #倒入词性还原
WNL = WordNetLemmatizer()

base_path = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_path,'Email_list') #输入邮件地址
#读取字典
word_dict = pickle.load(open('WORD_DICTIONARY.pkl','rb'))
#读取训练好的模型
RFC = joblib.load('Detector_Model.m')
#读取邮件
email_vector_list = []
for email_name in os.listdir(input_path):
    with open(os.path.join(input_path,email_name),'r',encoding='utf-8',errors='ignore') as email_text:
        email = email_text.read()
        word_list = word_tokenize(email)#切分为单个的词
        stop_words = stopwords.words('english')
        word_list_1 = [WNL.lemmatize(WNL.lemmatize(word.lower(),'v'),'n') for word in word_list if word.isalnum() and not word in stop_words]
        #生成邮件向量
        feature = [word_list_1.count(word) for word in word_dict]
        #print(feature)
        lable = RFC.predict([feature])
        if lable[0] == 'SPAM':
            print('{} is a junk mail'.format(email_name))
        elif lable[0] =='LEGAL':
            print('{} is a legitimate email'.format(email_name))

            



        