from fastapi import FastAPI, UploadFile,Form,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db',check_same_thread=False) #SQLLITE 연결
cur = con.cursor()

app = FastAPI()


@app.post('/items')
async def create_item(image: UploadFile, #AWAIT 을 썼기에 앞에는 async
                title: Annotated[str, Form()],
                price: Annotated[int, Form()],
                description: Annotated[str, Form()],
                place: Annotated[str, Form()],
                insertAt:Annotated[int,Form()]):
    
    image_bytes =await image.read() #await을 씀으로 써 읽는 시간을줌 
   
    cur.execute(f"""  
                INSERT INTO items(title,image,price,description,place,InsertAt)
                VALUES ('{title}','{image_bytes.hex()}' ,{price} ,'{description}','{place}',{insertAt})
                """)#SQL 문법 image bytes로 바꿧기때문 hex로 
    con.commit() #itmes 테이블에 Valeus 값을 넣어주는 개념 
    return '200'     #javacript ` ` 같은 개념  이미지와 타이틀 프라이스르를 정보도 다 읽었기때문에 데이터베이스에 인설트
#여기 까지 하면 서버 오류가 나는것을 볼 수 있음 price 같은 경우 int 이기 때문에 ''뺌  VALEUS(X)  VALUES(O)

@app.get ('/items')
async def get_items():
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
