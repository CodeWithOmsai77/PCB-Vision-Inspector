from pathlib import Path
import torch
from ultralytics import YOLO


def main():

    # Locate project directory
    ROOT = Path(__file__).resolve().parent.parent

    # Locate trained model
    model_path = ROOT / "outputs" / "pcb_baseline" / "weights" / "best.pt"

    # Select evaluation device
    device = 0 if torch.cuda.is_available() else "cpu"

    print("Evaluation device:", device)
    print("Loading model:", model_path)

    # Load trained YOLO model
    model = YOLO(str(model_path))

    # Evaluate on the independent test dataset
    metrics = model.val(
        data=str(ROOT / "data.yaml"),
        split="test",
        imgsz=640,
        batch=4,
        device=device,
        workers=0,
        plots=True,
        project=str(ROOT / "outputs"),
        name="test_evaluation",
        exist_ok=True
    )

    # Display evaluation metrics
    print("\nTEST DATASET RESULTS")
    print("Precision:", metrics.box.mp)
    print("Recall:", metrics.box.mr)
    print("mAP50:", metrics.box.map50)
    print("mAP50-95:", metrics.box.map)


if __name__ == "__main__":
    main()