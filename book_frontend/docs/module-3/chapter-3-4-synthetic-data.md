---
id: chapter-3-4-synthetic-data
title: "Chapter 3.4: Synthetic Data for Computer Vision"
sidebar_label: "3.4 Synthetic Data"
sidebar_position: 4
---

# Chapter 3.4: Synthetic Data for Computer Vision

## Training AI Without Collecting Real-World Data

Collecting 100,000 labeled images costs $10,000+ and weeks of effort. Rare scenarios (nighttime, rain, edge cases) are nearly impossible to capture at scale. **Synthetic data generation** solves this: Isaac Sim's **Replicator** can generate millions of perfect

ly-labeled images with automatic randomization—lighting, materials, poses, backgrounds—creating diverse datasets that rival real-world collection.

In this chapter, you'll use domain randomization to generate training data for object detection, semantic segmentation, and pose estimation—then evaluate how well models trained on synthetic data perform on real cameras.

---

## Learning Objectives

By the end of this chapter, you will:

- **Understand**: Explain domain randomization and why synthetic data generalizes to real-world deployment
- **Apply**: Use Isaac Sim Replicator to randomize lighting, materials, object poses, and camera parameters
- **Create**: Generate 10,000+ labeled images for YOLO object detection automatically
- **Analyze**: Train a YOLOv8 model on synthetic data and evaluate sim-to-real transfer
- **Apply**: Build production data pipelines with COCO format export

**Estimated Time**: 2.5 hours

---

## Prerequisites

- **Chapter 3.3 complete** (Sensor simulation, ground truth generation)
- **Chapter 3.2 complete** (Photorealistic environments)
- **Python programming** (NumPy, basic ML familiarity)
- **Optional**: PyTorch or TensorFlow experience (for training section)

---

## What You'll Build

By the end of this chapter, you'll have:

✅ **Domain randomization pipeline** generating diverse synthetic scenes
✅ **10,000+ labeled images** for object detection with bounding boxes
✅ **Trained YOLOv8 model** on purely synthetic data
✅ **Sim-to-real evaluation** comparing synthetic vs. real-world performance
✅ **Production data pipeline** with COCO/YOLO format export

---

## Why Synthetic Data Works

### The Sim-to-Real Gap

**Problem**: Models trained on Gazebo's cartoon-like graphics fail on real cameras.

**Root cause**: **Domain shift** → Training distribution ≠ Test distribution
- Gazebo: Flat colors, harsh shadows, unrealistic lighting
- Real world: Textured objects, soft shadows, natural light

**Solution**: Close the gap with:
1. **Photorealism** (RTX ray tracing) → Matches real lighting/materials
2. **Domain randomization** → Increase data diversity beyond real-world variation

### Domain Randomization Theory

**Core idea**: If you train on **infinite visual variations**, model learns **invariant features** that work everywhere.

**Randomize**:
- **Lighting**: Brightness, color, direction (day/night/cloudy)
- **Textures**: Materials, colors, patterns on objects/walls
- **Camera**: Position, angle, FOV, exposure, noise
- **Background**: Clutter, different environments
- **Object poses**: Rotation, position, occlusions

**Result**: Model sees 10,000 wildly different scenes → Learns "box is box" regardless of context → Generalizes to real cameras.

**Paper**: "Domain Randomization for Transferring Deep Neural Networks" (Tobin et al., 2017) - Trained robot gripper vision *only* on synthetic data, worked on real hardware with zero real examples.

---

## Isaac Sim Replicator Overview

**Replicator** is Isaac Sim's synthetic data generation framework.

**Key features**:
- **Randomizers**: Built-in functions for lights, materials, poses, cameras
- **Orchestrator**: Runs simulation, captures data automatically
- **Writers**: Export to COCO, KITTI, custom formats
- **Scripting**: Python API for full control

**Workflow**:
```
Define scene → Add randomizers → Run orchestrator → Export dataset
```

