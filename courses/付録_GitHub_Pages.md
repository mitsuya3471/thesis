# 付録：GitHub Pages で公開する

HTML・CSS・JavaScript でできたページを、GitHubから無料で公開します。この教材のサイトも GitHub Pages で公開しています。

PHP やデータベースのように、サーバ側で処理が動くものは公開できません。その場合は AWS EC2 に Apache を立てます。

```mermaid
flowchart LR
    L["手元のフォルダ<br/>index.html など"] -- "git push" --> R["GitHubの公開リポジトリ"]
    R -- "自動で公開" --> W["https://ユーザー名.github.io/リポジトリ名/"]
```

## 公開用のリポジトリを分ける

無料のアカウントでは、公開リポジトリからしか GitHub Pages を使えません。制作中のリポジトリは非公開のままにして、公開するページだけを入れるリポジトリを別に作ります。

公開リポジトリは誰でも中身を見られます。パスワードやAPIキーを入れないでください。

## ブラウザで公開する

1. 公開（Public）のリポジトリを作り、`index.html` を置いてプッシュする
2. リポジトリの Settings を開き、左のメニューから Pages を選ぶ
3. Build and deployment の Source を「Deploy from a branch」にする
4. ブランチを `main`、フォルダを `/ (root)` にして Save を押す

数分たつと、`https://ユーザー名.github.io/リポジトリ名/` で見られるようになります。

## コマンドで公開する

公開したいファイルのあるフォルダで、次を実行します。`gh` の準備は [付録：ターミナルで操作する](付録_ターミナルで操作する.md) にあります。

```powershell
git init
git add .
git commit -m "公開するページ"
gh repo create mysite --public --source=. --remote=origin --push
gh api -X POST repos/{owner}/{repo}/pages -f "source[branch]=main" -f "source[path]=/"
```

最後の行が、ブラウザの手順2〜4にあたります。

エージェントに頼むなら、次のように伝えます。

```
このフォルダの内容を、GitHub の公開リポジトリ mysite に置いて、GitHub Pages で公開してください。
```

## 更新する

ファイルを直して `git push` すれば、数分で公開中のページにも反映されます。
