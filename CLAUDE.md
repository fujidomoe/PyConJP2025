# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要
PyConJP2025は、クリーンアーキテクチャパターンに基づくPython Web APIプロジェクトです。Flask、MySQL、Auth0認証を採用し、TDD（テスト駆動開発）原則に従って開発されています。

## 開発コマンド

### ローカル開発
```bash
# Docker環境の起動
make docker/start

# テストの実行
make docker/test

# 単一テストファイルの実行
docker compose exec batch pytest src/tests/path/to/test_file.py -v

# 特定テスト関数の実行
docker compose exec batch pytest src/tests/path/to/test_file.py::TestClass::test_function -v
```


## アーキテクチャ構造

このプロジェクトはクリーンアーキテクチャに従い、以下の層構造を持ちます：

### ドメイン層 (src/domain/)
- **model/**: ドメインエンティティ（ビジネスロジックの中核）
- **repository/**: リポジトリインターフェース（データアクセスの抽象化）

### アプリケーション層 (src/application/)
- **usecase/**: ユースケース実装（ビジネスロジックのオーケストレーション）
- 各ユースケースは依存性注入によりリポジトリを受け取る

### インフラストラクチャ層 (src/infra/)
- **mysql/**: MySQLリポジトリ実装とSQLAlchemyモデル
- **auth0/**: Auth0認証クライアント実装

### プレゼンテーション層 (src/presentation/)
- **api/**: Flask REST APIエンドポイント
- 各エンドポイントはユースケースを呼び出す

## 重要な設計原則

### 依存性注入パターン
- Injectorライブラリを使用
- `src/di.py`でDIコンテナを構成
- テスト時はモックやスタブに差し替え可能

### 型安全性
- Pydanticモデルで入出力データを検証
- SQLAlchemyの型付きモデル
- MyPyによる静的型チェック

### テスト構造
- `src/tests/`配下にテストを配置
- `conftest.py`でpytest fixtureを定義
- トランザクションロールバックによるDB状態の分離

## 環境設定
- **APP_ENV**: Development | Staging | Production | Testing
- **DB_***: データベース接続設定
- **AUTH0_***: Auth0認証設定
- Docker Composeで3サービス（api, batch, db）を管理

## 開発時の注意事項
- 新機能はTDDサイクル（Red-Green-Refactor）に従って実装
- 各層の責務を厳守（ドメイン層は外部依存を持たない）
- リポジトリインターフェースを介したデータアクセス
- Ruffの150文字行制限を遵守
