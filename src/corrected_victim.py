from flask import Flask, request, session, redirect, url_for, render_template_string
import secrets

app = Flask(__name__)
app.secret_key = "supersecretkey"

# CSRFトークンを保存する辞書
csrf_tokens = {}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = "victim"
        return redirect(url_for("transfer"))
    
    return """
    <h2>ログインページ</h2>
    <form method="post">
        <input type="submit" value="ログイン">
    </form>
    """

@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if "user" not in session:
        return redirect(url_for("login"))

    # CSRFトークンの生成
    if "user" in session and session["user"] not in csrf_tokens:
        csrf_tokens[session["user"]] = secrets.token_hex(16)

    if request.method == "POST":
        token = request.form.get("csrf_token")
        if not token or token != csrf_tokens.get(session["user"]):
            return "<h2>CSRF攻撃を検出しました！</h2>", 403
        return "<h2>振込成功！（正規リクエスト）</h2>"

    return f"""
    <h2>銀行振込</h2>
    <form method="post">
        <input type="hidden" name="csrf_token" value="{csrf_tokens[session['user']]}">
        <input type="hidden" name="amount" value="100000">
        <input type="submit" value="送金">
    </form>
    """

if __name__ == "__main__":
    app.run(port=5000, debug=True)
