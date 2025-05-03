from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """

    RequestValidationErrorをキャッチして、
    課題使用に基づいた HTTP 400 Bad Request レスポンスを生成するハンドラ
    ルーターレベルで使用する
    """

    # デバッグ用にエラーメッセージを出力
    print(f"Validation error caught by router-kevek handler: {exc.errors()}")

    # エラーレスポンスの内容を定義
    error_responce = {
        "status": status.HTTP_400_BAD_REQUEST,
        "message": "Bad request. Invalid input parameter 'n'."
    }

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_responce
    )
