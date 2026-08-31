from flask import Flask, request, jsonify

from tars_core import TARS


app = Flask(__name__)

tars = TARS()


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "No message provided"
        }), 400

    try:

        response = tars.ask(message)

        return jsonify({
            "response": response
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "TARS online"
    })


if __name__ == "__main__":

    print(" TARS server starting...")
    print("Listening on port 5000")

    app.run(
        host="0.0.0.0",
        port=5000
    )
