# 開発ルール

## 環境構築
- `uv init` でプロジェクトを初期化し、依存関係は `uv add` で管理する
- `uv` でpythonバージョンを固定し管理する

## テスト
- テストフレームワークは `pytest` を使用する（`unittest` は使わない）
- dev 依存に `uv add --dev pytest` で追加する

## ワークフロー
1. GitHub Issue を発行する
2. feature ブランチで修正・テストを実装する
  featureブランチはmainから作成する。作成前にmainを最新化すること。
3. テストがすべてパスしたら PR を作成する
4. ユーザーが確認・マージする

## Git
### ブランチ名
- 機能改修ブランチの場合はfeature_"issue No" とする
  - ex: feature_1
- 障害修正ブランチの場合はfixup_"issue Noとする
  - ex: fixup_1
### コミットメッセージ
- 1行のサマリのみ記載する（本文・箇条書き不要）
- 例: `feat: pytest によるユニットテストを追加 (closes #1)`
