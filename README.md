# TODO 管理アプリケーション

フロントエンド（Vue.js）とバックエンド（Django）を使用したタスク管理アプリケーションです。

## 機能

- タスクの追加、編集、削除
- タスクのカテゴリ/タグ管理
- タスクの優先度設定
- 繰り返しタスク
- フィルタリングと検索
- ドラッグ＆ドロップでの並べ替え（実装予定）

## 技術スタック

- フロントエンド: Vue.js, Tailwind CSS
- バックエンド: Django, Django REST Framework
- データベース: SQLite（開発環境）

## セットアップ手順

### バックエンド

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
