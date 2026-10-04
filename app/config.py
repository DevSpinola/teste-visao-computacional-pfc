# config.py
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

# Modelo "full" é mais preciso que o "lite" com corpo parcial (sentado, cortado pelo banco)
MODEL_PATH = str(PROJECT_DIR / 'pose_landmarker_full.task')

# Vídeo padrão (pode ser trocado pela linha de comando: python main.py outro.mp4 ou python main.py 0 para webcam)
VIDEO_PATH = str(APP_DIR / 'uber.mp4')

# Confiança mínima do MediaPipe (valores baixos aceitam esqueletos "fantasma")
MIN_DETECTION_CONFIDENCE = 0.5
MIN_PRESENCE_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# Visibilidade mínima de um pulso para ele contar
MIN_VISIBILITY = 0.5

# Máximo de pessoas procuradas no frame
MAX_POSES = 3

# Zonas dos bancos: retângulos (x1, y1, x2, y2) em coordenadas normalizadas (0 a 1).
# Cada câmera/vídeo precisa das suas zonas. Gere com: python calibrate.py <video>
# Valores abaixo: aproximados para uber.mp4 (câmera no para-brisa olhando para trás).
ZONES = {
    'motorista':         (0.45, 0.10, 1.00, 1.00),
    'banco_tras':        (0.12, 0.25, 0.45, 0.80),
    'passageiro_frente': (0.00, 0.25, 0.12, 1.00),
}

# Quanto tempo (segundos) um pulso precisa ficar na zona de outra pessoa para virar alerta
INVASION_SECONDS = 1.5
