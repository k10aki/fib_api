from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Union

from app.services.calculate_fibonacci import calculate_fibonacci
from app.exceptions.custom_exceptions import FibonacciParameterError

# ルーターの作成
router = APIRouter(
    prefix="/fib",
    tags=["fibonacci"]
)


def validate_fibonacci_n(
    n_str: Union[str, None] = Query(None, alias="n", description="The index 'n' of the Fibonacci number (must be >= 1)")
) -> int:
    """
    フィボナッチ数列のインデックス 'n' を検証する依存関数
    カスタム例外FibonacciParameterErrorを使用して、フィボナッチエンドポイント用のエラー処理を行う
    Args:
        n_str (str): フィボナッチ数列のインデックス
        適切な入力かチェックするために、str型で受け取る
    Returns:
        int: フィボナッチ数列のインデックス
    """

    # 入力なしチェック
    if n_str is None:
        print("Validation Error: 'n' is missing.")
        raise FibonacciParameterError(
            "Bad request. Query parameter 'n' (positive integer) is required.")

    # 整数変換チェック
    try:
        n_int = int(n_str)
    except ValueError:
        print(f"Validation Error: 'n' ({n_str}) is not a valid integer.")
        raise FibonacciParameterError(
            f"Bad request. Input 'n' must be a positive integer (>= 1). Received: {n_str}")

    # 範囲チェック
    if n_int < 1:
        print(f"Validation Error: 'n' ({n_int}) is not positive.")
        raise FibonacciParameterError(
            f"Bad request. Input 'n' must be a positive integer (>= 1). Received: {n_str}")

    return n_int


@router.get("")
async def get_fibonacci(n: int = Depends(validate_fibonacci_n)):
    """
    n番目のフィボナッチ数を計算するAPIエンドポイント
    """
    try:
        result = calculate_fibonacci(n)
    except Exception as e:
        print(f"Error during Fibonacci calculation for n={n}: {e}")
        # 内部エラーは500を返す
        # これはフィボナッチAPI専用のエラーではないため、標準のHTTPExceptionを使用
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "Internal server error during calculation."}
        )

    # 正常レスポンス
    return {"result": result}
