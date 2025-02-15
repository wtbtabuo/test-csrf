# CSRF攻撃のデモ

このプロジェクトは、Cross-Site Request Forgery (CSRF) 攻撃の仕組みを理解し、対策の必要性を学ぶためのサンプルコードです。

## 構成

このデモには以下の2つの要素があります。

1. **被害者のサイト（Flaskアプリ）**: `http://localhost:5000`
   - ユーザーがログインし、送金ページへアクセス可能。
   - 初期状態ではCSRF対策がないため、攻撃が成功する。

2. **攻撃者のサイト（HTMLファイル）**: `http://localhost:8000`
   - 被害者がアクセスすると、意図しないリクエストが送信される。
   - CSRFトークンを導入後、この攻撃はブロックされる。

3. **修正済みの被害者のサイト（corrected_victim.py）**
   - `request` に CSRF トークンが含まれているか確認。
   - CSRF トークンがない場合、エラーを出すことで攻撃を防ぐ。

---

## セットアップと実行方法

### 1. **被害者のサイトを起動（Flaskアプリ）**

#### **仮想環境の作成とFlaskのインストール**
```bash
python3 -m venv venv
source venv/bin/activate  # Windowsの場合は venv\Scripts\activate
pip install flask
```

#### **Flaskアプリの実行**
```bash
python victim.py
```

成功すると、以下のようなメッセージが表示されます。
```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

ブラウザで `http://localhost:5000` にアクセスして、ログインを行います。

---

### 2. **攻撃者のサイトを起動（HTMLページ）**

#### **ローカルサーバーを起動**
攻撃者のサイトを提供するために、以下のコマンドで簡易HTTPサーバーを起動します。

```bash
python3 -m http.server 8000
```

ブラウザで `http://localhost:8000/attack.html` にアクセスすると、CSRF攻撃が実行されます。

---

## CSRF攻撃の流れ
1. **被害者が `http://localhost:5000` にアクセスし、ログインする**。
2. **ログイン状態のまま `http://localhost:8000/attack.html` にアクセス**。
3. **攻撃者のページが、ユーザーのセッションを利用して `/transfer` にリクエストを送信**。
4. **被害者のアカウントから意図しない送金が実行される（CSRF攻撃成功）**。

---

## CSRF対策の導入

CSRF対策として、以下の方法を `victim.py` および `corrected_victim.py` に追加しました。

1. **CSRFトークンの導入**
   - 各ユーザーごとにランダムなトークンを生成し、フォームに埋め込む。
   - `POST` リクエスト時にトークンの一致を確認。

2. **正当なフォームからのリクエストのみ許可**
   - `request.form.get("csrf_token")` をチェックし、不正なリクエストをブロック。

3. **`corrected_victim.py` では、CSRFトークンが含まれていない場合にエラーを出す機能を追加**
   - CSRF トークンがないリクエストはすべて拒否される。

---

## **対策後の動作確認**
1. **Flaskアプリ (`corrected_victim.py`) を修正後に再起動**
   ```bash
   python corrected_victim.py
   ```
2. **ブラウザで `http://localhost:5000` にアクセスし、ログイン後 `/transfer` に移動**
3. **送金ボタンを押すと、CSRFトークンが正しく送信されるため成功する**
4. **攻撃者のページ (`http://localhost:8000/attack.html`) にアクセスすると 403 Forbidden となり、攻撃が失敗する**

---

## まとめ
- **CSRF攻撃は、罠サイトを利用して被害者のセッションでリクエストを送信させる手法。**
- **CSRF対策として、CSRFトークンの導入が効果的。**
- **`corrected_victim.py` を使用すると、CSRFトークンがないリクエストはすべてブロックされ、攻撃が防止される。**

このプロジェクトを通じて、CSRFの仕組みと防御策を学ぶことができます！ 🚀

