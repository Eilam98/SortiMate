import gradio as gr
from transformers import AutoImageProcessor
from transformers import SiglipForImageClassification
from PIL import Image
import torch
import numpy as np

class WasteClassifier:
    def __init__(self, model_name="prithivMLmods/Augmented-Waste-Classifier-SigLIP2"):
        self.model_name = model_name
        self.model = SiglipForImageClassification.from_pretrained(self.model_name)
        self.processor = AutoImageProcessor.from_pretrained(self.model_name, use_fast=True)
        self.labels = {
            "0": "Battery", "1": "Biological", "2": "Cardboard", "3": "Clothes",
            "4": "Glass", "5": "Metal", "6": "Paper", "7": "Plastic",
            "8": "Shoes", "9": "Trash"
        }

    def waste_classification(self, image):
        """Predicts waste classification for an image.
        Accepts a NumPy array or a path/file-like; returns (predicted_label, confidence).
        """
        if isinstance(image, np.ndarray):
            pil_image = Image.fromarray(image)
        else:
            pil_image = Image.open(image).convert("RGB")

        inputs = self.processor(images=pil_image, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.nn.functional.softmax(logits, dim=1).squeeze().tolist()

        predictions = {self.labels[str(i)]: round(probs[i], 4) for i in range(len(probs))}
        predicted_label = max(predictions, key=predictions.get)

        return predicted_label, predictions[predicted_label]