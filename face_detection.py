import cv2
from insightface.app import FaceAnalysis
import numpy as np
# Initialize
app = FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))
known_names = []
known_embeddings = []
for name in ["Tran Khac Phuc Khanh"]:
    known_image = cv2.imread(f"{name}.jpg")
    known_faces = app.get(known_image)
    known_embedding = known_faces[0].embedding
    known_names.append(name)
    known_embeddings.append(known_embedding)
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect faces
    faces = app.get(frame)

    # Draw boxes
    for face in faces:
        bbox = face.bbox.astype(int)
        embedding = face.embedding
        label = "Unknown"
        best_similarity = -1
        for i in range(len(known_embeddings)):
            similarity = cosine_similarity(embedding, known_embeddings[i])
            if similarity > best_similarity:
                best_similarity = similarity
                best_match_name = known_names[i]
        if best_similarity > 0.4:
            label = best_match_name
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        cv2.putText(frame, f"{label}", (bbox[0], bbox[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    cv2.imshow('InsightFace Webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
