from fastapi import APIRouter, Query
from fastapi.exceptions import RequestValidationError
from typing import Annotated

from app.calculate_fibonacci import calculate_fibonacci
from app.exceptions.handlers_fibonacci import validation_exception_handler


router = APIRouter(
    prefix="/fib",  # このルーターのパスプレフィックス
    tags=["fibonacci"]  # ドキュメント用のタグ
)


@router.get("")
async def get_fibonacci(
    n: Annotated[int, Query(ge=1, description="The index 'n' of the Fibonacci number (must be >= 1)")]
):
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
    result = calculate_fibonacci(n)
    return {"result": result}
