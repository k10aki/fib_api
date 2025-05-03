from fastapi import APIRouter, Query, Depends, HTTPException, status
from typing import Union
from fastapi.responses import JSONResponse

from app.calculate_fibonacci import calculate_fibonacci


router = APIRouter(
    prefix="/fib",  # このルーターのパスプレフィックス
    tags=["fibonacci"]  # ドキュメント用のタグ
)


# n の取得、検証、変換を行う
def validate_n(
    n_str: Union[str, None] = Query(None, alias="n", description="The index 'n' of the Fibonacci number (must be >= 1)")
) -> Union[int, JSONResponse]: 
    """
    クエリパラメータ 'n' を検証し、有効な場合は整数として返す依存関数。
    無効な場合は HTTP 400 エラーを発生させる。
    """
    # 1. 入力なしチェック
    if n_str is None:
        print("Validation Error: 'n' is missing.") 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": status.HTTP_400_BAD_REQUEST,
                    "message": "Bad request. Query parameter 'n' (int : >=1) is required."}
        )

    # 2. 整数変換チェック (文字列、小数を弾く)
    try:
        n_int = int(n_str)
    except ValueError:
        print(f"Validation Error: 'n' ({n_str}) is not a valid integer.") 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": status.HTTP_400_BAD_REQUEST,
                    "message": f"Bad request. Input 'n' must be an integer (>= 1). Received: '{n_str}'"} # 少し詳細なメッセージ
        )

    # 3. 範囲チェック (1以上か)
    if n_int < 1:
        print(f"Validation Error: 'n' ({n_int}) is not positive.") # ログ
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": status.HTTP_400_BAD_REQUEST,
                    "message": f"Bad request. Input 'n' must be a positive integer (>= 1). Received: {n_int}"}
        )

    # すべてのチェックをパスしたら、検証済みの整数値を返す
    return n_int


@router.get("")
async def get_fibonacci(
    n: int = Depends(validate_n)  # validate_n関数を依存関数として使用: 
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
    try:
        result = calculate_fibonacci(n)
    except Exception as e:
        # 計算中の内部エラーは 500 を返す
        print(f"Error during Fibonacci calculation for n={n}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Internal server error during calculation."}
        )

    # 正常レスポンス
    return {"result": result}
