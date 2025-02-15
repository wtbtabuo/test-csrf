from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "supersecretkey"  # セッション管理のため

# 簡単なログイン機能
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = "victim"  # ログイン状態を作成
        return redirect(url_for("transfer"))
    
    return """
    <h2>ログインページ</h2>
    <form method="post">
        <input type="submit" value="ログイン">
    </form>
    """

# 銀行振込のページ（脆弱）
@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        return "<h2>振込成功！（CSRF攻撃されたかも？）</h2>"

    return """
    <h2>銀行振込</h2>
    <form method="post">
        <input type="hidden" name="amount" value="100000">
        <input type="submit" value="送金">
    </form>
    """

if __name__ == "__main__":
    app.run(port=5000, debug=True)
