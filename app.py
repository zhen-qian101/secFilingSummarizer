from flask import Flask, render_template, request, jsonify, session
from static import utils
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_bytes(32)

@app.route("/", methods=["POST", "GET"])
def index():    
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    data = request.get_json()
    ticker = data['ticker']
    headers = utils.headers

    form_text = utils.fetch_latest_filing(ticker)
    # tenK_item7 = utils.extract_tenK_item7(form_text)
    evi = utils.retrieve_evidences(form_text)


    return jsonify(evi=evi)


if __name__ == '__main__':
    
    app.run(debug=True)
