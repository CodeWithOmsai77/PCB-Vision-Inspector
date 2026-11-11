
from pathlib import Path
import torch
from ultralytics import YOLO


def main():

    # Project directory
    ROOT = Path(__file__).resolve().parent.parent

    # Check GPU availability
    device = 0 if torch.cuda.is_available() else "cpu"

    print("Training device:", device)

    # Load pretrained YOLO11 Nano model
    model = YOLO("yolo11n.pt")

    # Train the model
    results = model.train(
        data=str(ROOT / "data.yaml"),
        epochs=5,
        imgsz=640,
        batch=4,
        device=device,
        workers=0,
        project=str(ROOT / "outputs"),
        name="pcb_baseline",
        exist_ok=True
    )

    print("Training experiment completed.")


if __name__ == "__main__":
    main()
