# 付録：three.js で立体を動かす

three.js は、ブラウザで3Dの図形を描いて動かすためのライブラリです。スロットのリールのように、円筒が回って止まる動きを作れます。

「回す」を押してみてください。

<iframe src="../demo/threejs_reel.html" width="100%" height="420" style="border:0" loading="lazy"></iframe>

このデモのファイルは [threejs_reel.html](demo/threejs_reel.html) です。

## 読み込む

CDN から読み込むので、Node.js のインストールは要りません。HTML の `<head>` に次を書きます。

```html
<script type="importmap">
  { "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.module.js" } }
</script>
```

使う側の `<script>` には `type="module"` を付け、`import * as THREE from "three";` で読み込みます。

## 5つの考え方

three.js のコードは、次の5つでできています。

| 考え方 | コード | 役割 |
| --- | --- | --- |
| シーン | `new THREE.Scene()` | 物を置く空間 |
| カメラ | `new THREE.PerspectiveCamera(...)` | どこから見るか |
| レンダラー | `new THREE.WebGLRenderer(...)` | カメラから見た様子を `<canvas>` に描く |
| メッシュ | `new THREE.Mesh(geometry, material)` | 形（ジオメトリ）と材質（マテリアル）を組み合わせた物 |
| アニメーションループ | `renderer.setAnimationLoop(...)` | 毎フレーム呼ばれる。角度を変えて描き直す |

デモでは、形は円筒（`CylinderGeometry`）で、材質には絵柄を描いた画像を貼っています。

