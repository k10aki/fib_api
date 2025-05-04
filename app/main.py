from fastapi import FastAPI

from app.routers.fibonacci import router as fibonacci_router
from app.exceptions.custom_exceptions import FibonacciParameterError
from app.exceptions.custom_handlers import fibonacci_parameter_handler


app = FastAPI()

# ルーターの登録
app.include_router(fibonacci_router)

# fib用のカスタムエラーハンドラーの登録
app.add_exception_handler(
    FibonacciParameterError,
    fibonacci_parameter_handler
)

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
