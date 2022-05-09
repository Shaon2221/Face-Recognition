import os
import urllib.request
from app import app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
from flask import jsonify
import requests,base64,json
from io import BytesIO, StringIO
from PIL import Image
from deepface import DeepFace

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'files[]' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	
	files = request.files.getlist('files[]')
	
	errors = {}
	success = False
	if len(files)>2 or len(files)<2:
		errors['message'] = 'Please Provide two Images'
		resp = jsonify(errors)
		resp.status_code = 406
		return resp
	
	for file in files:	
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			success = True
		else:
			errors[file.filename] = 'File type is not allowed'
	
	if success and errors:
		errors['message'] = 'File(s) successfully uploaded'
		resp = jsonify(errors)
		resp.status_code = 500
		return resp
	if success:
		im1 = Image.open(files[0])
		im2 = Image.open(files[1])
		im1.save('static/img1.jpg')
		print('img1.jpg received')
		im2.save('static/img2.jpg')
		print('img2.jpg received')
		backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
		metrics = ["cosine", "euclidean", "euclidean_l2"]
		models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
		try:
			try:
				print('First Attempt:')
				result = DeepFace.verify(img1_path = 'static/img1.jpg', img2_path = 'static/img2.jpg',align = False,\
                detector_backend = backends[4],distance_metric = metrics[2], model_name = models[2])
				print(result)
				print(result['verified'])
				if result['verified'] == True:
					print('Verified')
					content='Verified'
					confidence=result['distance']
					resp = jsonify({'message' : 'Files successfully uploaded', 'result' : content, 'confidence' : confidence})
					resp.status_code = 202
					return resp
				else:
					print('Not Verified')
					content='Not Verified'
					confidence=result['distance']
					resp = jsonify({'message' : 'Files successfully uploaded', 'result' : content, 'confidence' : confidence})
					resp.status_code = 202
					return resp
			except Exception as e:
				print('Second Attempt:',e)
				result = DeepFace.verify(img1_path = 'static/img1.jpg', img2_path = 'static/img2.jpg',align = True,\
                detector_backend = backends[4],distance_metric = metrics[2], model_name = models[2])
				print(result)
				print(result['verified'])
				if result['verified'] == True:
					print('Verified')
					content='Verified'
					confidence=result['distance']
					resp = jsonify({'message' : 'Files successfully uploaded', 'result' : content, 'confidence' : confidence})
					resp.status_code = 202
					return resp
				else:
					print('Not Verified')
					content='Not Verified'
					confidence=result['distance']
					resp = jsonify({'message' : 'Files successfully uploaded', 'result' : content, 'confidence' : confidence})
					resp.status_code = 202
					return resp
		except Exception as e:
			content = 'Face Could not be detected. Give valid human image!'
			print(content)
			confidence = 0
			resp = jsonify({'message' : 'Invalid Image', 'result' : content, 'confidence' : confidence})
			resp.status_code = 406
			return resp
	else:
		resp = jsonify(errors)
		resp.status_code = 500
		return resp

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5006)