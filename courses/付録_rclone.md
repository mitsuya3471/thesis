# 付録：Googleドライブを操作する（rclone）

`rclone` を使うと、Googleドライブのファイルの一覧・アップロード・ダウンロードをターミナルやエージェントから行えます。ログインの仕組みは [付録：ブラウザでのログインとトークン](付録_ブラウザでのログインとトークン.md) にあります。

## セットアップ

```powershell
winget install Rclone.Rclone
rclone config
```

`rclone config` を実行すると、次のように聞かれます。入力する箇所だけ示します。

```{ .console .terminal }
e) Edit existing remote
n) New remote
d) Delete remote
q) Quit config
e/n/d/q> n                      ← 新しい接続を作る

Enter name for new remote.
name> gdrive                    ← 好きな名前

Option Storage.
Type of storage to configure.
 1 / 1Fichier
   \ (fichier)
   （…50件以上並ぶので、Google Drive の番号を探す…）
24 / Google Drive
   \ (drive)
Storage> drive                  ← 番号でも名前でも可

Option client_id.
Google Application Client Id
Enter a value. Press Enter to leave empty.
client_id>                      ← 何も入れずEnter

Option client_secret.
client_secret>                  ← 何も入れずEnter

Option scope.
 1 / Full access all files, excluding Application Data Folder.
   \ (drive)
 2 / Read-only access to file metadata and file contents.
   \ (drive.readonly)
scope> 1                        ← 読み書きしたいので1

Option service_account_file.
service_account_file>           ← 何も入れずEnter

Edit advanced config?
y/n> n

Use web browser to automatically authenticate rclone with remote?
y/n> y                          ← ブラウザが開く
```

最後にブラウザが開くので、自分のGoogleアカウントで許可します。以降は認証なしで使えます。

## 使い方

使い方の例です。

```powershell
rclone ls gdrive:                              # ファイルの一覧
rclone copy 計画書.docx gdrive:                 # アップロード
rclone copy gdrive:週次報告書（回答）.xlsx .      # ダウンロード
rclone cat gdrive:メモ.txt                      # 中身を表示
```

`.txt` や `.docx` をアップロードするとき、次を付けるとGoogleドキュメントに変換されます。

```powershell
rclone copy 計画書.txt gdrive: --drive-import-formats txt --drive-export-formats txt
```

## 接続を解除する

使い終わったら接続を解除します。学校のPCは共用で、許可した情報は `%APPDATA%\rclone\rclone.conf` に残ります。そのままにすると、次に使う人が自分のGoogleドライブを操作できてしまいます。

```powershell
rclone config disconnect gdrive:    # Google側の許可を取り消す
rclone config delete gdrive         # 設定そのものを消す
```

自分のPCなら、残しておいて構いません。
