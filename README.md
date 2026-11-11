# PCB Vision Inspector

**AI-powered PCB defect detection using YOLO11n and computer vision.**

PCB Vision Inspector is an experimental object-detection project that identifies and localizes six types of printed circuit board (PCB) defects. The first phase focuses on dataset validation, baseline model training, independent test-set evaluation, and visualizing model predictions.

> **Project status:** Phase 01 — baseline model completed. The interactive inspection application is planned for Phase 02. This baseline is a learning and development result, not a production inspection system.

## Defect categories

The model is trained to detect these six classes:

| Class ID | Defect |
|---:|---|
| 0 | Missing hole |
| 1 | Mouse bite |
| 2 | Open circuit |
| 3 | Short |
| 4 | Spur |
| 5 | Spurious copper |

## Phase 01 dataset

The project uses the **PKU-Market-PCB (Data enhanced version)** dataset in YOLO detection format. The dataset is kept outside this repository and is not included in the GitHub upload.

| Split | Images |
|---|---:|
| Training | 2,772 |
| Validation | 366 |
| Test | 366 |
| **Total** | **3,504** |

The dataset validation script checks image/label filename matching, image readability, YOLO annotation format, numeric values, class IDs, normalized coordinates, and bounding-box dimensions. These structural checks do not independently verify whether every annotation is semantically correct.

## Model and training configuration

| Setting | Value |
|---|---|
| Model | YOLO11n (pretrained) |
| Framework | Ultralytics / PyTorch |
| Training epochs | 5 |
| Image size | 640 × 640 |
| Batch size | 4 |
| Data loader workers | 0 |
| Training device | NVIDIA RTX 3050 GPU when CUDA is available; otherwise CPU |

The five-epoch run is an initial baseline. It should not be interpreted as a fully optimized model.

## Initial test-set results

The trained checkpoint was evaluated on the held-out **test** split (366 images, 1,307 annotated defect instances).

| Metric | Result |
|---|---:|
| Precision | 80.47% |
| Recall | 55.22% |
| mAP@50 | 62.16% |
| mAP@50–95 | 29.41% |

These metrics describe this specific five-epoch baseline and dataset split. Recall and localization performance leave room for improvement; the model is not production-ready.

### Evaluation visualizations

**Test-set confusion matrix**

![Test-set confusion matrix](outputs/test_evaluation/confusion_matrix.png)

**Normalized test-set confusion matrix**

![Normalized test-set confusion matrix](outputs/test_evaluation/confusion_matrix_normalized.png)

**Precision–recall curve**

![Test-set precision recall curve](outputs/test_evaluation/BoxPR_curve.png)

**Training results**

![Training results](outputs/pcb_baseline/results.png)

### Prediction examples

The following images show model outputs with predicted defect labels and confidence scores.

| Missing-hole example | Spurious-copper example |
|---|---|
| ![PCB prediction example](outputs/predictions/pcb_defect.jpg) | ![Spurious copper prediction example](outputs/predictions/Spurious_copper.jpg) |

Predicted boxes are model outputs, not ground-truth confirmation. Confidence scores should not be interpreted as a guarantee that a defect is present.

## Repository structure

```text
PCB-Vision-Inspector/
├── src/
│   ├── check_dataset.py
│   ├── select_dataset_samples.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
├── sample_images/                 # Input PCB images for prediction
├── outputs/
│   ├── dataset_samples/            # Selected dataset examples
│   ├── pcb_baseline/               # Training plots and validation outputs
│   ├── test_evaluation/            # Independent test-set metrics and plots
│   └── predictions/                # Annotated prediction examples
├── data.yaml                       # YOLO dataset configuration
├── .gitignore
├── LICENSE
└── README.md
```

Model checkpoint files (`.pt`) and the full dataset are intentionally excluded from this repository.

## Getting started

### 1. Clone the repository

```powershell
git clone https://github.com/CodeWithOmsai77/PCB-Vision-Inspector.git
cd PCB-Vision-Inspector
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install a PyTorch build appropriate for your system and CUDA version by following the [official PyTorch installation selector](https://pytorch.org/get-started/locally/). Then install Ultralytics and Pillow:

```powershell
python -m pip install --upgrade pip
python -m pip install ultralytics pillow
```

### 4. Prepare the dataset

Download and extract the PKU-Market-PCB dataset separately. The expected directory structure is:

```text
PKU-Market-PCB/
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

Update the `path` value in `data.yaml` to the location of your extracted dataset. The `train`, `val`, and `test` entries are relative to that path.

The dataset path is also currently specified directly in `src/check_dataset.py` and `src/select_dataset_samples.py`. Update the `DATASET_PATH` value in those scripts before running them on another computer.

### 5. Validate the dataset

```powershell
python src/check_dataset.py
```

### 6. Train the baseline model

```powershell
python src/train.py
```

The training script uses `yolo11n.pt` as the pretrained starting checkpoint. Ultralytics can download it if it is not already available. Training outputs and the `best.pt` checkpoint are written under `outputs/pcb_baseline/`.

### 7. Evaluate on the test split

After training completes:

```powershell
python src/evaluate.py
```

The evaluation script loads `outputs/pcb_baseline/weights/best.pt` and evaluates the held-out test split. Plots are saved under `outputs/test_evaluation/`.

### 8. Run prediction on a sample image

Before running prediction, open `src/predict.py` and set `image_path` to an image that exists in your `sample_images/` folder. The default filename in the current script may need to be changed to match the files included in the repository.

```powershell
python src/predict.py
```

The script saves annotated predictions under `outputs/predictions/`. Its current confidence threshold is `0.10`.

## Phase 02 roadmap

- Develop an interactive Streamlit inspection dashboard.
- Support single-image and batch PCB inspection.
- Add inspection history and analytics.
- Generate downloadable PDF inspection reports.
- Improve recall and reduce false-positive detections through further experimentation and evaluation.

## License

This project is released under the [MIT License](LICENSE).

## Acknowledgements

- PKU-Market-PCB dataset contributors.
- [Ultralytics](https://github.com/ultralytics/ultralytics) for the YOLO framework.
- [PyTorch](https://pytorch.org/) for the deep learning framework.
