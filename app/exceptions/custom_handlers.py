from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
        request: Request, exc: RequestValidationError):
    """
    リクエストパラメータのバリデーションエラーを処理するためのカスタムハンドラー
    fibonacciエンドポイントに特化したエラーメッセージを返す

    Args:
        request (Request): リクエストオブジェクト
        exc (RequestValidationError): バリデーションエラーオブジェクト

    Returns:
        JSONResponse: エラーレスポンス
    """
    # リクエストURLが"/fib"で始まる場合
    if request.url.path.startswith("/fib"):
        errors = exc.errors()
        error_message = "Bad request."

        if errors and len(errors) > 0:
            error_detail = errors[0]
            error_type = error_detail.get("type")

            # パラメータが見つからない場合 - 400 Bad Request
            if error_type == "missing":
                error_message = ("Bad request. Query parameter 'n' "
                                 "(positive integer) is required.")
                status_code = status.HTTP_400_BAD_REQUEST

            # 型変換エラー、範囲エラー、小数エラーの場合 - すべて422 Unprocessable Entity
            elif any(err_type in error_type for err_type in [
                "type_error", "greater_than_equal", "less_than", "int_parsing"
            ]):
                input_value = request.query_params.get("n", "unknown")
                error_message = (f"Bad request. Input 'n' must be "
                                 f"a positive integer (>= 1). Received: {input_value}")
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

            # その他のエラー - 400 Bad Request（デフォルト）
            else:
                status_code = status.HTTP_400_BAD_REQUEST
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return JSONResponse(
            status_code=status_code,
            content={"status": status_code, "message": error_message}
        )

    # "/fib"以外のエンドポイントからのリクエストの場合はデフォルトのエラーレスポンスを返す
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )
