
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate #데이터베이스 연결도구
import os

# 1) __init__.py 처음 형성 폴더
# 2) 파이썬 가상환경 생성
# 3) 블루 프린터 설정 main_routes 형성
# 4) 부스트트랩 탬플릿 가져오기 mian.html
# 5) db 만들기
# 6) migrate로 db 연결시키기
#FLASK_APP=qksekf flask run

db = SQLAlchemy()
migrate= Migrate()

def create_app():
    app = Flask(__name__) #앱 생성
    # app.config : 플라스크의 앱 내부 설정
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # db 주소 
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://hmrbtvnbrfmazg:acb569db97580a4588a921f9f821bfbd267426e12bd4d5813e1fdf87372a8e60@ec2-52-6-211-59.compute-1.amazonaws.com:5432/ddvr1ata3kfu3t"
   #app.config['SQLALCHEMY_DATABASE_URI']= os.getenv('DATABASE_URI')



    with app.app_context(): # 안전한 db 설정 방법 : with 블럭 내의 db가 현재 app에 접근
        db.init_app(app)
        migrate.init_app(app, db)

    from qksekf.routes.main_routes import bp 
    app.register_blueprint(bp) #main_routess의 bp 등록
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


#2) 부스트트랩 탬플렛 