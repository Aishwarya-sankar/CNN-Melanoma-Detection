import tensorflow as tf

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

def get_datasets(train_dir, val_dir, test_dir):
    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir, labels="inferred", label_mode="binary",
        batch_size=BATCH_SIZE, image_size=IMG_SIZE
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        val_dir, labels="inferred", label_mode="binary",
        batch_size=BATCH_SIZE, image_size=IMG_SIZE
    )
    test_ds = tf.keras.utils.image_dataset_from_directory(
        test_dir, labels="inferred", label_mode="binary",
        batch_size=BATCH_SIZE, image_size=IMG_SIZE
    )
    return train_ds, val_ds, test_ds
