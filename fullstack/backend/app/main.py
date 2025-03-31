from fastapi import FastAPI
import psutil

app = FastAPI()

@app.get("/")
async def default_page():
    for _, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family.name == "AF_INET" and not snic.address.startswith("127."):
                return {"ip": snic.address, "port": "8000", "address": f"http://{snic.address}:8000"}

    return {"detail": "default_page_error"}
