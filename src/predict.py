# predict.py
import tensorflow as tf
import numpy as np
from src.model import build_model

model = build_model()
model.load_weights("outputs/models/best_model.h5")

def predict_image(img_path):
    img = tf.keras.utils.load_img(img_path, target_size=(224,224))
    img = tf.keras.utils.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)

    pred = model.predict(img)
    return pred[0][0]


