import os
import shutil
import random

SOURCE_DIR = "dataset/all_images"
DEST_DIR = "dataset"

SPLIT = {
    "train": 0.7,
    "val": 0.15,
    "test": 0.15
}

random.seed(42)

for category in ["benign", "malignant"]:
    category_path = os.path.join(SOURCE_DIR, category)

    images = os.listdir(category_path)
    images = [img for img in images if img.lower().endswith((".png", ".jpg", ".jpeg"))]
    random.shuffle(images)

    train_end = int(len(images) * SPLIT["train"])
    val_end = train_end + int(len(images) * SPLIT["val"])

    splits = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:]
    }

    for split, files in splits.items():
        split_dir = os.path.join(DEST_DIR, split, category)
        os.makedirs(split_dir, exist_ok=True)

        for file in files:
            src = os.path.join(category_path, file)
            dst = os.path.join(split_dir, file)
            shutil.copy(src, dst)

print("✅ Dataset split completed!")
