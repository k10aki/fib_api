def calculate_fibonacci(n: int) -> int:
    """
    n番目のフィボナッチ数を計算する関数。
    再帰関数による実装だと、同じ計算を何度も行うため、動作に影響が出る。
    そのため、メモ化を行う。

    Args:
        n (int): フィボナッチ数列のインデックス
        ここでは、n >= 1であることを想定する。
        呼び出し元(API側)でn<=0の場合はエラーを返すようチェックする。

    Returns:
        int: n番目のフィボナッチ数
    """

    if n == 1 or n == 2:
        return 1

    a, b = 1, 1

    for _ in range(n-2):
        a, b = b, a + b

    # ループが終了した時点で、b にn番目のフィボナッチ数が格納されている
    return b
