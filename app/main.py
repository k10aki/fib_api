from fastapi import FastAPI, Query
from fastapi.exceptions import RequestValidationError

from app.routers.fibonacci import router as fibonacci_router
from app.exceptions.custom_handlers import validation_exception_handler


app = FastAPI()

# RequestValidationErrorハンドラーの登録
# エンドポイント"/fib"に特化したカスタムハンドラーを登録
# これにより、"/fib"エンドポイントに対するリクエストのバリデーションエラーが発生した場合、
# エンドポイント"/fib"に特化したカスタムハンドラーが呼び出される
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler)

# ルーターの登録
app.include_router(fibonacci_router)


# ルートエンドポイントの定義
@app.get("/")
def read_root():
    """
    ルートエンドポイント
    """
    return {"message":
            "Welcome to the Fibonacci API! See /docs for API documentation."}
