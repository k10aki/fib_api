# Fibonacci API

フィボナッチ数列のn番目の数を返すRESTAPIサービス。

## 概要

この API は指定されたインデックス n のフィボナッチ数を計算して返します。フィボナッチ数列は、最初の2項が1で、それ以降の各項がその直前の2項の和として定義される数列です。

例: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

## 技術スタック

- Python
- FastAPI
- pytest

## プロジェクト構成

```
fib_api/
├── .gitignore
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── custom_handlers.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── fibonacci.py
│   └── services/
│       ├── __init__.py
│       └── calculate_fibonacci.py
└── tests/
    ├── __init__.py
    └── test_api.py
```

### コンポーネントの説明

- **main.py**: アプリケーションのエントリーポイント。FastAPIアプリケーションの設定と起動を担当。
- **exceptions/**: カスタム例外とエラーハンドラーを定義。
  - **custom_handlers.py**: エラーハンドラー関数で、課題仕様に沿ったエラーレスポンス形式を返す。
- **routers/**: APIエンドポイントの定義。
  - **fibonacci.py**: フィボナッチ数列のAPIエンドポイントとパラメータ検証ロジック。
- **services/**: ビジネスロジックの実装。
  - **calculate_fibonacci.py**: フィボナッチ数列の計算ロジック。
- **tests/**: テストコード。
  - **test_api.py**: APIのエンドポイントと機能のテスト。

## インストールと実行方法

### 必要条件

- Python 3.8以上

### セットアップ

1. リポジトリをクローン
   ```
   # HTTPSの場合
   git clone https://github.com/k10aki/fib_api.git

   # SSHの場合
   git clone git@github.com:k10aki/fib_api.git

   cd fib_api
   ```

2. 仮想環境を作成して有効化
   ```
   python -m venv fibapi_env
   source fibapi_env/bin/activate  # Linuxの場合
   fibapi_env\Scripts\activate     # Windowsの場合
   ```

3. 依存関係のインストール
   ```
   pip install -r requirements.txt
   ```

### ローカルでのサーバーの起動例

```
uvicorn app.main:app --reload
```

## ローカルでのAPIの使い方

### フィボナッチ数の取得

**エンドポイント**: GET /fib

**クエリパラメータ**:
- `n` (整数): 取得したいフィボナッチ数列のインデックス (n >= 1)

**成功レスポンス**:
- ステータスコード: 200 OK
- レスポンス本文: `{"result": フィボナッチ数}`

**エラーレスポンス**:
- ステータスコード: 400 Bad Request または 422 Unprocessable Entity
- レスポンス本文: `{"status": ステータスコード, "message": "エラーメッセージ"}`

### 使用例

```bash
# 10番目のフィボナッチ数を取得
curl -X GET -H "Content-Type: application/json" "http://localhost:8000/fib?n=10"

# レスポンス
{"result": 55}
```

```bash
# 99番目のフィボナッチ数を取得
curl -X GET -H "Content-Type: application/json" "http://localhost:8000/fib?n=99"

# レスポンス
{"result": 218922995834555169026}
```

### エラー例

```bash
# パラメータなし
curl -X GET  -H "Content-Type: application/json" "http://localhost:8000/fib"

# レスポンス
{"status": 400, "message": "Bad request. Query parameter 'n' (positive integer) is required."}
```

```bash
# 無効なパラメータ
curl -X GET -H "Content-Type: application/json" "http://localhost:8000/fib?n=abc"

# レスポンス
{"status": 422, "message": "Bad request. Input 'n' must be a positive integer (>= 1). Received: abc"}
```

```bash
# 数値が範囲外（負の値）
curl -X GET -H "Content-Type: application/json" "http://localhost:8000/fib?n=-5"

# レスポンス
{"status": 422, "message": "Bad request. Input 'n' must be a positive integer (>= 1). Received: -5"}
```

```bash
# 整数以外の値
curl -X GET -H "Content-Type: application/json" "http://localhost:8000/fib?n=3.14"

# レスポンス
{"status": 422, "message": "Bad request. Input 'n' must be a positive integer (>= 1). Received: 3.14"}
```

## テスト実行

テストを実行するには:
```
pytest -v
```

テスト内容:
- ルートエンドポイントのテスト
- 有効な入力値でのフィボナッチAPIテスト
- パラメータなしの場合のテスト
- 文字列が渡された時のテスト
- 負の値のテスト
- 0が渡された時のテスト
- 整数以外の値が渡された時のテスト
- 大きな数値のテスト
- calculate_fibonacci関数の単体テスト

## 実装上の特徴

- **パフォーマンス最適化**: フィボナッチ数の計算において反復処理を使用し、再帰呼び出しによるパフォーマンス低下を防止。
- **エラー処理**: カスタムエラーハンドラーを使用して、課題に即したエラーレスポンスを提供。
- **バリデーション**: リクエストパラメータに対するバリデーションを実装。
- **保守性と変更容易性**: サービス層、ルーティング層、エラー処理層を分離。
- **テスト**: ユニットテストにより、APIの正常動作と様々なエラー条件の処理を検証。