from datetime import datetime
import numpy as np
from FaceDatabase import FaceDatabase
import os
import csv
import cv2
class Teacher:
    def __init__(self, teacher_id, class_list: list, face_db: FaceDatabase, threshold=0.5):
        self.teacher_id = teacher_id
        self.face_db = face_db
        self.class_list = class_list
        self.app = self.face_db.app
        self.threshold = threshold

    def select_class(self, class_name):
        self.current_class = class_name
        self.student_ids, self.known_embeddings = self.face_db.load_class(class_name)
        self.class_dir = os.path.join("class", class_name)
        self.member_list_path = os.path.join(self.class_dir, "class_member_list.csv")

    def get_class_members(self):
        try:
            with open(self.member_list_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                headers = reader.fieldnames
                rows = list(reader)
            return headers, rows
        except FileNotFoundError:
            print(f"Không tìm thấy file {self.member_list_path}")
            return [], []
    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def process_webcam(self, frame):
        faces = self.app.get(frame)
        for face in faces:
            bbox = face.bbox.astype(int)
            embedding = face.embedding
            label = "Unknown"
            best_similarity = -1

            for i in range(len(self.known_embeddings)):
                similarity = (
                    self.cosine_similarity(embedding, self.known_embeddings[i]))
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match_name = self.student_ids[i]

            if best_similarity > 0.4:
                label = best_match_name

            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            cv2.putText(frame, label, (bbox[0], bbox[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        return frame
