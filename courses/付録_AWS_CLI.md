# 付録：AWS CLI（aws）

`aws` を使うと、EC2 などの AWS の操作をターミナルやエージェントから行えます。ログインの仕組みは [付録：ブラウザでのログインとトークン](付録_ブラウザでのログインとトークン.md) にあります。

## インストール

インストールは次の1行です。管理者の権限は要りません。

```powershell
irm https://awscli.amazonaws.com/v2/install.ps1 | iex
```

PowerShellを開き直し、`aws --version` でバージョンが表示されれば成功です。

`irm` はURLの中身をダウンロードするコマンド、`iex` は受け取った文字列をそのまま実行するコマンドです。AWSが配布しているインストール用のスクリプトを、ダウンロードして実行しています。

## IAMユーザーを作る

`aws login` には、ルートユーザー（AWSに登録したときのメールアドレス）ではなく、IAMユーザーでログインします。ルートユーザーは何でもできてしまうので、普段の作業には使いません。

AWSのコンソールで、ルートユーザーとしてログインして作ります。検索欄に `IAM` と入れて開き、左のメニューの「ユーザー」から「ユーザーの作成」を押します。

ユーザーの詳細を指定します。

1. ユーザー名を入れる
2. 「AWS マネジメントコンソールへのユーザーアクセスを提供する」にチェックを入れる
3. 「IAM ユーザーを作成します」を選ぶ。パスワードは自動生成のままでよい

![ユーザーの詳細を指定する](../images/aws_iam_user_details.png)

次へ進み、許可を設定します。

1. 「ポリシーを直接アタッチする」を選ぶ
2. 検索欄にポリシー名を入れる
3. 出てきたポリシーにチェックを入れる

![許可を設定する](../images/aws_iam_permissions.png)

チェックを入れるポリシーは2つです。1つ選んだら、検索し直してもう1つ選びます。

- `SignInLocalDevelopmentAccess`（`aws login` に必要）
- 使うサービスのポリシー。EC2なら `AmazonEC2FullAccess`

確認画面で、選んだポリシーが並んでいることを確かめて「ユーザーの作成」を押します。`IAMUserChangePassword` は、初回ログインでパスワードを変えるために自動で付きます。

![確認して作成する](../images/aws_iam_review.png)

最後の画面に、コンソールのサインインURLとパスワードが表示されるので控えます。

以降は、控えたURLを開いてIAMユーザーでログインします。

## ログインする

`aws login` を実行するとブラウザが開き、AWSのコンソールと同じ画面でログインします。初めてのときはリージョンを聞かれるので、東京なら `ap-northeast-1` と入れます。

```{ .console .terminal }
> aws login
AWS Region [us-east-1]: ap-northeast-1          ← 初回だけ聞かれる
Attempting to open the login page for `ap-northeast-1` in your default browser.
                                                 ← ブラウザでログインして、ターミナルに戻る
> aws sts get-caller-identity                    ← ログインできたか確かめる
{
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/yamada"
}
> aws ec2 describe-instances                     ← 以降は普通に使える
> aws logout                                     ← 使い終わったら消す
```

- AWS CLI のバージョン 2.32.0 以降が必要です
- IAMユーザでログインする場合は、そのユーザに `SignInLocalDevelopmentAccess` というポリシーを付けておきます

## 監査用のIAMユーザーを作る

教員が構成と料金を確かめられるように、読み取り専用のIAMユーザーを作ります。手順は「IAMユーザーを作る」と同じで、付けるポリシーだけが違います。

| ポリシー | 目的 |
| --- | --- |
| `ReadOnlyAccess` | 設定を見る。変更や削除はできない |
| `AWSBillingReadOnlyAccess` | 料金と請求を見る |
| `SignInLocalDevelopmentAccess` | `aws login` で使う |

料金を見せるには、ルートユーザーで右上のアカウント名から「アカウント」を開き、「IAM ユーザーおよびロールによる請求情報へのアクセス」を有効にします。

作成後に表示されるサインインURL・ユーザー名・パスワードは、Classroomの限定公開コメントで教員に送ります。リポジトリやグループのチャットには書きません。制作が終わったら、このユーザーを削除します。
