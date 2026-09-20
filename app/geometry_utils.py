# geometry_utils.py
import math

def calculate_euclidean_distance(point_a, point_b, frame_width, frame_height):
    """Calcula a distância euclidiana em pixels entre dois pontos normalizados."""
    x1, y1 = point_a.x * frame_width, point_a.y * frame_height
    x2, y2 = point_b.x * frame_width, point_b.y * frame_height
    return math.hypot(x2 - x1, y2 - y1)

def get_shoulder_width(landmarks, frame_width, frame_height, left_idx=11, right_idx=12):
    """Calcula a largura dos ombros em pixels para servir como métrica de escala."""
    left_shoulder = landmarks[left_idx]
    right_shoulder = landmarks[right_idx]
    return calculate_euclidean_distance(left_shoulder, right_shoulder, frame_width, frame_height)