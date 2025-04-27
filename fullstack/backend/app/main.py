import json

import psutil
from app.books_init import Books
from fastapi import FastAPI

# init
books = Books()

# app
app = FastAPI(
    title="Gaonbooks",
)


@app.get("/")
async def default_page():
    for _, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family.name == "AF_INET" and not snic.address.startswith("127."):
                return {
                    "address": f"http://{snic.address}:8000",
                    "file_name": books.latest_file,
                    "soldout_list_size": len(books.soldout_list),
                }

    return {"detail": "default_page_error"}


@app.get("/find/{input_book_name}/")
async def find_book(input_book_name: str):
    user_input = input_book_name.strip()

    if user_input == "":
        return

    filtered_df = books.dataframe[
        books.dataframe["도서명"].str.contains(user_input, case=False, na=False)
    ].copy()

    # orient: 리스트로 출력, force_ascii: 한글 출력 가능
    json_df = filtered_df.to_json(orient="records", force_ascii=False)

    return json.loads(json_df)
