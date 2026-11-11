from pathlib import Path
import random
import shutil

# Dataset locations
DATASET = Path(
    r"D:\Programming Languages\PYTHON\Datasets for ML\PKU-Market-PCB(Data enhanced version)"
)

OUTPUT = Path("outputs/dataset_samples")

IMAGE_DIR = DATASET / "train" / "images"
LABEL_DIR = DATASET / "train" / "labels"

# Six defect categories
classes = {
    0: "Missing_hole",
    1: "Mouse_bite",
    2: "Open_circuit",
    3: "Short",
    4: "Spur",
    5: "Spurious_copper"
}

OUTPUT.mkdir(parents=True, exist_ok=True)

random.seed(42)

for class_id, class_name in classes.items():

    matching_images = []

    for label_file in LABEL_DIR.glob("*.txt"):

        lines = label_file.read_text().splitlines()

        for line in lines:
            values = line.split()

            if values and int(values[0]) == class_id:
                image_file = IMAGE_DIR / f"{label_file.stem}.jpg"

                if image_file.exists():
                    matching_images.append(image_file)

                break

    if matching_images:
        selected = random.choice(matching_images)

        destination = OUTPUT / f"{class_name}.jpg"
        shutil.copy2(selected, destination)

        print(f"Selected: {destination}")

print("Dataset sample selection completed.")