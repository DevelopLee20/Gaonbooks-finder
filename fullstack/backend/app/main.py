import socket

import numpy as np
from app.books_init import Books
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# init
books = Books()

# app
app = FastAPI(
    title="Gaonbooks",
)

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="app/templates")

# 정적 파일 제공 (CSS, JS 등)
# app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/assets", StaticFiles(directory="app/assets"), name="assets")

# 주소 반환
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f"http://{local_ip}:8000")
print(books.latest_file)


def get_title_img(title: str) -> str:
    return "/assets/mas.png"


@app.get("/")
async def find_page():
    return templates.TemplateResponse("find.html", {"request": {}})


@app.get("/find/{input_book_name}/")
async def find_book(input_book_name: str):
    user_input = input_book_name.strip()
    if user_input == "":
        return []

    filtered_df = books.dataframe[
        books.dataframe["도서명"].str.contains(user_input, case=False, na=False)
    ].copy()

    filtered_df = filtered_df.replace([np.inf, -np.inf], np.nan).fillna("")

    result = []
    for _, row in filtered_df.iterrows():
        book_info = row.to_dict()
        title = book_info.get("도서명", "")
        book_info["cover"] = get_title_img(title)
        result.append(book_info)

    return result
