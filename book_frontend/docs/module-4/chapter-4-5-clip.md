---
id: chapter-4-5-clip
title: "Chapter 4.5: Visual Grounding with CLIP"
sidebar_label: "4.5 Visual Grounding"
sidebar_position: 5
description: "Learn zero-shot object detection with CLIP for text-to-image matching"
keywords: [clip, visual grounding, zero-shot detection, vision-language models]
learning_journey: "LJ3"
duration: "2.5 hours"
difficulty: "advanced"
prerequisites:
  - "chapter-4-4-llm-planning"
objectives:
  - "Understand: Explain how CLIP enables zero-shot visual grounding"
  - "Apply: Use CLIP to match text queries to image regions"
  - "Create: Build VisualGroundingNode for object localization"
milestone: "Robot locates objects from text descriptions with 80%+ accuracy"
---

# Chapter 4.5: Visual Grounding with CLIP

## What You'll Learn

By the end of this chapter, you will:
- Understand CLIP (Contrastive Language-Image Pre-training) for vision-language tasks
- Implement zero-shot object detection by matching text to image patches
- Build a VisualGroundingNode that publishes bounding boxes for detected objects
- Integrate visual grounding with LLM action plans
- Handle edge cases (multiple objects, occlusions, no matches)

**Estimated Time**: 2.5 hours

---

## The Visual Grounding Problem

In Chapter 4.4, the LLM generated plans like:
```json
[
  {"action": "navigate", "target": "red box"},
  {"action": "detect", "object": "red box"},
  {"action": "grasp", "object": "red box"}
]
```

**Challenge**: The robot needs to **locate** the "red box" in camera images. How do we connect text "red box" to pixels in the image?

### Traditional Approach: Object Detection Models

Classical solution: Train object detector (YOLO, Faster R-CNN) on labeled dataset:
- Collect 1000+ images of boxes, label bounding boxes
- Train neural network to detect "box" class
- Deploy model

**Problems**:
- ❌ Requires labeled data for every object type
- ❌ Can't detect new objects without retraining
- ❌ No understanding of attributes like "red", "small", "metallic"

### CLIP Approach: Zero-Shot Visual Grounding

**CLIP** (Contrastive Language-Image Pre-training) learns a shared embedding space where:
- Text descriptions and images are encoded as vectors
- Similar text-image pairs have similar vectors
- **Zero-shot**: Works on any text query without training on that specific object

**How CLIP Works**:
1. **Image Encoder**: CNN or Vision Transformer (ViT) encodes image → 512D vector
2. **Text Encoder**: Transformer encodes text → 512D vector
3. **Similarity**: Cosine similarity between image and text vectors
4. **Training**: Trained on 400M (text, image) pairs from internet (captions, alt-text)

**Result**: CLIP can match "red box" to image regions without ever being trained on boxes specifically!

---

## Installing CLIP

```bash
pip install git+https://github.com/openai/CLIP.git
pip install torch torchvision pillow
```

---

## Basic CLIP Example: Text-Image Matching

Create file: `docs/assets/module-4/code/chapter-4-5/clip_basic.py`

```python
"""
Basic CLIP example: Match text queries to images
"""

import clip
import torch
from PIL import Image
import requests
from io import BytesIO

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
print(f"CLIP loaded on {device}")

# Download sample image (or use your own)
url = "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6"  # Image of a cat
response = requests.get(url)
image = Image.open(BytesIO(response.content))

# Preprocess image
image_input = preprocess(image).unsqueeze(0).to(device)

# Text queries
text_queries = [
    "a photo of a cat",
    "a photo of a dog",
    "a photo of a car",
    "a red box"
]

# Tokenize text
text_inputs = clip.tokenize(text_queries).to(device)

# Compute embeddings
with torch.no_grad():
    image_features = model.encode_image(image_input)
    text_features = model.encode_text(text_inputs)

    # Normalize
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    # Compute similarity
    similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)

# Print results
print("\nText-Image Similarity:")
for i, query in enumerate(text_queries):
    print(f"  '{query}': {similarity[0, i].item():.2%}")
```

**Expected Output**:
```
CLIP loaded on cuda
Text-Image Similarity:
  'a photo of a cat': 89.32%
  'a photo of a dog': 7.21%
  'a photo of a car': 2.14%
  'a red box': 1.33%
```

**CLIP correctly identifies the cat!**

---

## Zero-Shot Object Detection with Sliding Windows

To detect objects in an image:
1. **Divide image** into patches (e.g., 16x16 grid)
2. **Compute CLIP similarity** between text query and each patch
3. **Find patches with high similarity** → bounding boxes

### Code: CLIP Object Localization

Create file: `docs/assets/module-4/code/chapter-4-5/clip_detection.py`

