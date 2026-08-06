from transformers import pipeline


# ~350MB model, downloads on first run to ~/.cache/huggingface/
classifier = pipeline("image-classification", model="google/vit-base-patch16-224")


def classify_image(file_path: str) -> list[dict]:
    """
    Given a path to an image file, return the top 5 predicted labels 
    with confidence scores.
    """
    #  the pipeline opens the file, decodes the image format (JPG/PNG bytes → pixel array), 
    # and feeds it into the neural network.
    # 
    # top_k=5 asks for the top 5 predictions instead of just 1. Useful because 
    # the model might be 40% confident it's a golden retriever and 30% a 
    # labrador — both are meaningful information.
    results = classifier(file_path, top_k=5)

    # results is already a list of dicts: [{"label": "golden retriever", "score": 0.94}, ...]
    # We rebuild each dict to convert numpy floats to Python floats so JSON 
    # serialization works (same reason we did int()/float() in anomaly.py).
    return [
        {"label": r["label"], "score": float(r["score"])} 
        for r in results
    ]