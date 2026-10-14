# 付録：Apacheの設定

[サーバの構築と公開](サーバの構築と公開.md) のWebサーバの節で使う、Apacheのインストールと設定の手順です。

## インストール

Ubuntuの場合、以下のコマンドでApacheをインストールできます。

```bash
sudo apt update
sudo apt install apache2
```

## 設定ファイル

### ドキュメントルート

作成したHTMLファイルはApacheのドキュメントルートに配置する必要があります。通常は`/var/www/html`がドキュメントルートとして設定されています。

### sites-available/ フォルダ

`/etc/apache2/sites-available/`は、Apacheの設定ファイルが格納されているディレクトリです。

`000-default.conf`は、デフォルトの設定ファイルです。このファイルの中で、ドキュメントルートやポート番号などの設定を行います。

`default-ssl.conf`は、HTTPS（SSL/TLS）を利用する場合の設定ファイルです。ここにSSL証明書のパスやポート番号などを設定します。

## 設定の反映・再起動

設定ファイルを変更した場合、設定の反映とApacheの再起動が必要です。

```bash
sudo a2ensite <設定ファイル名> # 設定の有効化
sudo systemctl reload apache2 # 設定の反映
```

設定ファイルは、`sites-available`（設定を置く場所）に作り、`a2ensite` で `sites-enabled`（実際に使われる場所）へ有効化する、という二段構えになっています。設定を書いただけでは反映されない点に注意してください。

```mermaid
flowchart LR
    A["sites-available/<br/>設定ファイルを置く"] -- "sudo a2ensite" --> B["sites-enabled/<br/>有効になった設定"]
    B -- "sudo systemctl reload apache2" --> C["Apacheが新しい設定で動く"]
```