---

## Hands-On: Object Detection Dataset

Let's generate a dataset for detecting boxes in a warehouse.

### Step 1: Prepare Scene

1. Open Isaac Sim
2. Load warehouse environment (Chapter 3.2)
3. **Add target objects** (the things we want to detect):
   - **Create** → **Mesh** → **Cube** (represents a box/package)
   - Scale: (0.3, 0.3, 0.3) → 30cm cube
   - Position: (0, 0, 0.15) → On ground
   - Rename: `/World/Box_01`

4. **Assign semantic class**:
   ```python
   import omni.usd
   from pxr import Semantics

   stage = omni.usd.get_context().get_stage()
   box_prim = stage.GetPrimAtPath("/World/Box_01")
   sem = Semantics.SemanticsAPI.Apply(box_prim, "class")
   sem.CreateSemanticTypeAttr().Set("class")
   sem.CreateSemanticDataAttr().Set("box")
   ```

5. Add camera: `/World/Camera` at position (5, 0, 2) looking at origin

### Step 2: Create Randomization Script

**File**: `generate_dataset.py`

```python
import omni.replicator.core as rep
import numpy as np

# Define randomization parameters
NUM_FRAMES = 10000

# Get scene objects
camera = rep.create.camera(position=(0, 0, 0), look_at=(0, 0, 0))
box = rep.get.prims(path_pattern="/World/Box_01")

# Randomize box pose
with box:
    rep.modify.pose(
        position=rep.distribution.uniform((-5, -5, 0.15), (5, 5, 0.15)),  # Random XY position
        rotation=rep.distribution.uniform((0, 0, 0), (0, 0, 360)),  # Random Z rotation
        scale=rep.distribution.uniform((0.2, 0.2, 0.2), (0.5, 0.5, 0.5))  # Random size
    )

# Randomize lighting
lights = rep.get.prims(type="Light")
with lights:
    rep.modify.attribute(
        "intensity",
        rep.distribution.uniform(1000, 100000)  # Brightness variation
    )

# Randomize camera
with camera:
    rep.modify.pose(
        position=rep.distribution.uniform((3, -2, 1), (7, 2, 3)),  # Circle around scene
        look_at="/World/Box_01"  # Always point at box
    )

# Setup render products
rp = rep.create.render_product(camera, resolution=(1280, 720))

# Setup writer (export to COCO format)
writer = rep.WriterRegistry.get("BasicWriter")
writer.initialize(
    output_dir="~/isaac_data/boxes",
    rgb=True,
    semantic_segmentation=True,
    bounding_box_2d_tight=True,
    colorize_semantic_segmentation=False
)
writer.attach([rp])

# Run randomization
with rep.trigger.on_frame(num_frames=NUM_FRAMES):
    rep.randomizer.register(rep.modify.pose)
    rep.randomizer.register(rep.modify.attribute)

# Execute
rep.orchestrator.run()

print(f"Generated {NUM_FRAMES} synthetic images!")
```

**Run**:
1. **Window** → **Script Editor**
2. Paste script
3. **Execute**
4. Isaac Sim automatically:
   - Randomizes scene
   - Captures camera frame
   - Saves RGB + labels
   - Repeats 10,000 times

**Progress**: Check `~/isaac_data/boxes/` as images appear.

### Step 3: Verify Dataset

**Directory structure**:
```
~/isaac_data/boxes/
  rgb/
    rgb_0000.png
    rgb_0001.png
    ...
  bounding_box_2d_tight/
    bbox_0000.npy  # NumPy array
    bbox_data.json  # COCO-style annotations
  semantic/
    semantic_0000.png
```

