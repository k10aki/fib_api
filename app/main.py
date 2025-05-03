from fastapi import FastAPI

from app.routers.fibonacci import router as fibonacci_router


app = FastAPI()

# ルーターの登録
app.include_router(fibonacci_router)

# ルートエンドポイントの定義
@app.get("/")
async def read_root():
    """
    ルートエンドポイント
    """
    return {"message":
            "Welcome to the Fibonacci API! See /docs for API documentation."}
