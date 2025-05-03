from fastapi import FastAPI, Query, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Annotated

from fibonacci import calculate_fibonacci

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    FastAPIのデフォルトのバリデーションエラー(422)を捕捉し、
    課題仕様の400エラーレスポンスに変換します。

    Args:
        request (Request): リクエストオブジェクト
        exc (RequestValidationError): バリデーションエラー

    Returns:
        JSONResponse: エラーレスポンス
    """

    error_response = {
        "status": status.HTTP_400_BAD_REQUEST, # 400 を設定
        "message": "Bad request. Invalid input parameter 'n'." # 課題に合わせたメッセージ
    }

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response
    )

@app.get("/fib")
async def get_fibonacci(n: Annotated[int, Query(ge=1)]):
    """
    n番目のフィボナッチ数を計算するAPIエンドポイント。
    クエリパラメータとしてnを受け取り、フィボナッチ数列のn番目の値を返す。
    nは1以上の整数

    Args:
        n (int): フィボナッチ数列のインデックス (1以上の整数)
        クエリパラメータとして指定する。

    Returns:
        int: n番目のフィボナッチ数
    """

    return {"result": calculate_fibonacci(n)}
