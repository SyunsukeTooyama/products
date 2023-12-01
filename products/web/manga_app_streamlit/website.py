import streamlit as stl
from sqlalchemy import create_engine
from sqlalchemy.schema import Column
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import Integer, String, DATETIME
from sqlalchemy.orm import sessionmaker
import pandas as pd
from scraping import Book, User, Bug
import datetime

#DB
user = 'ユーザ名'
password = 'パスワード'
host = 'ホスト名'
db_name = 'データベース名'

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}")

Base = declarative_base()

SessionClass = sessionmaker(engine)
session = SessionClass()

users_data = session.query(User).all()

books_data = session.query(Book).all()

df=[]
for book_add in books_data:
    book_data={'title':book_add.title,'author':book_add.author,'url':book_add.url,'app':book_add.app,'remarks':book_add.remarks}
    df.append(book_data)
df=pd.DataFrame(df)

stl.set_page_config(
    page_title="漫画アプリ検索",
    layout="wide",
    initial_sidebar_state="expanded"
)

def change_page():
    stl.session_state.page_control=1

def register():
    if (stl.session_state.password==stl.session_state.password2) and (stl.session_state.user) and (stl.session_state.password):
        stl.session_state.login=True
        stl.session_state.page_control = 0
        stl.session_state['user'] = stl.session_state.user

    #DBに追加
        user_data=User(name=stl.session_state.user,password=stl.session_state.password)
        session.add(user_data)
        session.commit()

    elif not(stl.session_state.user):
        stl.sidebar.warning('ユーザー名を入力してください。')
    elif stl.session_state.password!=stl.session_state.password2:
        stl.sidebar.warning('パスワードが異なります。')
    else:
        stl.sidebar.warning('パスワードを入力してください。')

def signin():
    users_info = session.query(User).filter_by(name=stl.session_state.user).all()
    for user_info in users_info:
        if stl.session_state.password == user_info.password:
            stl.session_state.login=True

    if stl.session_state.login == False:
        stl.sidebar.warning('ユーザー名またはパスワードが違います。')        

def signout():
    stl.session_state.login=False

if ('user' not in stl.session_state):
    stl.session_state['user'] = '' 
elif ('user' in stl.session_state):
    stl.session_state['user'] = stl.session_state.user
    stl.session_state['password'] = stl.session_state.password

def signup_page():
    stl.sidebar.write("## 新規登録")
    stl.sidebar.text_input("ユーザー名",key='user')
    stl.sidebar.text_input("パスワード",type='password',key='password')
    stl.sidebar.text_input("パスワード",type='password',key='password2')
    stl.sidebar.button("登録する",on_click=register)

def login_page():
    if ('login' in stl.session_state) and (stl.session_state.login==True):
        stl.sidebar.write('### ログイン状態')
        stl.sidebar.write(stl.session_state.user +'さん、ログイン中です。')
        stl.sidebar.button('sign_out',on_click=signout)

    else:
        stl.sidebar.write("## 簡易ログイン")
        stl.sidebar.text_input("ユーザー名",key='user')
        stl.sidebar.text_input("パスワード",type='password',key='password')
        stl.session_state.login=False
        sign_in,sign_up=stl.sidebar.columns([2,3])
        with sign_in:
            stl.button('sign in',on_click=signin)
        with sign_up:
            stl.button('sign up (新規登録)',on_click=change_page)

stl.sidebar.write("## 設定")
table_size=stl.sidebar.slider('表サイズ',min_value=10,max_value=510,step=100,value=100)

if ("page_control" in stl.session_state and stl.session_state["page_control"] == 1):
    signup_page()
else:
    stl.session_state["page_control"] = 0
    login_page()


tab1,tab2,tab3 = stl.tabs(["検索","マイページ","バグ報告"])

options={'':'連載中',
        'oneshot':'読切',
        'finished':'連載終了',
        }

df['読みたい！']=False

