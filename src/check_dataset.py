
from pathlib import Path
from collections import Counter
from PIL import Image
import math

# ==========================================
# 1. DATASET CONFIGURATION
# ==========================================

DATASET_PATH = Path(
    r"D:\Programming Languages\PYTHON\Datasets for ML\PKU-Market-PCB(Data enhanced version)"
)

CLASSES = [
    "Missing hole",
    "Mouse bite",
    "Open circuit",
    "Short",
    "Spur",
    "Spurious copper"
]

SPLITS = ["train", "valid", "test"]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}


# ==========================================
# 2. INITIALIZE INSPECTION COUNTERS
# ==========================================

total_images = 0
total_annotations = 0

class_counts = Counter()
issues = []


# ==========================================
# 3. INSPECT EACH DATASET SPLIT
# ==========================================

for split in SPLITS:

    print(f"\n========== {split.upper()} ==========")

    image_dir = DATASET_PATH / split / "images"
    label_dir = DATASET_PATH / split / "labels"

    if not image_dir.is_dir() or not label_dir.is_dir():
        issues.append(f"{split}: Missing images or labels directory")
        continue

    images = [
        file for file in image_dir.iterdir()
        if file.is_file()
        and file.suffix.lower() in IMAGE_EXTENSIONS
    ]

    labels = list(label_dir.glob("*.txt"))

    total_images += len(images)

    print("Images:", len(images))
    print("Labels:", len(labels))

    image_names = {image.stem for image in images}
    label_names = {label.stem for label in labels}

    # Check matching image-label filenames

    for name in image_names - label_names:
        issues.append(f"{split}: Missing label for {name}")

    for name in label_names - image_names:
        issues.append(f"{split}: Missing image for {name}")

    # Validate image files

    for image_path in images:
        try:
            with Image.open(image_path) as image:
                image.verify()
        except Exception as error:
            issues.append(f"Invalid image: {image_path.name} ({error})")

    # Validate annotation files

    for label_path in labels:

        try:
            lines = label_path.read_text(encoding="utf-8").splitlines()
        except OSError as error:
            issues.append(f"Cannot read {label_path.name}: {error}")
            continue

        for line_number, line in enumerate(lines, start=1):

            if not line.strip():
                continue

            parts = line.split()

            if len(parts) != 5:
                issues.append(
                    f"{label_path.name}, line {line_number}: Expected 5 values"
                )
                continue

            try:
                class_value = float(parts[0])
                x_center, y_center, width, height = map(float, parts[1:])
            except ValueError:
                issues.append(
                    f"{label_path.name}, line {line_number}: Non-numeric values"
                )
                continue

            values = [class_value, x_center, y_center, width, height]

            if not all(math.isfinite(value) for value in values):
                issues.append(
                    f"{label_path.name}, line {line_number}: Non-finite value"
                )
                continue

            if not class_value.is_integer():
                issues.append(
                    f"{label_path.name}, line {line_number}: Invalid class ID"
                )
                continue

            class_id = int(class_value)

            if class_id < 0 or class_id >= len(CLASSES):
                issues.append(
                    f"{label_path.name}, line {line_number}: Unknown class ID {class_id}"
                )
                continue

            if not all(0 <= value <= 1 for value in
                       [x_center, y_center, width, height]):
                issues.append(
                    f"{label_path.name}, line {line_number}: Coordinate outside 0-1"
                )
                continue

            if width <= 0 or height <= 0:
                issues.append(
                    f"{label_path.name}, line {line_number}: Invalid box dimensions"
                )
                continue

            x_min = x_center - width / 2
            x_max = x_center + width / 2
            y_min = y_center - height / 2
            y_max = y_center + height / 2

            if x_min < 0 or y_min < 0 or x_max > 1 or y_max > 1:
                issues.append(
                    f"{label_path.name}, line {line_number}: Bounding box exceeds image"
                )
                continue

            class_counts[class_id] += 1
            total_annotations += 1


# ==========================================
# 4. GENERATE INSPECTION REPORT
# ==========================================

print("\n========== DATASET SUMMARY ==========")

print("Total images:", total_images)
print("Total valid annotations:", total_annotations)

print("\n========== CLASS DISTRIBUTION ==========")

for class_id, class_name in enumerate(CLASSES):
    print(f"{class_id} - {class_name}: {class_counts[class_id]}")

print("\n========== DATASET ISSUES ==========")

if not issues:
    print("No issues detected by the implemented checks.")
else:
    print("Total issues:", len(issues))

    for issue in issues[:30]:
        print("-", issue)

    if len(issues) > 30:
        print("Additional issues:", len(issues) - 30)

print("\n========== INSPECTION COMPLETE ==========")
