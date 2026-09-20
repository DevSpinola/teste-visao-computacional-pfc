import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 1. Configurar o Pose Landmarker com o modelo baixado
base_options = python.BaseOptions(model_asset_path='pose_landmarker_lite.task')
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    num_poses=2,
    min_pose_detection_confidence=0.2, # Força a IA a ser menos rígida na detecção inicial
    min_pose_presence_confidence=0.3,  # Força a IA a ser menos rígida no rastreamento contínuo
    output_segmentation_masks=False
)
detector = vision.PoseLandmarker.create_from_options(options)

# # 2. Carregar o arquivo de vídeo
# cap = cv2.VideoCapture('before_sunrise_trem.mp4')

# 2. Abrir a webcam (0 = câmera padrão; tente 1 se houver mais de uma)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Não foi possível abrir a webcam.")

while cap.isOpened():
    sucesso, frame = cap.read()
    if not sucesso:
        print("Fim do vídeo ou arquivo não encontrado.")
        break

    # O MediaPipe moderno trabalha com objetos mp.Image em RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

    # 3. Detectar os keypoints
    resultado = detector.detect(mp_image)

    # 4. Processar coordenadas geométricas se encontrar alguma pessoa
    if resultado.pose_landmarks:
        # Pega a primeira pessoa identificada no frame
        for landmarks in resultado.pose_landmarks:            
            
            # Ponto 16 = Pulso Direito (Right Wrist)
            nariz = landmarks[0]
            ombro_direito = landmarks[12]
            ombro_esquerdo = landmarks[11]
            pulso_direito = landmarks[16]
            pulso_esquerdo = landmarks[15]
            # É sempre bom manter a trava de visibilidade para evitar falsos positivos
            if nariz.visibility > 0.1:
                altura, largura, _ = frame.shape
                pos_x = int(nariz.x * largura)
                pos_y = int(nariz.y * altura)

                print(f"Nariz -> X: {pos_x}, Y: {pos_y}")

                # Desenhar um círculo vermelho no pulso direito
                cv2.circle(frame, (pos_x, pos_y), 8, (0, 0, 255), -1)
            if ombro_direito.visibility > 0.1:
                altura, largura, _ = frame.shape
                pos_x = int(ombro_direito.x * largura)
                pos_y = int(ombro_direito.y * altura)

                print(f"Ombro Direito -> X: {pos_x}, Y: {pos_y}")

                # Desenhar um círculo azul no ombro direito
                cv2.circle(frame, (pos_x, pos_y), 8, (255, 0, 0), -1)
            if ombro_esquerdo.visibility > 0.1:
                altura, largura, _ = frame.shape
                pos_x = int(ombro_esquerdo.x * largura)
                pos_y = int(ombro_esquerdo.y * altura)

                print(f"Ombro Esquerdo -> X: {pos_x}, Y: {pos_y}")

                # Desenhar um círculo verde no ombro esquerdo
                cv2.circle(frame, (pos_x, pos_y), 8, (0, 255, 0), -1)
            if pulso_direito.visibility > 0.1:
                altura, largura, _ = frame.shape
                pos_x = int(pulso_direito.x * largura)
                pos_y = int(pulso_direito.y * altura)

                print(f"Pulso Direito -> X: {pos_x}, Y: {pos_y}")

                # Desenhar um círculo amarelo no pulso direito
                cv2.circle(frame, (pos_x, pos_y), 8, (0, 255, 255), -1)
            if pulso_esquerdo.visibility > 0.1:
                altura, largura, _ = frame.shape
                pos_x = int(pulso_esquerdo.x * largura)
                pos_y = int(pulso_esquerdo.y * altura)

                print(f"Pulso Esquerdo -> X: {pos_x}, Y: {pos_y}")

                # Desenhar um círculo roxo no pulso esquerdo
                cv2.circle(frame, (pos_x, pos_y), 8, (255, 0, 255), -1)

    cv2.imshow('MediaPipe 1.0 - Pose Tracking', frame)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()