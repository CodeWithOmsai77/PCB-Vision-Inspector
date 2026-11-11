
from pathlib import Path
import torch
from ultralytics import YOLO


def main():

    # 1. Locate project directory
    ROOT = Path(__file__).resolve().parent.parent

    # 2. Define model and input image paths
    model_path = ROOT / "outputs" / "pcb_baseline" / "weights" / "best.pt"
    image_path = ROOT / "sample_images" / "01_open_circuit_15_2.jpg"

    # 3. Check input files
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # 4. Select device
    device = 0 if torch.cuda.is_available() else "cpu"
    print("Prediction device:", device)

    # 5. Load trained model
    model = YOLO(str(model_path))

    # 6. Perform prediction
    results = model.predict(
        source=str(image_path),
        imgsz=640,
        conf=0.10,
        device=device,
        save=True,
        project=str(ROOT / "outputs"),
        name="predictions",
        exist_ok=True
    )

    # 7. Display detection results
    print("\nPCB DEFECT DETECTION RESULTS")

    for result in results:

        if result.boxes is None or len(result.boxes) == 0:
            print("No defects detected.")
            continue

        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = result.names[class_id]

            print(f"{class_name}: {confidence:.2%}")

    print("\nPrediction completed.")


if __name__ == "__main__":
    main()
