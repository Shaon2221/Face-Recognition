from flask import Flask

UPLOAD_FOLDER = ''

app = Flask(__name__)
#app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def get_Confidence(value):
    OldValue=value
    OldMin=0
    OldMax=2.082
    NewMax=0
    NewMin=1
    NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
    print(NewValue)
    return NewValue
# resp.result=content
# resp.confidence=confidence
# return resp

# resp = jsonify(errors)
# resp.status_code = 500
# return resp