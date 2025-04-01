import psutil
from app.books_init import Books
from fastapi import FastAPI

# init
books = Books()
soldout_list = books.get_soldout_list()
dataframe = books.get_dataframe()
excel_file_name = books.get_excel_file_name()

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
                    "file_name": excel_file_name,
                    "soldout_list_size": len(soldout_list),
                }

    return {"detail": "default_page_error"}
