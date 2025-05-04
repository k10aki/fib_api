class FibonacciParameterError(Exception):
    """フィボナッチエンドポイント用の入力パラメータバリデーションエラー"""
    def __init__(self, message="Bad request."):
        self.message = message
        super().__init__(self.message)
