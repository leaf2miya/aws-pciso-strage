# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 制限
- 秘密情報を決してGit管理下に置かないこと

## コマンド

uv でプロジェクトの Python バージョン（3.12）を管理しているため、`sam` コマンドは `uv run` 経由で実行する。
`uv init` でプロジェクトを初期化済み（`pyproject.toml` / `uv.lock` が存在）。

```bash
# ビルド
uv run sam build

# デプロイ（本番環境）
uv run sam deploy --config-env prd

# デプロイ（開発環境）
uv run sam deploy --config-env dev

# ローカル実行（テストイベントを使って Lambda を起動）
uv run sam local invoke S3UploadHandlerFunction -e events/s3_event.json

# テスト実行
uv run pytest tests/ -v
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

## SSM パラメータ

デプロイ前に AWS Systems Manager → Parameter Store で以下のパラメータを SecureString で登録すること。

| パラメータパス | 説明 |
|---|---|
| `/aws-pciso-strage/prd/s3-bucket-name` | prd 環境の S3 バケット名 |
| `/aws-pciso-strage/prd/dynamodb-table-name` | prd 環境の DynamoDB テーブル名 |
| `/aws-pciso-strage/prd/lambda-role-arn` | prd 環境の Lambda 実行ロール ARN |
| `/aws-pciso-strage/dev/s3-bucket-name` | dev 環境の S3 バケット名 |
| `/aws-pciso-strage/dev/dynamodb-table-name` | dev 環境の DynamoDB テーブル名 |
| `/aws-pciso-strage/dev/lambda-role-arn` | dev 環境の Lambda 実行ロール ARN |

`sam deploy` 実行 IAM ユーザー/ロールには `ssm:GetParameters` および SecureString 復号用の `kms:Decrypt` 権限が必要。

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
samconfig.toml         # デプロイ設定（prd/dev プロファイル）
pyproject.toml         # uv プロジェクト設定（dev 依存: pytest, boto3）
src/handler/
  lambda_function.py   # Lambda ハンドラー本体
  requirements.txt     # Python 依存ライブラリ（Lambda 実行環境用）
tests/
  test_lambda_function.py  # ユニットテスト
```