**Load and inspect**:
```python
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Load RGB image
img = Image.open("~/isaac_data/boxes/rgb/rgb_0000.png")

# Load bounding box
bbox = np.load("~/isaac_data/boxes/bounding_box_2d_tight/bbox_0000.npy", allow_pickle=True)
print(bbox)  # [x_min, y_min, x_max, y_max, class_id]

# Visualize
plt.imshow(img)
x_min, y_min, x_max, y_max = bbox[0][:4]
plt.gca().add_patch(plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                                   fill=False, edgecolor='red', linewidth=2))
plt.show()
```

---

## Advanced Randomization Techniques

### Material Randomization

Change object materials every frame for texture invariance.

```python
import omni.replicator.core as rep

# Get material library
materials = rep.get.materials()

# Randomize box material
box = rep.get.prims(path_pattern="/World/Box_01")
with box:
    rep.randomizer.materials(materials=materials)
```

**Effect**: Box appears as wood, metal, plastic, concrete across frames → Model ignores texture.

### Background Randomization

Prevent model from overfitting to specific warehouse.

**Method 1: HDR Randomization**

```python
hdri_paths = [
    "warehouse_day.hdr",
    "warehouse_night.hdr",
    "outdoor_cloudy.hdr",
    "indoor_office.hdr"
]

# Randomize dome light texture
dome_light = rep.get.prims(path_pattern="/World/DomeLight")
with dome_light:
    rep.modify.attribute("texture:file", rep.distribution.choice(hdri_paths))
```

**Method 2: Wall Color Randomization**

```python
walls = rep.get.prims(path_pattern="/World/Wall_*")
with walls:
    rep.randomizer.color(
        colors=rep.distribution.uniform((0.5, 0.5, 0.5), (1.0, 1.0, 1.0))  # Gray to white
    )
```

### Occlusion Randomization

Add clutter to partially occlude target objects (harder detection).

```python
# Spawn random distractor objects
with rep.trigger.on_frame():
    for i in range(10):
        distractor = rep.create.cube(
            position=rep.distribution.uniform((-5, -5, 0), (5, 5, 2)),
            scale=rep.distribution.uniform((0.1, 0.1, 0.1), (0.4, 0.4, 0.4))
        )
```

**Effect**: Target box partially hidden by other boxes → Model learns to detect partial views.

---

## Converting to Training Formats

### COCO Format (for YOLOv8, Detectron2)

**COCO annotation JSON**:
```json
{
  "images": [
    {"id": 1, "file_name": "rgb_0000.png", "width": 1280, "height": 720}
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1,
      "category_id": 1,
      "bbox": [100, 150, 200, 180],  # [x, y, width, height]
      "area": 36000,
      "iscrowd": 0
    }
  ],
  "categories": [
    {"id": 1, "name": "box", "supercategory": "object"}
  ]
}
```

**Isaac Sim exports this automatically** with `BasicWriter` + `bounding_box_2d_tight`.

### YOLO Format (for YOLOv5/v8)

YOLO uses text files:

**Format**:
```
<class_id> <x_center> <y_center> <width> <height>
```

All values normalized to [0, 1].

**Convert from COCO**:
```python
def coco_to_yolo(bbox, img_width, img_height):
    """Convert COCO bbox to YOLO format"""
    x, y, w, h = bbox
    x_center = (x + w / 2) / img_width
    y_center = (y + h / 2) / img_height
    w_norm = w / img_width
    h_norm = h / img_height
    return [x_center, y_center, w_norm, h_norm]

# Example
bbox_coco = [100, 150, 200, 180]  # From Isaac Sim
bbox_yolo = coco_to_yolo(bbox_coco, 1280, 720)
print(bbox_yolo)  # [0.156, 0.292, 0.156, 0.250]

# Write to file
with open("labels/image_0000.txt", "w") as f:
    class_id = 0  # Box class
    f.write(f"{class_id} {' '.join(map(str, bbox_yolo))}\n")
```

---

## Training YOLOv8 on Synthetic Data

### Step 1: Install YOLOv8

```bash
pip install ultralytics
```

### Step 2: Prepare Dataset

