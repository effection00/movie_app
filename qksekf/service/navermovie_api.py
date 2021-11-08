import re
import collections
import bs4
import requests
from bs4 import BeautifulSoup
import urllib.request
#from qksekf.models import Movie
#from qksekf import db

BASE_URL = "https://movie.naver.com/movie"

def get_html(page_url):
    
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def get_movie_code(movie_title='소울'):
  
    search_url = f"{BASE_URL}/search/result.naver?query={movie_title}&section=all&ie=utf8"
    soup = get_html(search_url)

    link = soup.find_all('p',class_= "result_thumb")
    link_list=[]
    for i in link:
       link_list.append(i.find('a')['href'])
    movielink = link_list[0]
    movie_code=int(re.sub(r'[^0-9]', '',movielink))   
    return movie_code

def get_one(movie_title, page_num):
    movie_code = get_movie_code(movie_title)
    review_url = f"{BASE_URL}/point/af/list.naver?st=mcode&sword={movie_code}&target=after&page={page_num}"
    soup = get_html(review_url)
    data1 = soup.find_all('td','num')
    data_list =[]
    for a in data1:
        d = a.get_text("_",strip=True).split("_")
        data_list.append(d)
    id_list = []
    for b in data_list[1::2]:
        id_list.append(b[0])

    data2 = soup.find_all('td','title')
    review_list = []
    for f,e in zip(id_list ,data2):
        review = {
                'id' : str(f),
                'review_text':str(e.get_text("_",strip=True).split('_')[3]),
                'review_star': float(e.get_text("_",strip=True).split('_')[2]),
                'movie_title' : str(movie_title)
                }
        review_list.append(review)
    return review_list
 
def get_all(movie_title, page_num=5):
    a = get_one(movie_title,1)
    for i in range(2,page_num+1):
        a = a + get_one(movie_title, i)
    return a


# 9점 이상 준 고객의 id 
def get_code_one(movie_title, page_num=1):
    movie_code = get_movie_code(movie_title)
    review_url = f"{BASE_URL}/point/af/list.naver?st=mcode&sword={movie_code}&target=after&page={page_num}"
    soup = get_html(review_url)
    
        
    li =[]
    for e in soup.find_all('tr'):
        if e.find("em") == None:
            pass
        elif int(e.find("em").get_text()) > 8:
            li.append(e.find('td',class_='ac num'))
        else:
            pass
    li = filter(None,li)
    newli = []
    for p in li:
        newli.append(p.get_text())
    return newli 

# n 페이지까지의 9점 이상 준 id 
def get_code_all(movie_title, page_num=10):
    a = get_code_one(movie_title,1)
    for i in range(2,page_num+1):
        a = a + get_code_one(movie_title, i)
    return a


def high_class_user(movie_title):
    user_numbers = get_code_all(movie_title)
    list = []
    for user_number in user_numbers:
        URL = f"{BASE_URL}/point/af/list.naver?st=nickname&sword={user_number}&target=after&page=1"
        if int(get_html(URL).find('strong','c_88 fs_11').get_text()) >= 40:
            prt = user_number
            list.append(prt)
    return list



# 해당 영화 9점 이상 준 관람객들이 9점 이상 준 영화 
def get_one_one(movie_title, page_num=1):
    id_codes = high_class_user(movie_title)
    id_list = []
    list=[]
    for id_code in id_codes:
        review_url = f"{BASE_URL}/point/af/list.naver?st=nickname&sword={id_code}&target=after&page={page_num}"
        soup = get_html(review_url)
        id = soup.find_all('td','title')
        review_list = []
        for b in id:
            review = {
                'movie_name' : str(b.get_text("_",strip=True).split('_')[0]),
                'review_text':str(b.get_text("_",strip=True).split('_')[3]),
                'review_star': float(b.get_text("_",strip=True).split('_')[2]),
                 }
            if review['review_star'] > 8:
                review_list.append(review['movie_name'])
        id_list.append(review_list)
    for a  in id_list:
        list = list +a
    return list

def get_all_all(movie_title, page_num=5):
    a = get_one_one(movie_title,1)
    for i in range(2,page_num+1):
        a = a + get_one_one(movie_title, i)
    return a
    


#해당 영화 본 사람이 쓴 리뷰 : 데이터베이스에 넣은 후 별점 9점 이상인 영화 가려낼 것
# 빈칸에 영화제목 치면 데이터베이스로 해당 영화 들어옴 

def push_movie_db(movie_title):
    for i in get_one_one(movie_title):
        for a in i:
            new_review = Movie(movie_name=a['movie_name'], review_text=a['review_text'], review_star=a['review_star'])
            db.session.add(new_review) # db객체에 session이 붙어있음
            db.session.commit()
    return "push comlete"

def recent_movie():
    soup = get_html("https://movie.naver.com/movie/running/current.naver")
    recent = soup.find_all('dt','tit','a')[:4]
    list =[]
    list2=[]
    for i in recent:
       list.append(i.get_text().strip().split('\n'))
    best = list
    for a in best:
        list2.append(a[1])
    return list2

def movie3(movie1, movie2, movie3):
    list = get_one_one(movie1)+ get_one_one(movie2)+get_one_one(movie3)
    count = collections.Counter(list)
    best = count.most_common(8)
    return best[3][0],best[4][0],best[5][0],best[6][0],best[7][0]

def get_img(movie_title):     
    code = get_movie_code(movie_title)
    link= f'https://movie.naver.com/movie/bi/mi/basic.naver?code={code}'
    soup = get_html(link)
    recent = soup.find('div',class_ ='poster')
    new = recent.find('img')['src'] # src 크롤링 
    return new




def recent_movie2():
    soup = get_html("https://movie.naver.com/movie/point/af/list.naver")
    recent = soup.find_all('td','title','a')
    review_list = []
    for b in recent:
        review = {
            'movie_title' : str(b.get_text("_",strip=True).split('_')[0]),
            'review_text':str(b.get_text("_",strip=True).split('_')[3]),
            'review_star': float(b.get_text("_",strip=True).split('_')[2]),
                }
        review_list.append(review)
    return review_list

print(recent_movie())