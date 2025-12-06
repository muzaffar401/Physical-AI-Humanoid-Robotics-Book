# Contract: Chapter 4.5 - Visual Grounding

**Chapter**: 4.5-4.6 - Visual Grounding with CLIP
**Component**: VisualGroundingNode (ROS 2 node for text-to-vision mapping)
**Purpose**: Matches text queries ("red box") to image regions using CLIP, computes 3D poses from depth data, publishes object frames to TF

## Overview

VisualGroundingNode subscribes to camera topics (`/camera/image_raw`, `/camera/depth/image_raw`) and text queries from `/object_query` topic. It uses CLIP to find objects matching text descriptions, computes 3D positions from depth data, and publishes object poses to TF and `/object_pose` topic.

## Functional Requirements

### FR-1: Subscribe to Camera Topics
- **Input**: `sensor_msgs/Image` from `/camera/image_raw` (RGB) and `/camera/depth/image_raw`
- **Output**: Cached latest images for processing
- **Constraints**: Handle image encoding (RGB8, 16UC1 for depth)

### FR-2: CLIP-Based Object Detection
- **Input**: RGB image + text query (e.g., "red box")
- **Output**: Bounding box coordinates (x, y, width, height) + confidence score
- **Algorithm**: Sliding window approach (divide image into grid, run CLIP on patches, find highest similarity)
- **Constraints**:
  - Grid size configurable (default: 4x4 = 16 patches)
  - CLIP model: ViT-B/32 (lightweight, ~150MB)
  - Device: GPU if available, else CPU
  - Confidence threshold: 0.3 (configurable)
- **Test**: Query "red box" in image with red, blue, green boxes, verify red box detected

### FR-3: 3D Pose Estimation from Depth
- **Input**: Bounding box (x, y, w, h) + depth image
- **Output**: 3D position (x, y, z) in camera frame
- **Algorithm**:
  1. Extract depth at bbox center
  2. Use camera intrinsics to project to 3D
  3. Transform to robot base frame using TF
- **Constraints**: Handle invalid depth (NaN, inf) → skip detection

### FR-4: TF Publishing
- **Input**: 3D pose (x, y, z) + object name
- **Output**: TF frame `/detected_object` (or `/detected_<object_name>`)
- **Constraints**: Frame parent = `camera_link`, update at 10 Hz

### FR-5: Publish Object Pose
- **Input**: 3D pose (x, y, z)
- **Output**: `geometry_msgs/PoseStamped` on `/object_pose` topic
- **Constraints**: Frame ID = `camera_link`

## API Specification

**Node Name**: `visual_grounding_node`

**Subscribers**:
- `/camera/image_raw` (sensor_msgs/Image): RGB images
- `/camera/depth/image_raw` (sensor_msgs/Image): Depth images
- `/object_query` (std_msgs/String): Text queries (e.g., "red box")

**Publishers**:
- `/object_pose` (geometry_msgs/PoseStamped): Detected object 3D pose
- `/detection_image` (sensor_msgs/Image): Annotated image with bounding box

**TF Broadcaster**:
- Frame: `/detected_object` → parent: `camera_link`

**Parameters**:
- `clip_model`: String (default: "ViT-B/32")
- `grid_size`: Int (default: 4, for 4x4 grid)
- `confidence_threshold`: Float (default: 0.3)
- `device`: String ("cuda" or "cpu", auto-detect if empty)

## Example Usage

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
from cv_bridge import CvBridge
import clip
import torch
import numpy as np

class VisualGroundingNode(Node):
    def __init__(self):
        super().__init__('visual_grounding_node')
        self.bridge = CvBridge()

        # Load CLIP
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

        # Subscribers
        self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.create_subscription(String, '/object_query', self.query_callback, 10)

        # Publisher
        self.pose_pub = self.create_publisher(PoseStamped, '/object_pose', 10)

        self.latest_image = None

    def image_callback(self, msg):
        self.latest_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")

    def query_callback(self, msg):
        if self.latest_image is None:
            return

        query = msg.data
        bbox = self.detect_object(self.latest_image, query)
        if bbox:
            pose = self.compute_3d_pose(bbox)
            self.pose_pub.publish(pose)

    def detect_object(self, image, query):
        # CLIP sliding window (simplified)
        h, w = image.shape[:2]
        patches = self.split_image(image, grid=4)
        text = clip.tokenize([query]).to(self.device)

        best_score = 0
        best_idx = 0
        for i, patch in enumerate(patches):
            patch_tensor = self.preprocess(patch).unsqueeze(0).to(self.device)
            with torch.no_grad():
                image_features = self.model.encode_image(patch_tensor)
                text_features = self.model.encode_text(text)
                similarity = (image_features @ text_features.T).item()

            if similarity > best_score:
                best_score = similarity
                best_idx = i

        if best_score > 0.3:
            return self.get_bbox_from_patch(best_idx, grid=4, image_shape=(h, w))
        return None

    def split_image(self, image, grid=4):
        # Split image into grid x grid patches
        patches = []
        h, w = image.shape[:2]
        patch_h, patch_w = h // grid, w // grid
        for i in range(grid):
            for j in range(grid):
                patch = image[i*patch_h:(i+1)*patch_h, j*patch_w:(j+1)*patch_w]
                patches.append(patch)
        return patches

    def get_bbox_from_patch(self, idx, grid, image_shape):
        h, w = image_shape
        patch_h, patch_w = h // grid, w // grid
        row = idx // grid
        col = idx % grid
        return (col * patch_w, row * patch_h, patch_w, patch_h)

    def compute_3d_pose(self, bbox):
        # Placeholder (Chapter 4.6 implements full 3D logic)
        pose = PoseStamped()
        pose.header.frame_id = "camera_link"
        pose.pose.position.x = 1.0  # Example
        pose.pose.position.y = 0.0
        pose.pose.position.z = 0.5
        return pose

def main():
    rclpy.init()
    node = VisualGroundingNode()
    rclpy.spin(node)
    rclpy.shutdown()
```

## Acceptance Criteria

1. ✅ Detects objects matching text queries in 80%+ of test images
2. ✅ Computes 3D poses from depth data
3. ✅ Publishes TF frames for detected objects
4. ✅ Runs at 1-2 FPS on CPU, 30 FPS on GPU
5. ✅ Handles missing depth data gracefully

---

**Status**: ✅ Contract complete
**Implementation Effort**: ~6-8 hours
