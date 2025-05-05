from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import FibonacciParameterError


async def fibonacci_parameter_errorhandler(
        request: Request,
        exc: FibonacciParameterError) -> JSONResponse:
    """
    フィボナッチエンドポイント用のパラメータエラーハンドラー
    課題仕様に沿ったレスポンス形式を返す
    """
    error_response = {
        "status": status.HTTP_400_BAD_REQUEST,
        "message": exc.message
    }

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response
    )
