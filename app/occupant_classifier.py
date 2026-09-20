# occupant_classifier.py
from geometry_utils import get_shoulder_width

def classify_occupants(pose_landmarks_list, frame_width, frame_height):
    """
    Classifica o motorista como a pessoa com a maior escala (ombros mais largos em pixels),
    pois está no banco da frente e mais próximo da câmera do painel.
    """
    if not pose_landmarks_list:
        return None, []

    # Calcula a escala (largura dos ombros) de cada pessoa detectada
    poses_with_scale = []
    for pose in pose_landmarks_list:
        scale = get_shoulder_width(pose, frame_width, frame_height)
        poses_with_scale.append((scale, pose))

    # Ordena da maior escala (mais perto da câmera) para a menor
    poses_with_scale.sort(key=lambda item: item[0], reverse=True)

    driver = poses_with_scale[0][1]
    passengers = [item[1] for item in poses_with_scale[1:]]

    return driver, passengers