from flask import Flask, render_template, request
from flask import jsonify
import requests,base64,json
from io import BytesIO, StringIO
from PIL import Image
from deepface import DeepFace
from AWS_Code import *

app = Flask(__name__)

@app.route('/',methods=['GET'])
def Home():
    return 'This is Homepage!'

def get_Confidence(value):
    OldValue=value
    OldMin=0
    OldMax=2.082
    NewMax=0
    NewMin=1
    NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
    print(NewValue)
    return NewValue


@app.route('/upload',methods=['GET','POST'])
def Upload():
    if request.method == 'POST':
        try:
            files = request.files.getlist("fileupload")
            im1 = Image.open(files[0])
            im2 = Image.open(files[1])
            if len(files)>2 or len(files)<2:
            	content = 'Please Provide two Images'
            	return render_template('upload_image.html',content=content)
        except Exception as e:
        	print(e)
        	return render_template('upload_image.html',conntent='Invalid')
        # res = request.get_json()
        # raw_img1 = res['img1']
        # raw_img2 = res['img2']
        # im1 = Image.open(BytesIO(base64.b64decode(raw_img1)))
        # im2 = Image.open(BytesIO(base64.b64decode(raw_img2)))
        im1.save('static/img1.jpg')
        print('img1.jpg received')
        im2.save('static/img2.jpg')
        print('img2.jpg received')
        backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
        metrics = ["cosine", "euclidean", "euclidean_l2"]
        models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
        try:
            try:
                result = DeepFace.verify(img1_path = 'static/img1.jpg', img2_path = 'static/img2.jpg',align = False,\
                detector_backend = backends[4],distance_metric = metrics[2], model_name = models[2])
                print(result)
                print(result['verified'])
                if result['verified'] == True:
                    content = 'Verified'
                    confidence=get_Confidence(result['distance'])
                    return render_template('upload_image.html',content=content,confidence=confidence,image_names=['img1.jpg','img2.jpg'])
                else:
                    content = 'Not Verified'
                    confidence=get_Confidence(result['distance'])
                    return render_template('upload_image.html',content=content,confidence=confidence,image_names=['img1.jpg','img2.jpg'])
            except Exception as e:
                print('First Attempt:',e)
                result = DeepFace.verify(img1_path = 'static/img1.jpg', img2_path = 'static/img2.jpg',align = True,\
                detector_backend = backends[4],distance_metric = metrics[2], model_name = models[2])
                print(result)
                print(result['verified'])
                if result['verified'] == True:
                    content = 'Verified'
                    confidence=get_Confidence(result['distance'])
                    return render_template('upload_image.html',content=content,confidence=confidence,image_names=['img1.jpg','img2.jpg'])
                else:
                    content = 'Not Verified'
                    confidence=get_Confidence(result['distance'])
                    return render_template('upload_image.html',content=content,confidence=confidence,image_names=['img1.jpg','img2.jpg'])
        except Exception as e:
            print('Second Attempt:',e)
            print("Face Could not be detected. Give valid human image!")
            content = 'Face Could not be detected. Give valid human image!'
            return render_template('upload_image.html',content=content)
    return render_template('upload_image.html',content='Upload two valid human Images')


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5006)
