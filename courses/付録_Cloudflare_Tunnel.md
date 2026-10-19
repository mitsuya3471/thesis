# 付録：Cloudflare Tunnel で一時的に公開する

自分のPCで動かしているアプリに、外からアクセスできるURLを付けます。発表でデモを見せる、友人にスマートフォンから試してもらう、といったときに使います。アカウント登録は要りません。

```mermaid
flowchart LR
    U["外部の利用者<br/>スマートフォン・友人のPC"] --> C["公開URL<br/>https://～.trycloudflare.com"]
    C --> T["Cloudflare"]
    T --> L["自分のPCで動くアプリ<br/>localhost:8000"]
```

外からの通信は、いったん Cloudflare を通って、自分のPCのアプリに届きます。サーバを借りなくても公開できるのはこのためです。

## インストール

```powershell
winget install --id Cloudflare.cloudflared
```

PowerShellを開き直し、`cloudflared --version` でバージョンが表示されれば成功です。

## 公開する

まず、公開したいアプリを起動しておきます。たとえば、`index.html` のあるフォルダで次を実行すると、8000番でWebサーバが動きます。

```powershell
python -m http.server 8000
```

別のPowerShellを開き、そのポート番号を指定して実行します。

```powershell
cloudflared tunnel --url http://localhost:8000
```

表示の中に `https://～.trycloudflare.com` というURLが出ます。これをスマートフォンなどで開くと、自分のPCのアプリが表示されます。

ポート番号を変えれば、どのアプリでも同じように公開できます。Gradio なら、ふつうは7860番です。

```powershell
cloudflared tunnel --url http://localhost:7860
```

Colab で動かす方法は、[教材ノートブック](https://colab.research.google.com/github/mitsuya3471/thesis/blob/main/notebooks/gradio-cloudflared.ipynb) にあります。

## 止める

`cloudflared` を動かしているPowerShellで `Ctrl + C` を押します。止めるとURLは使えなくなります。

## 知っておくこと

- 起動するたびにURLが変わる。発表の直前に起動し、出たURLを配る
- PCを閉じたり `cloudflared` を止めたりすると、見られなくなる
- 同時に受け付けられるリクエストは200まで。テストやデモ用で、常時公開には使えない
- URLを知っている人は誰でもアクセスできる。パスワードや個人情報を入力させる画面は出さない
