from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"data": "McGill AI Society Project X, 2022-2023"}
