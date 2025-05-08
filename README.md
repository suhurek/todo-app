# TODO 管理アプリケーション

フロントエンド（Vue.js）とバックエンド（Django REST Framework）を使用した完全なタスク管理アプリケーションです。

## 機能

- タスクの追加、編集、削除
- タスクの完了状態の切り替え
- タスクの詳細説明
- タスクのカテゴリ/タグ管理（実装予定）
- タスクの優先度設定（実装予定）
- 繰り返しタスク（実装予定）
- フィルタリングと検索（実装予定）
- ドラッグ＆ドロップでの並べ替え（実装予定）

## 技術スタック

### フロントエンド

- Vue.js 3
- Axios（API リクエスト）
- Tailwind CSS（スタイリング）

### バックエンド

- Django 4.x
- Django REST Framework（API 構築）
- SQLite（開発環境）

## セットアップ手順

### 前提条件

- Python 3.8 以上
- Node.js 16 以上
- npm または yarn

### バックエンド

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/todo-app.git
cd todo-app

# バックエンドの設定
cd backend
python -m venv venv
source venv/bin/activate  # Linuxの場合
# または
venv\Scripts\activate     # Windowsの場合

# 依存関係のインストール
pip install -r requirements.txt

# データベースのセットアップ
python manage.py migrate

# 開発サーバーの起動
python manage.py runserver
```

### フロントエンド

```bash
# 別のターミナルで
cd todo-app/frontend

# 依存関係のインストール
npm install
# または
yarn install

# 開発サーバーの起動
npm run serve
# または
yarn serve
```

アプリケーションは以下の URL でアクセスできます：

- フロントエンド: http://localhost:8080
- バックエンド API: http://localhost:8000/api/

## API エンドポイント

| エンドポイント    | メソッド | 説明               |
| ----------------- | -------- | ------------------ |
| `/api/tasks/`     | GET      | タスク一覧の取得   |
| `/api/tasks/`     | POST     | 新しいタスクの作成 |
| `/api/tasks/:id/` | GET      | 特定のタスクの取得 |
| `/api/tasks/:id/` | PUT      | タスクの更新       |
| `/api/tasks/:id/` | DELETE   | タスクの削除       |

## 開発ガイド

### バックエンド開発

- モデルの定義は `backend/todos/models.py` にあります
- API ビューは `backend/todos/views.py` で定義されています
- シリアライザは `backend/todos/serializers.py` にあります

### フロントエンド開発

- Vue コンポーネントは `frontend/src/components` にあります
- API サービスは `frontend/src/services` で定義されています
- ルーティングは `frontend/src/router` で設定されています

## ライセンス

MIT

## 貢献方法

1. リポジトリをフォークする
2. 機能ブランチを作成する (`git checkout -b feature/amazing-feature`)
3. 変更をコミットする (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュする (`git push origin feature/amazing-feature`)
5. プルリクエストを作成する
