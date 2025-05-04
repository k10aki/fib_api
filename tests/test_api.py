from fastapi.testclient import TestClient

from app.main import app
from app.services.calculate_fibonacci import calculate_fibonacci

client = TestClient(app)


class TestFibonacciAPI:
    def test_read_root(self):
        """
        ルートエンドポイントのテスト
        """
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Fibonacci API! See /docs for API documentation."}
    
    def test_fibonacci_valid_input(self):
        """有効な入力値でのフィボナッチAPIテスト"""
        # 既知のフィボナッチ数列の値をテスト
        test_cases = [
            (1, 1),  # 1番目は1
            (2, 1),  # 2番目は1
            (3, 2),  # 3番目は2
            (4, 3),  # 4番目は3
            (5, 5),  # 5番目は5
            (10, 55),  # 10番目は55
        ]

        for n, expected in test_cases:
            response = client.get(f"/fib?n={n}")
            assert response.status_code == 200
            assert response.json() == {"result": expected}
    
    def test_fibonacci_missing_parameter(self):
        """パラメータなしの場合のテスト"""
        response = client.get("/fib")
        assert response.status_code == 400
        assert response.json() == {
            "status": 400,
            "message": "Bad request. Query parameter 'n' (positive integer) is required."
        }
    
    def test_fibonacci_invalid_parameter_type(self):
        """文字列が渡された時のテスト"""
        response = client.get("/fib?n=abc")
        assert response.status_code == 400
        assert response.json() == {
            "status": 400,
            "message": "Bad request. Input 'n' must be a positive integer (>= 1). Received: abc"
        }

    def test_fibonacci_negative_parameter(self):
        """負の値のテスト"""
        response = client.get("/fib?n=-5")
        assert response.status_code == 400
        assert response.json() == {
            "status": 400,
            "message": "Bad request. Input 'n' must be a positive integer (>= 1). Received: -5"
        }

    def test_fibonacci_zero_parameter(self):
        """0が渡された時のテスト"""
        response = client.get("/fib?n=0")
        assert response.status_code == 400
        assert response.json() == {
            "status": 400,
            "message": "Bad request. Input 'n' must be a positive integer (>= 1). Received: 0"
        }
    
    def test_fibonacci_not_int_number(self):
        """整数以外の値が渡された時のテスト"""
        response = client.get("/fib?n=3.14")
        assert response.status_code == 400
        assert response.json() == {
            "status": 400,
            "message": "Bad request. Input 'n' must be a positive integer (>= 1). Received: 3.14"
        }

    def test_fibonacci_large_number(self):
        """大きな数値のテスト"""
        n = 99
        expected = 218922995834555169026
        response = client.get(f"/fib?n={n}")
        assert response.status_code == 200
        assert response.json() == {"result": expected}

    def test_calculate_fibonacci_function(self):
        """calculate_fibonacci関数の単体テスト"""
        assert calculate_fibonacci(1) == 1
        assert calculate_fibonacci(2) == 1
        assert calculate_fibonacci(3) == 2
        assert calculate_fibonacci(4) == 3
        assert calculate_fibonacci(5) == 5
        assert calculate_fibonacci(10) == 55
    



