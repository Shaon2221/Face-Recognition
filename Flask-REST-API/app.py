from flask import Flask

UPLOAD_FOLDER = ''

app = Flask(__name__)
#app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# resp.result=content
# resp.confidence=confidence
# return resp

# resp = jsonify(errors)
# resp.status_code = 500
# return resp