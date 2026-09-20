# config.py
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = str(APP_DIR / 'pose_landmarker_lite.task')
VIDEO_PATH = str(APP_DIR / 'uber.mp4')

# Thresholds de Confiança
MIN_DETECTION_CONFIDENCE = 0.2
MIN_PRESENCE_CONFIDENCE = 0.3
MIN_VISIBILITY = 0.3

# Limiar de Invasão (Razão entre distância e largura do ombro do passageiro)
INVASION_THRESHOLD_RATIO = 1.2

# Limite máximo de pessoas no frame
MAX_POSES = 3

# Mapeamento de Landmarks (MediaPipe Pose)
KEYPOINT_NOSE = 0
KEYPOINT_LEFT_SHOULDER = 11
KEYPOINT_RIGHT_SHOULDER = 12
KEYPOINT_LEFT_WRIST = 15
KEYPOINT_RIGHT_WRIST = 16