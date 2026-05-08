# aws-pciso-strage

S3 にファイルをアップロードすると S3 イベント通知が Lambda を起動し、S3 キーのパス構造 `{company}/{soft}/{filename}` を分解して DynamoDB に保存する SAM アプリケーション。

## アーキテクチャ

```
S3
  └── ObjectCreated イベント
        └── Lambda
              └── DynamoDB
                    ├── PK: company (String)
                    └── SK: soft (String)
```

## 既存リソースとの関係

SAM テンプレートは Lambda 関数と Lambda への S3 実行権限のみを管理する。S3 バケット・DynamoDB テーブルは既存リソースのため SAM スタック外で管理されており、**S3 バケットのイベント通知設定は AWS コンソールまたは CLI で手動設定が必要**。

### S3 イベント通知の手動設定

1. AWS コンソールで対象の S3 バケットを開く
2. プロパティ → イベント通知 → イベント通知を作成
3. イベントタイプ: `s3:ObjectCreated:*`
4. 送信先: Lambda 関数（デプロイした Lambda を指定）

## セットアップ

### 前提条件

- [uv](https://docs.astral.sh/uv/)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- AWS CLI（認証済み）

### SSM パラメータの登録

デプロイ前に AWS Systems Manager → Parameter Store で以下のパラメータを登録すること（タイプ: **String**）。

| パラメータパス | 説明 |
|---|---|
| `/pciso-strage/prd/s3-bucket-name` | prd 環境の S3 バケット名 |
| `/pciso-strage/prd/dynamodb-table-name` | prd 環境の DynamoDB テーブル名 |
| `/pciso-strage/prd/lambda-role-arn` | prd 環境の Lambda 実行ロール ARN |
| `/pciso-strage/dev/s3-bucket-name` | dev 環境の S3 バケット名 |
| `/pciso-strage/dev/dynamodb-table-name` | dev 環境の DynamoDB テーブル名 |
| `/pciso-strage/dev/lambda-role-arn` | dev 環境の Lambda 実行ロール ARN |

### IAM 権限

`sam deploy` を実行する IAM ユーザー/ロールに以下の権限が必要。

| 権限 | 対象リソース |
|---|---|
| `ssm:GetParameters` | `/pciso-strage/*` 配下のパラメータ |

### デプロイ

```bash
# ビルド
uv run sam build

# 本番環境へデプロイ
uv run sam deploy --config-env prd

# 開発環境へデプロイ
uv run sam deploy --config-env dev
```

### ローカル実行

```bash
uv run sam local invoke S3UploadHandlerFunction -e events/s3_event.json
```

## ファイル構成

```
template.yaml          # SAM テンプレート（Lambda + Lambda Permission）
samconfig.toml         # デプロイ設定（prd/dev プロファイル）
src/handler/
  lambda_function.py   # Lambda ハンドラー本体
  requirements.txt     # Python 依存ライブラリ
```
