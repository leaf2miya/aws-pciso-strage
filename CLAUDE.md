# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## コマンド

uv でプロジェクトの Python バージョン（3.12）を管理しているため、`sam` コマンドは `uv run` 経由で実行する。

```bash
# ビルド
uv run sam build

# デプロイ（samconfig.toml の設定を使用）
uv run sam deploy

# 初回デプロイ（S3バケットを自動作成）
uv run sam deploy --guided

# ローカル実行（テストイベントを使って Lambda を起動）
uv run sam local invoke S3UploadHandlerFunction -e events/s3_event.json
```

## アーキテクチャ

S3 にファイルをアップロードすると S3 イベント通知が Lambda を起動し、S3 キーのパス構造 `{company}/{soft}/{filename}` を分解して DynamoDB に保存する。

```
S3
  └── ObjectCreated イベント
        └── Lambda (S3UploadHandlerFunction)
              └── DynamoDB
                    ├── PK: company (String)
                    └── SK: soft (String)
```

## 既存リソースとの関係

SAM テンプレートは Lambda 関数と Lambda への S3 実行権限のみを管理する。S3 バケット・DynamoDB テーブルは既存リソースのため SAM スタック外で管理されており、**S3 バケットのイベント通知設定は AWS コンソールまたは CLI で手動設定が必要**。

### S3 イベント通知の手動設定手順

1. AWS コンソールで対象の S3 バケットを開く
2. プロパティ → イベント通知 → イベント通知を作成
3. イベントタイプ: `s3:ObjectCreated:*`
4. 送信先: Lambda 関数（デプロイした Lambda を指定）

## ファイル構成

```
template.yaml          # SAM テンプレート（Lambda + Lambda Permission）
samconfig.toml         # デプロイ設定（リージョン・スタック名など）
src/handler/
  lambda_function.py   # Lambda ハンドラー本体
  requirements.txt     # Python 依存ライブラリ
```
