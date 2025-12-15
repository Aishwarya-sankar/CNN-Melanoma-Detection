import tensorflow as tf
from data_loader import get_datasets
from model import build_model

train_dir = "../dataset/train"
val_dir = "../dataset/val"
test_dir = "../dataset/test"

train_ds, val_ds, test_ds = get_datasets(train_dir, val_dir, test_dir)
model = build_model()

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    "../outputs/models/best_model.h5", save_best_only=True, monitor="val_accuracy"
)

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=20,
    callbacks=[checkpoint]
)

print("Evaluating on test data...")
test_loss, test_acc = model.evaluate(test_ds)
print("Test accuracy:", test_acc)
