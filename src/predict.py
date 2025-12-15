import tensorflow as tf
import numpy as np
from model import build_model   # ✅ now works

model = build_model()
model.load_weights("../outputs/models/best_model.h5")

img = tf.keras.utils.load_img("../sample.jpg", target_size=(224,224))
img = tf.keras.utils.img_to_array(img)
img = np.expand_dims(img, axis=0)

img = tf.keras.applications.mobilenet_v2.preprocess_input(img)

pred = model.predict(img)

print("Prediction value:", pred[0][0])
print("Malignant" if pred[0][0] > 0.5 else "Benign")
