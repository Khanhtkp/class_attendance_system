# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
from Teacher import Teacher
from FaceDatabase import FaceDatabase

app = Flask(__name__)

face_db = FaceDatabase()
teacher = Teacher("GV01", ["2425H_AIT3004_60"], face_db)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", class_list=teacher.class_list, headers=[], students=[])

@app.route("/select_class", methods=["POST"])
def select_class():
    class_name = request.form["class_name"]
    teacher.select_class(class_name)
    headers, students = teacher.get_class_members()
    return render_template("index.html", class_list=teacher.class_list,
                           headers=headers, students=students)

@app.route("/process_frame", methods=["POST"])
def process_frame():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({"error": "No image data received"}), 400

    # Giải mã ảnh từ base64
    img_data = base64.b64decode(data['image'].split(',')[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Xử lý ảnh: vẽ khung khuôn mặt & tên
    processed_frame = teacher.process_webcam(frame)

    # Mã hóa ảnh đã xử lý về base64
    _, buffer = cv2.imencode('.jpg', processed_frame)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    image_data_url = f"data:image/jpeg;base64,{encoded_image}"

    return jsonify({ "image": image_data_url })
@app.route("/get_class_data")
def get_class_data():
    class_name = request.args.get("class_name")
    if not class_name:
        return jsonify({"error": "Thiếu tên lớp"}), 400

    teacher.select_class(class_name)
    headers, students = teacher.get_class_members()
    return jsonify({"headers": headers, "students": students})

if __name__ == "__main__":
    app.run(debug=True)
