from fastapi import FastAPI, UploadFile,Form,Response,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager #FASTAPI 로그인 매니저 설치 23.07.05
from fastapi_login.exceptions import InvalidCredentialsException #유효하지않은 계정정보에 대한 에러 처리 07.05
from typing import Annotated

import sqlite3

con = sqlite3.connect('db.db',check_same_thread=False) #SQLLITE 연결
cur = con.cursor()

app = FastAPI()
#sercret을 어떻게 인코딩 할건지 정함 잘못되면 디코딩 23.07.05
SERCRET = "super-coding"
#안에다가 sercret을 입력해야됨 
manager = LoginManager(SERCRET,'/login')

@manager.user_loader() #user_loader를 호출 
def  query_user(data): #쿼리를 이용해서 유저 정보 가져옴
     WHERE_STATEMENTS =f'id="{data}"'
     if type(data) == dict:
         WHERE_STATEMENTS = f'''id="{data["id"]}"'''
         
     con.row_factory = sqlite3.Row
     cur = con.cursor()
     user = cur.execute(f"""
                       SELECT * from users WHERE id='{WHERE_STATEMENTS}'
                       """).fetchone()
     return user

@app.post('/signup')   #회원가입 정보 저장을 위한 테이블을 만듦
def signup(id:Annotated[str,Form()],
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):
    cur.execute(f"""
                INSERT INTO users(id,name,email,password)
                VALUES ('{id}','{name}','{email}','{password}')
                """)
    con.commit()
    print (id, password)
    return '200'

#23.07.05
@app.post('/login')
def login(id:Annotated[str,Form()],
           password:Annotated[str,Form()]):
    user = query_user(id) #user는 query_user로 통해 id를 받음
    if not user :   #pytion에서는 raise로 에러 메시지를 던짐 07.05
        raise InvalidCredentialsException  # print(user)성공 할시 user 정보가 터미널에 뜨는걸 볼수있음 23.07.05
    elif password != user['password']: #elif = else if
        raise InvalidCredentialsException #401을 자동으로 내려줌
    #token 만드는 방법 07.05
    access_token = manager.create_access_token(data={
    'sub' : {
        'id':user['id'],
        'name':user['name'],
        'email' :user['email']
        }
    })
    
    
    return {'access_token':access_token} #자동으로 200코드를 내줌 
#유효하지 않은 유저가 로그인을 할시 401 에러를 나타냄 07.05


@app.post('/items')
async def create_item(image: UploadFile, #AWAIT 을 썼기에 앞에는 async
                title: Annotated[str, Form()],
                price: Annotated[int, Form()],
                description: Annotated[str, Form()],
                place: Annotated[str, Form()],
                insertAt:Annotated[int,Form()],
                user=Depends(manager)):
    
    image_bytes =await image.read() #await을 씀으로 써 읽는 시간을줌 
   
    cur.execute(f"""  
                INSERT INTO items(title,image,price,description,place,InsertAt)
                VALUES ('{title}','{image_bytes.hex()}' ,{price} ,'{description}','{place}',{insertAt})
                """)#SQL 문법 image bytes로 바꿧기때문 hex로 
    con.commit() #itmes 테이블에 Valeus 값을 넣어주는 개념 
    return '200'     #javacript ` ` 같은 개념  이미지와 타이틀 프라이스르를 정보도 다 읽었기때문에 데이터베이스에 인설트
#여기 까지 하면 서버 오류가 나는것을 볼 수 있음 price 같은 경우 int 이기 때문에 ''뺌  VALEUS(X)  VALUES(O)

@app.get ('/items') #유저가 인증된 상태에서만 보내주겠다라는 뜻
def get_items(user=Depends(manager)):
    con.row_factory = sqlite3.Row #컬럼명도 가져옴
    cur = con.cursor() #올려주는거
    rows = cur.execute(f"""
                       SELECT * from items;
                       """).fetchall()
    
    
    return JSONResponse(jsonable_encoder(dict(row) for row in rows)) #각각 정리가 되서 나옴
                             
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
	            id INTEGER PRIMARY KEY,
	            title TEXT NOT NULL,
	            image BLOB,
	            Price INTEGER NOT NULL,
	            description TEXT,
	            place TEXT NOT NULL,
	            insertAt INTEGER NOT NULL
            );
            """)                             
                                    
@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    image_bytes = cur.execute(f"""
                              SELECT image from items WHERE id={item_id}
                              """).fetchone()[0]
    return Response(content=bytes.fromhex(image_bytes),media_type='image/*') #16진법으로 된것을 바꾸겠다




app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
