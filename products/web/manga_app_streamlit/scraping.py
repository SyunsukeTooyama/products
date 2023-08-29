from sqlalchemy import create_engine
from sqlalchemy.schema import Column
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import Integer, String, DATETIME
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup 
import requests
import pandas as pd
import datetime

#スクレイピング
headers="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58"
def get_magapoke():
    url_mag = "https://pocket.shonenmagazine.com/series"
    res = requests.get(url_mag,headers={"User-Agent":headers})
    soup=BeautifulSoup(res.text,'html.parser')
    items = soup.find_all('li',{'class':'daily-series-item'})

    items_data=[]
    for item in items:
        item_data={}
        item_data['title']=item.find('h4',{'class':'daily-series-title'}).text
        item_data['author']=item.find('h5',{'class':'daily-series-author'}).text
        item_data['url']=item.find('a')['href']
        items_data.append(item_data)

    df=pd.DataFrame(items_data)
    df['app']='マガポケ'
    df['remarks']='連載中'

    return df

options={'':'連載中',
        'oneshot':'読切',
        'finished':'連載終了',
        }

def get_jump(option):
    if option == '':
        url_jump ="https://shonenjumpplus.com/series"
    else:
        url_jump ="https://shonenjumpplus.com/series" + '/' + option
    res = requests.get(url_jump,headers={"User-Agent":headers})
    soup=BeautifulSoup(res.text,'html.parser')
    items = soup.find_all('li',{'class':'series-list-item'})
    items_data=[]
    for item in items:
        item_data={}
        item_data['title']=item.find('h2',{'class':'series-list-title'}).text
        item_data['author']=item.find('h3',{'class':'series-list-author'}).text
        item_data['url']=item.find('a')['href']
        items_data.append(item_data)

    df=pd.DataFrame(items_data)
    df['app']='ジャンプ＋'
    df['remarks']=options[option]

    return df

def get_sunday():
    url_sun = "https://www.sunday-webry.com/series"
    res = requests.get(url_sun,headers={"User-Agent":headers})
    soup=BeautifulSoup(res.text,'html.parser')
    
    items = soup.find_all('li',{'class':'webry-series-item test-series'})
    

    items_data=[]
    for item in items:
        item_data={}
        item_data['title']=item.find('h4',{'class':'test-series-title series-title'}).text
        item_data['author']=item.find('p',{'class':'author'}).text
        item_data['url']=item.find('a')['href']
        items_data.append(item_data)

        df_series=pd.DataFrame(items_data)
        df_series['app']='サンデーうぇぶり'
        df_series['remarks']='連載中'

    item_not_series=items[:len(items)-2]

    items_not_series=[]
    for item in item_not_series:
        item_data={}
        item_data['title']=item.find('h4',{'class':'test-series-title series-title'}).text
        item_data['author']=item.find('p',{'class':'author'}).text
        item_data['url']=item.find('a')['href']
        items_not_series.append(item_data)

        df_not_series=pd.DataFrame(items_not_series)
        df_not_series['app']='サンデーうぇぶり'
        df_not_series['remarks']='連載終了/その他'

    df = pd.concat([df_series,df_not_series])

    return df

df_maga = get_magapoke()

df_jump = pd.DataFrame()
for option in options.keys():
    df_jump_con = pd.DataFrame(get_jump(option))
    df_jump = pd.concat([df_jump,df_jump_con])

df_sun = get_sunday()

df=pd.concat([df_maga,df_jump,df_sun],axis=0)

#DB
user = 'ユーザ名'
password = 'パスワード'
host = 'ホスト名'
db_name = 'データベース名'

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}")

Base = declarative_base()

class Book(Base):
    __tablename__="mangaapp"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    author = Column(String(255))
    url = Column(String(255))
    app = Column(String(255))
    remarks = Column(String(255))

class User(Base):
    __tablename__="user"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    password = Column(String(255))
    favorite = Column(String(1020))

class Bug(Base):
    __tablename__="bug"
    id = Column(Integer, primary_key=True)
    text = Column(String(1020))
    time = Column(DATETIME)

SessionClass = sessionmaker(engine)
session = SessionClass()

'''#空テーブル回避
book_data=Book(title="a",author="a",url='a',app='a',remarks='a')
session.add(book_data)
session.commit()
'''

#初期化
books_init = session.query(Book).all()
for book_init in books_init:
    session.delete(book_init)
session.commit()

#書き込み
books_add = df
for book_add in books_add.itertuples():
    book_data=Book(title=book_add.title,author=book_add.author,url=book_add.url,app=book_add.app,remarks=book_add.remarks)
    session.add(book_data)
session.commit()