with tab1:
    stl.title('漫画アプリ検索')

    col1,col2=stl.columns([3,1])
    with col1:
        stl.text_input('絞り込むには作品名、作者名、アプリ名のキーワードを入力してください',key='keyword')
    with col2:
        option=stl.selectbox('絞り込み要素',('すべて','作品名','作者名','アプリ名'),key='filter_elem')

    if stl.session_state.filter_elem=='すべて':
        df=df
    elif stl.session_state.filter_elem=='作品名':
        df=df[df['title'].str.contains(stl.session_state.keyword)]

    elif stl.session_state.filter_elem=='作者名':
        df=df[df['author'].str.contains(stl.session_state.keyword)]

    elif stl.session_state.filter_elem=='アプリ名':
        df=df[df['app'].str.contains(stl.session_state.keyword)]

    edited=stl.data_editor(
        df,
        column_config={
            'title': stl.column_config.TextColumn(
                "title",
                width="large"
            ),
            'author': stl.column_config.TextColumn(
                "author",
                width="medium"
            ),
            'url': stl.column_config.LinkColumn(
                "URL",
                width="medium",
                help="URLをダブルクリックでリンクに飛べます。"
            ),
            'remarks': stl.column_config.TextColumn(
                "備考",
                width="small"
            ),
            '読みたい！':stl.column_config.CheckboxColumn(
                "ブックマーク",
                help="ブックマークに追加するものを選んでください。",
                default=False
            ),   
        },
        disabled= ['title','author','URL','app','備考'],
        height=5*table_size
    )

    wantedtoread=edited
    wantedtoread=edited[wantedtoread["読みたい！"]]

    def mypage():
            fav_titles = wantedtoread['title'].to_list()
            users_info = session.query(User).filter_by(name=stl.session_state.user,password=stl.session_state.password).first()
            if stl.session_state.login==False:
                stl.warning('マイページに追加するにはログインしてください。')
            else:
                if users_info.favorite:
                    user_list=users_info.favorite.split(',')
                else:
                    user_list=[]            
                user_set=set(user_list)
                user_set.update(tuple(fav_titles))
                users_info.favorite =",".join(list(user_set))
                session.commit()
        
    bookmark_text,to_mypage=stl.columns([2,3])
    with bookmark_text:
        stl.write('ブックマークした作品')
    with to_mypage:
        stl.button('マイページに追加',on_click=mypage)
    wantedtoread=stl.data_editor(
        wantedtoread,
        column_config={
            'title': stl.column_config.TextColumn(
                "title",
                width="large"
            ),
            'author': stl.column_config.TextColumn(
                "author",
                width="medium"
            ),
            'url': stl.column_config.LinkColumn(
                "URL",
                width="medium",
                help="URLをダブルクリックでリンクに飛べます。"
            ),
            '読みたい！':stl.column_config.CheckboxColumn(
                "ブックマーク",
                default=False
            ), 
        },
        disabled= ['title','author','app','URL','備考','読みたい！'],
    )
    stl.write('ページ遷移後もブックマークを保持するには\nマイページに追加してください。')

with tab2:
    stl.write('## マイページ')
    if stl.session_state.login:
        fav_books=[]
        user_fav_before = session.query(User).filter_by(name=stl.session_state.user,password=stl.session_state.password).first().favorite
        if user_fav_before:
            user_favs = user_fav_before.split(',')
            for user_fav in user_favs:
                fav_books.append(session.query(Book).filter_by(title=user_fav).first())
            fav_books_data=[]
            print(fav_books)
            print(type(fav_books))
            for fav_book in fav_books:
                fav_data={'title':fav_book.title,'author':fav_book.author,'url':fav_book.url,'app':fav_book.app,'remarks':fav_book.remarks}
                fav_books_data.append(fav_data)
            df_fav=pd.DataFrame(fav_books_data)
            df_fav["削除"]=False

            def delete_book():
                mypage_delete_set=set(mypage_bookmark[mypage_bookmark['削除']]['title'].to_list())
                favs_delete = session.query(User).filter_by(name=stl.session_state.user,password=stl.session_state.password).first()
                user_delete_set=set(favs_delete.favorite.split(','))
                afterdel=user_delete_set-mypage_delete_set
                afterdel_list=list(afterdel)
                favs_delete.favorite = ",".join(afterdel_list)
                session.commit()

            mypage_text,bookmark_button=stl.columns([4,5])
            with mypage_text:
                stl.write('ブックマークした作品')
            with bookmark_button:
                stl.button('選択項目の削除', on_click=delete_book)
            mypage_bookmark=stl.data_editor(
            df_fav,
            column_config={
                'title': stl.column_config.TextColumn(
                    "title",
                    width="large"
                ),
                'author': stl.column_config.TextColumn(
                    "author",
                    width="medium"
                ),
                'url': stl.column_config.LinkColumn(
                    "URL",
                    width="medium",
                    help="URLをダブルクリックでリンクに飛べます。"
                ),
                '削除':stl.column_config.CheckboxColumn(
                    "削除",
                    default=False
                ), 
            },
            disabled= ['title','author','app','URL','備考'],
            )

        else:
            stl.write('ブックマークされた作品はありません。')
    else:
        stl.write('ログインしてください')

with tab3:
    stl.write('## バグ報告/改善点')
    stl.text_area('バグや改善点が見つかった場合は報告していただけるとありがたいです。',key='bug_improve')
    
    for book_add in books_data:
        book_data={'title':book_add.title,'author':book_add.author,'url':book_add.url,'app':book_add.app,'remarks':book_add.remarks}
        
    def submit():
        bug_txt = stl.session_state.bug_improve
        add_bug = Bug(text=bug_txt, time=datetime.datetime.now())
        session.add(add_bug)
        session.commit()
        

    bug_col1,bug_col2 = stl.columns([8,2])
    with bug_col1:
        pass
    with bug_col2:
        stl.button('提出',on_click=submit)
    
    def show_text():
        bug_datum = session.query(Bug).all()
        for bug_data in bug_datum:
            stl.write(bug_data.time, bug_data.text)  
    
    stl.write('## Log')
    show_text()