**Directory structure**:
```
~/yolo_dataset/
  images/
    train/
      rgb_0000.png
      rgb_0001.png
    val/
      rgb_8000.png
      rgb_8001.png
  labels/
    train/
      rgb_0000.txt
      rgb_0001.txt
    val/
      rgb_8000.txt
      rgb_8001.txt
  dataset.yaml
```

**`dataset.yaml`**:
```yaml
path: ~/yolo_dataset
train: images/train
val: images/val

nc: 1  # Number of classes
names: ['box']
```

### Step 3: Train YOLOv8

```python
from ultralytics import YOLO

# Load pre-trained model (transfer learning from COCO)
model = YOLO('yolov8n.pt')  # Nano model (fastest)

# Train on synthetic data
model.train(
    data='dataset.yaml',
    epochs=50,
    imgsz=640,
    batch=16,
    device=0  # GPU
)

# Validate
metrics = model.val()
print(f"mAP@0.5: {metrics.box.map50}")

# Export for deployment
model.export(format='onnx')
```

**Training time**: ~30 minutes on RTX 3080 for 10,000 images.

### Step 4: Test on Real Images

```python
# Inference on real camera image
model = YOLO('runs/detect/train/weights/best.pt')

results = model('real_warehouse.jpg')
results.show()  # Display detections
```

**Expected**: If domain randomization was sufficient, model detects boxes in real images with high confidence!

---

## Evaluating Sim-to-Real Transfer

### Metrics

**Quantify performance**:
- **Synthetic validation mAP**: Performance on held-out synthetic images
- **Real validation mAP**: Performance on hand-labeled real images
- **Sim-to-real gap**: Difference between above

**Goal**: Minimize gap through better randomization.

### Improving Transfer

**If model fails on real data**:

1. **Analyze failure modes**:
   - Does it fail on specific lighting? → Add more light randomization
   - Does it fail on textures? → Randomize materials more
   - Does it fail on camera angles? → Increase camera pose variation

2. **Collect 10-100 real images** (not 10,000!):
   - Fine-tune model on small real dataset
   - Often closes remaining gap with minimal labeling

3. **Domain adaptation** (advanced):
   - Use GANs to style-transfer synthetic → real appearance
   - Adversarial training

---

## Production Data Pipeline

### Scaling to Millions of Images

**Challenge**: 10,000 images takes ~2 hours. Need 1 million images?

**Solution**: **Headless mode** + **parallel workers**.

**Run Isaac Sim without GUI**:
```bash
python ~/omni/isaac-sim/standalone_examples/replicator/offline_generation.py \
  --script generate_dataset.py \
  --num-frames 100000
```

**Multi-GPU parallel**:
- Launch 4 Isaac Sim instances on 4 GPUs
- Each generates 250,000 frames
- Total: 1 million images in ~10 hours

### Continuous Data Generation

**Use case**: Iteratively improve AI as failures are discovered.

**Pipeline**:
1. Deploy model to robot
2. Log failure cases (missed detections)
3. Add failure scenarios to randomization script
4. Re-generate dataset with new variations
5. Re-train model
6. Re-deploy

**Automation**: Run nightly on cloud GPUs (AWS g5.xlarge with RTX A10).

---

## Advanced: Semantic Segmentation Dataset

**Task**: Train a U-Net for pixel-wise scene understanding.

**Modifications to script**:
```python
# Use semantic segmentation writer
writer = rep.WriterRegistry.get("BasicWriter")
writer.initialize(
    output_dir="~/isaac_data/segmentation",
    rgb=True,
    semantic_segmentation=True,
    colorize_semantic_segmentation=False  # Raw class IDs
)
```

**Training**:
- Use PyTorch or TensorFlow with U-Net/DeepLabv3 architecture
- Loss: Cross-entropy per pixel
- Input: RGB image (H, W, 3)
- Output: Class IDs (H, W, 1)

