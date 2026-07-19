try:
    # type: ignore - some linters/editors may not resolve flask in certain environments
    from flask import Flask, request, jsonify
except Exception:  # pragma: no cover - graceful fallback if flask isn't installed
    raise ImportError(
        "Flask is not installed or could not be imported. Install it with: pip install flask"
    )

app = Flask(__name__)


@app.route("/ask", methods=["POST"])
def ask():

    data = request.json

    question = data["question"]

    answer = "You asked: " + question

    return jsonify({
        "answer": answer
    })


app.run(host="127.0.0.1", port=5000)