# main.py
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import config as config
from geometry_utils import calculate_euclidean_distance, get_shoulder_width
from occupant_classifier import classify_occupants

def initialize_detector():
    base_options = python.BaseOptions(model_asset_path=config.MODEL_PATH)
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        num_poses=config.MAX_POSES,
        min_pose_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
        min_pose_presence_confidence=config.MIN_PRESENCE_CONFIDENCE,
        output_segmentation_masks=False
    )
    return vision.PoseLandmarker.create_from_options(options)

def process_frame(frame, detector):
    altura, largura, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    
    resultado = detector.detect(mp_image)

    if resultado.pose_landmarks and len(resultado.pose_landmarks) >= 2:
        # Classifica motorista (mais próximo) e passageiros
        motorista, passageiros = classify_occupants(resultado.pose_landmarks, largura, altura)

        # Avalia a interação do motorista com o primeiro passageiro identificado
        passageira = passageiros[0]

        pulso_dir_mot = motorista[config.KEYPOINT_RIGHT_WRIST]
        nariz_pas = passageira[config.KEYPOINT_NOSE]

        largura_ombros_pas = get_shoulder_width(passageira, largura, altura)

        if largura_ombros_pas > 0 and pulso_dir_mot.visibility > config.MIN_VISIBILITY:
            dist_bruta = calculate_euclidean_distance(pulso_dir_mot, nariz_pas, largura, altura)
            dist_relativa = dist_bruta / largura_ombros_pas

            px_m = int(pulso_dir_mot.x * largura)
            py_m = int(pulso_dir_mot.y * altura)

            # Checagem do Threshold de Invasão Espacial
            if dist_relativa < config.INVASION_THRESHOLD_RATIO:
                cor_alerta = (0, 0, 255) # Vermelho
                cv2.putText(frame, f"ALERTA: INVASAO ({dist_relativa:.2f})", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, cor_alerta, 2)
            else:
                cor_alerta = (0, 255, 0) # Verde

            cv2.circle(frame, (px_m, py_m), 10, cor_alerta, -1)

    return frame

def main():
    detector = initialize_detector()
    cap = cv2.VideoCapture(config.VIDEO_PATH)
    #cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError(f"Não foi possível abrir o vídeo: {config.VIDEO_PATH}")

    nome_janela = 'SDK - Monitoramento de Espaco'
    cv2.namedWindow(nome_janela, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    display_height = min(video_height, 720)
    display_width = round(display_height * video_width / video_height)
    cv2.resizeWindow(nome_janela, display_width, display_height)

    while cap.isOpened():
        sucesso, frame = cap.read()
        if not sucesso:
            break

        frame_processado = process_frame(frame, detector)
        cv2.imshow(nome_janela, frame_processado)

        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()