---

## Key Takeaways

🎓 **Domain randomization** generates diverse synthetic data that generalizes to real-world deployment by training on infinite visual variations.

🎓 **Isaac Sim Replicator** automates randomization of lighting, materials, poses, cameras—no manual effort.

🎓 **Synthetic data eliminates labeling costs**—10,000 perfect bounding boxes generated in hours vs. $10,000+ manual annotation.

🎓 **Sim-to-real transfer works**—models trained purely on synthetic data achieve 80-95% of real-data performance with good randomization.

🎓 **Production pipelines** scale to millions of images using headless mode and parallel GPUs.

🎓 **Training formats**: Export to COCO (YOLOv8, Detectron2) or YOLO text files with automatic conversion.

---

## What's Next?

You've mastered synthetic data generation for perception—now let's train robot control policies with reinforcement learning!

In **Chapter 3.5: Reinforcement Learning with Isaac Gym**, you'll:

- Understand PPO, SAC, and RL fundamentals
- Train humanoid walking policies with GPU-accelerated parallel simulation
- Leverage Isaac Gym for 1000+ simultaneous robots
- Implement domain randomization for robust controllers
- Deploy RL policies from simulation to real hardware

**Continue to** → [Chapter 3.5: Reinforcement Learning](./chapter-3-5-reinforcement-learning)

---

## Assessment: Object Detection Dataset & Model

**Goal**: Generate synthetic dataset and train a working object detection model.

**Requirements**:

1. **Dataset generation**:
   - 5,000+ training images
   - Target object: Humanoid robot (or any USD model)
   - Randomize: lighting (3 variations), materials (5 variations), camera pose (hemisphere coverage)
   - Export with bounding boxes in COCO format

2. **Data quality**:
   - Objects visible in all images (not out-of-frame)
   - Bounding boxes accurate (IoU > 0.9 with manual check on 10 samples)
   - Diverse scenes (check visual variety with t-SNE on embeddings)

3. **Model training**:
   - Train YOLOv8 on synthetic data (or any detector)
   - Achieve mAP@0.5 > 0.8 on synthetic validation set
   - Test on 3 real-world images (hand-labeled)

4. **Deliverables**:
   - Replicator script (`generate_dataset.py`)
   - Sample images (20 with bounding boxes visualized)
   - Trained model weights (`.pt` or `.onnx`)
   - Evaluation report (400 words):
     - Synthetic mAP
     - Real-world qualitative results (screenshots)
     - Sim-to-real gap analysis
     - Lessons learned on randomization

**Expected Pass Rate**: 60% of learners complete within 150 minutes (excluding training time).

**Bonus**: Fine-tune on 50 real labeled images, report mAP improvement.

---

## Additional Resources

📚 **Official Documentation**:
- [Isaac Sim Replicator Guide](https://docs.omniverse.nvidia.com/replicator/latest/index.html)
- [Synthetic Data Generation Tutorial](https://docs.omniverse.nvidia.com/isaacsim/latest/replicator_tutorials/index.html)

📺 **Video Tutorials**:
- NVIDIA Replicator - Getting Started
- Synthetic Data for AI Training
- Domain Randomization Best Practices

🛠️ **Training Frameworks**:
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) - Easy object detection
- [Detectron2](https://github.com/facebookresearch/detectron2) - Facebook's vision library
- [MMDetection](https://github.com/open-mmlab/mmdetection) - Comprehensive detector toolbox

📖 **Papers**:
- "Domain Randomization for Transferring DNNs" (Tobin et al., 2017)
- "Learning Dexterous In-Hand Manipulation" (OpenAI, 2019) - Used domain randomization for robot hand
- "Sim-to-Real Transfer for Deep RL" (Peng et al., 2018)

---

**Chapter Status**: Complete ✅
**Next Chapter**: [3.5 Reinforcement Learning](./chapter-3-5-reinforcement-learning)
