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

### 設定ファイルの準備

`samconfig.toml` はリポジトリ管理外のため、サンプルをコピーして作成する。

```bash
cp samconfig.toml.example samconfig.toml
```

`samconfig.toml` を開き、各パラメータを自分の環境に合わせて編集する。

### デプロイ

```bash
# ビルド
uv run sam build

# 初回デプロイ（対話形式で設定）
uv run sam deploy --guided

# 2回目以降（samconfig.toml の設定を使用）
uv run sam deploy
```

### ローカル実行

```bash
uv run sam local invoke S3UploadHandlerFunction -e events/s3_event.json
```

## ファイル構成

```
template.yaml             # SAM テンプレート（Lambda + Lambda Permission）
samconfig.toml            # デプロイ設定（管理外・要作成）
samconfig.toml.example    # デプロイ設定サンプル
src/handler/
  lambda_function.py      # Lambda ハンドラー本体
  requirements.txt        # Python 依存ライブラリ
```
