#블루 프린트 가져오기

import re
from flask import Blueprint,render_template,request
from qksekf import db
from qksekf.models import Mymovie, Comment,Movie,User
from qksekf.service import navermovie_api
from sqlalchemy import and_
from collections import Counter
bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        userid = request.form['ID'] #post일 때 
        userpw = request.form['PW']
        isuser = User.query.filter(and_(User.id==userid, User.pw==userpw)).all()
        enter1 = "로그인 완료"
        enter2 = "잘못된 입력입니다"
        return render_template("login.html", userid=userid, isuser=isuser, enter1=enter1, enter2=enter2)

        

    




@bp.route('/findmovie',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template("data2.html")
    elif request.method == 'POST':
        m1 = request.form['movie1'] #post일 때 
        m2 = request.form['movie2']
        m3 = request.form['movie3']
        result = navermovie_api.movie3(m1,m2,m3)
        db.session.query(Mymovie).delete()
        for i in result:
            a = Mymovie(title=i)
            db.session.add(a) # db객체에 session이 붙어있음
        db.session.commit()
        return render_template('data2.html',m1=m1,result=result),200 #폴더 내부 파일이라 import 필요없음

@bp.route('/best5')
def mine():
    list = Mymovie.query.all()    
    return render_template('best5.html',list=list)



@bp.route('/new')
def real():
    recents = navermovie_api.recent_movie()
    recents_review = navermovie_api.recent_movie2()
    img1 = navermovie_api.get_img(recents[0])
    img2 = navermovie_api.get_img(recents[1])
    img3 = navermovie_api.get_img(recents[2])
    img4 =  navermovie_api.get_img(recents[3])
    
    return render_template('data.html', recents=recents,recents_review=recents_review, img1=img1, img2=img2, img3=img3, img4=img4),200

@bp.route('/datatable')
def datatable():
    return render_template('dist/table-datatable.html'),200

@bp.route('/comment')
def add_comment():
    new_text = request.args.get('q') #?q= 에 입력된 글자 가져오기

    if not new_text: # commnet가 없다면 
        return '입력된 것이 없어요', 404


    new_comment = Comment(text=new_text)

    db.session.add(new_comment) # db객체에 session이 붙어있음
    db.session.commit()

    return "추가 완료", 200






   
@bp.route('/sign',methods=['GET','POST'])
def sign():
    if request.method == 'GET':
        return render_template("form.html")
    elif request.method == 'POST':
        userid = request.form['ID'] #post일 때 
        email = request.form['Email']
        nick = request.form['Nickname']
        pw = request.form['PW']
        signup = User(id =userid, email=email, nickname = nick, pw=pw)
        db.session.add(signup) # db객체에 session이 붙어있음
        db.session.commit()
        com = "등록완료"
        dis = "다시 입력하세요"
        return render_template('form.html',signup=signup, userid=userid,com=com,dis=dis)