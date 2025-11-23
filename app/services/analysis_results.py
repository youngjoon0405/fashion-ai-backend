from google.cloud import firestore
from datetime import datetime

db = firestore.Client()

def save_analysis_result(user_id: str, image_url: str, ai_result: dict):

    doc_ref = (
        db.collection("analysis_results")
          .document(user_id)
          .collection("results")
          .document()
    )

    doc_ref.set({
        "uid": user_id,
        "image_url": image_url,
        "ai_result": ai_result,
        "created_at": datetime.utcnow().isoformat(),
    })
