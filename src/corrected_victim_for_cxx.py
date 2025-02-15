from flask import Flask, request, session, redirect, url_for, jsonify, make_response, render_template_string
import secrets

app = Flask(__name__)
app.secret_key = "supersecretkey"

# シンプルなログインフォーム
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = "victim"
        return redirect(url_for("dashboard"))

    return """
    <h2>ログインページ</h2>
    <form method="post">
        <input type="submit" value="ログイン">
    </form>
    """

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    
    return """
    <h2>ダッシュボード</h2>
    <p>ようこそ、あなたはログインしています。</p>
    <a href="/get-csrf-token">CSRFトークンを取得</a> |
    <a href="/logout">ログアウト</a>
    """

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/get-csrf-token", methods=["GET"])
def get_csrf_token():
    if "user" not in session:
        return "Unauthorized", 401

    csrf_token = secrets.token_hex(16)
    session["csrf_token"] = csrf_token

    response = make_response(jsonify({"message": "CSRF token set"}))
    response.set_cookie("csrf_token", csrf_token, httponly=True, samesite="Strict")
    return response

@app.route("/transfer", methods=["POST"])
def transfer():
    if "user" not in session:
        return "Unauthorized", 401

    token = request.headers.get("X-CSRF-Token")
    if not token or token != session.get("csrf_token"):
        return "CSRF attack detected!", 403

    return "Transfer successful!"

if __name__ == "__main__":
    app.run(port=5000, debug=True)
