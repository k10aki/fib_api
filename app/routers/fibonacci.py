from fastapi import APIRouter, Query, HTTPException, status

from app.services.calculate_fibonacci import calculate_fibonacci

# ルーターの作成
router = APIRouter(
    prefix="/fib",
    tags=["fibonacci"]
)


@router.get("")
async def get_fibonacci(
    n: int = Query(
        ...,
        ge=1,
        description="The index 'n' of the Fibonacci number (must be >= 1)"
    )
):
    """
    n番目のフィボナッチ数を計算するAPIエンドポイント
    """
    try:
        result = calculate_fibonacci(n)
    except Exception as e:
        print(f"Error during Fibonacci calculation for n={n}: {e}")
        # 内部エラーは500を返す
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Internal server error during calculation."}
        )

    # 正常レスポンス
    return {"result": result}