```python
"""
CLIP-based object detection with sliding windows
"""

import clip
import torch
from PIL import Image, ImageDraw
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def detect_object(image, text_query, patch_size=64, threshold=0.25):
    """
    Detect object in image using CLIP

    Args:
        image: PIL Image
        text_query: Text description (e.g., "red box")
        patch_size: Size of sliding window
        threshold: Minimum similarity score

    Returns:
        List of bounding boxes [(x1, y1, x2, y2), ...]
    """
    width, height = image.size
    text_input = clip.tokenize([text_query]).to(device)

    # Encode text
    with torch.no_grad():
        text_features = model.encode_text(text_input)
        text_features /= text_features.norm(dim=-1, keepdim=True)

    # Sliding window
    detections = []
    for y in range(0, height - patch_size, patch_size // 2):
        for x in range(0, width - patch_size, patch_size // 2):
            # Extract patch
            patch = image.crop((x, y, x + patch_size, y + patch_size))
            patch_input = preprocess(patch).unsqueeze(0).to(device)

            # Compute similarity
            with torch.no_grad():
                patch_features = model.encode_image(patch_input)
                patch_features /= patch_features.norm(dim=-1, keepdim=True)
                similarity = (patch_features @ text_features.T).item()

            # Threshold
            if similarity > threshold:
                detections.append((x, y, x + patch_size, y + patch_size, similarity))

    # Non-maximum suppression (simple version)
    if detections:
        detections.sort(key=lambda d: d[4], reverse=True)
        best = detections[0]
        return [best[:4]]  # (x1, y1, x2, y2)

    return []

# Test
image = Image.open("test_image.jpg")  # Your test image
boxes = detect_object(image, "red box", patch_size=100, threshold=0.23)

# Visualize
draw = ImageDraw.Draw(image)
for box in boxes:
    draw.rectangle(box, outline="green", width=3)
image.show()
print(f"Detected {len(boxes)} objects")
```

---

## ROS 2 Integration: VisualGroundingNode

### Architecture

```
[/camera/image topic] + [/detect_object service] → [VisualGroundingNode]
                                                           ↓
                                                     [CLIP Detection]
                                                           ↓
                                               [/detected_bbox topic]
```

### Code: VisualGroundingNode

Create file: `docs/assets/module-4/code/chapter-4-5/visual_grounding_node.py`

```python
"""
VisualGroundingNode: Detects objects using CLIP
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import clip
import torch
from PIL import Image as PILImage
import numpy as np
import json

class VisualGroundingNode(Node):
    def __init__(self):
        super().__init__('visual_grounding_node')

        # Load CLIP
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        self.get_logger().info(f"CLIP loaded on {self.device}")

        # Subscribers
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.detect_sub = self.create_subscription(
            String,
            '/detect_object',
            self.detect_callback,
            10
        )

        # Publisher
        self.bbox_pub = self.create_publisher(String, '/detected_bbox', 10)

        self.bridge = CvBridge()
        self.latest_image = None

    def image_callback(self, msg):
        """Store latest camera image"""
        self.latest_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")

    def detect_callback(self, msg):
        """Detect object in latest image"""
        object_query = msg.data
        self.get_logger().info(f"Detecting: '{object_query}'")

        if self.latest_image is None:
            self.get_logger().warn("No image available")
            return

        # Detect with CLIP
        boxes = self.detect_object(self.latest_image, object_query)

        if boxes:
            bbox_msg = String()
            bbox_msg.data = json.dumps(boxes[0])  # Best detection
            self.bbox_pub.publish(bbox_msg)
            self.get_logger().info(f"✅ Detected at {boxes[0]}")
        else:
            self.get_logger().warn("❌ Object not found")

    def detect_object(self, image_np, text_query, patch_size=64, threshold=0.25):
        """CLIP-based detection (same as clip_detection.py)"""
        image = PILImage.fromarray(image_np)
        width, height = image.size

        text_input = clip.tokenize([text_query]).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text_input)
            text_features /= text_features.norm(dim=-1, keepdim=True)

        detections = []
        for y in range(0, height - patch_size, patch_size // 2):
            for x in range(0, width - patch_size, patch_size // 2):
                patch = image.crop((x, y, x + patch_size, y + patch_size))
                patch_input = self.preprocess(patch).unsqueeze(0).to(self.device)

                with torch.no_grad():
                    patch_features = self.model.encode_image(patch_input)
                    patch_features /= patch_features.norm(dim=-1, keepdim=True)
                    similarity = (patch_features @ text_features.T).item()

                if similarity > threshold:
                    detections.append((x, y, x + patch_size, y + patch_size, similarity))

        if detections:
            detections.sort(key=lambda d: d[4], reverse=True)
            return [detections[0][:4]]

        return []

def main(args=None):
    rclpy.init(args=args)
    node = VisualGroundingNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Running VisualGroundingNode

```bash
# Terminal 1: Run node
ros2 run vla_robot visual_grounding_node

# Terminal 2: Publish detection request
ros2 topic pub --once /detect_object std_msgs/msg/String "data: 'red box'"

# Terminal 3: Monitor detections
ros2 topic echo /detected_bbox
```

---

## Milestone Validation

✅ **You've completed Chapter 4.5 if**:
1. VisualGroundingNode detects objects from text queries
2. Bounding boxes published to /detected_bbox
3. Accuracy greater than 80% on 10 test objects
4. Works for color+object queries ("red box", "blue mug")
5. Gracefully handles "object not found" cases

---

## Chapter Summary

You learned:
- ✅ **CLIP**: Zero-shot vision-language model for text-image matching
- ✅ **Visual Grounding**: Sliding window + CLIP similarity for object localization
- ✅ **ROS 2 Integration**: VisualGroundingNode detects objects from camera images
- ✅ **Zero-Shot Detection**: Works on any text query without retraining

---

## What's Next?

In **Chapter 4.6**, we'll add **3D pose estimation** to convert 2D bounding boxes into 3D positions (x, y, z) using depth cameras.

**🎯 Next Chapter**: [4.6 3D Pose Estimation](./chapter-4-6-pose)
