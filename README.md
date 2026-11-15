# Tennis Video Analyzer

A Flask web app that takes a tennis match video and returns an annotated version with **player tracking, ball tracking, a mini-court overlay, and per-player stats** (shot speed, player speed, shot count).

> _Demo Video coming soon._

## Pipeline
```
Upload (Flask) ─► Frames (OpenCV)
                    ├─► Player detection + tracking   (YOLOv8x)
                    ├─► Ball detection                (fine-tuned YOLOv5) ─► interpolation of missed frames
                    └─► Court keypoints               (CNN keypoint model)
                              │
                              ▼
              Project to mini-court coordinates (pixels → meters)
                              │
                              ▼
      Shot detection ─► shot speed, player speed, shot count ─► annotated video
```

## Features
- Detects and tracks both players and filters out spectators and officials using court keypoints
- Detects the ball and fills in missed frames by interpolation
- Maps positions onto a top-down mini court so distances are in real-world meters
- Computes per-shot ball speed and player movement speed
- Simple web UI: upload a clip, get an annotated video back

## Tech
Python · Flask · PyTorch · Ultralytics YOLO · OpenCV · Pandas

## Running locally
```bash
git lfs install && git lfs pull     # model weights are stored with Git LFS
pip install -r requirements.txt
python app.py                       # http://localhost:5000
```

## Repo layout
```
app.py                     # Flask server (upload -> process -> serve result)
transform_video/main.py    # End-to-end processing pipeline
static/trackers/           # Player + ball trackers
static/court_line_detector/
static/mini_court/
static/models/             # Model weights (Git LFS)
templates/index.html       # Upload UI
```

## Acknowledgments
Pipeline adapted from [this tutorial](https://www.youtube.com/watch?v=L23oIHZE14w); I added the Flask app, upload flow, and user interface.
