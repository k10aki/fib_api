from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
        request: Request, exc: RequestValidationError):
    """
    リクエストバリデーションエラー用のハンドラー
    /fib エンドポイントのみカスタムレスポンス形式、それ以外は標準形式で返す
    今後の拡張性を考慮して、/fib エンドポイントのみに適用
    """
    # /fib エンドポイントからのリクエストの場合のみカスタム形式でレスポンスを返す
    if request.url.path.startswith("/fib"):
        errors = exc.errors()
        error_message = "Bad request."
        print(f"Validation error: {errors}")
        # エラーの種類に応じてメッセージを設定
        if errors and len(errors) > 0:
            error_detail = errors[0]
            error_type = error_detail.get("type")
            
            # パラメータが見つからない場合
            if error_type == "missing":
                error_message = ("Bad request."
                                 "Query parameter 'n' (positive integer) is required.")
            # 型変換エラーの場合
            elif "type_error" in error_type:
                input_value = request.query_params.get("n", "unknown")
                error_message = (f"Bad request. Input 'n' must be "
                                 f"a positive integer (>= 1). Received: {input_value}")
            # 範囲エラーの場合
            elif ("greater_than_equal" in error_type or
                  "less_than" in error_type):
                input_value = request.query_params.get("n", "unknown")
                error_message = (f"Bad request. Input 'n' must be a positive integer "
                                 f"(>= 1). Received: {input_value}")
            # 小数エラーの場合
            elif "int_parsing" in error_type:
                input_value = request.query_params.get("n", "unknown")
                error_message = (f"Bad request. Input 'n' must be a positive integer "
                                 f"(>= 1). Received: {input_value}")
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": status.HTTP_400_BAD_REQUEST, "message": error_message}
        )
    
    # 他のエンドポイントからのリクエストの場合はデフォルトのエラーレスポンスを返す
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

