import cv2
import os
import numpy as np
from insightface.app import FaceAnalysis
class FaceDatabase:
    def __init__(self, db_root="face_db"):
        self.db_root = db_root
        os.makedirs(db_root, exist_ok=True)
        self.app = FaceAnalysis(providers=['CPUExecutionProvider'])
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def add_face(self, class_name, student_id, image_path):
        class_dir = os.path.join("class", class_name, self.db_root)
        os.makedirs(class_dir, exist_ok=True)
        img = cv2.imread(image_path)
        faces = self.app.get(img)
        if not faces:
            raise Exception("Không tìm thấy khuôn mặt")
        embedding = faces[0].embedding
        np.save(os.path.join(class_dir, f"{student_id}.npy"), embedding)
        return embedding

    def load_class(self, class_name):
        class_dir = os.path.join("class", class_name, self.db_root)
        known_embeddings = []
        student_ids = []
        for fname in os.listdir(class_dir):
            if fname.endswith(".npy"):
                sid = fname[:-4]
                emb = np.load(os.path.join(class_dir, fname))
                student_ids.append(sid)
                known_embeddings.append(emb)
        return student_ids, known_embeddings
