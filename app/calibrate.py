# calibrate.py
# Desenha as zonas dos bancos com o mouse e imprime o bloco ZONES para colar no config.py.
# Uso:  python calibrate.py              (vídeo do config.py, frame no segundo 0)
#       python calibrate.py 0            (webcam)
#       python calibrate.py uber.mp4 10  (frame no segundo 10)
# Para cada zona: arraste o retângulo e aperte ENTER. Para pular uma zona, aperte ENTER sem desenhar.
import sys

import cv2

import config

source = sys.argv[1] if len(sys.argv) > 1 else config.VIDEO_PATH
second = float(sys.argv[2]) if len(sys.argv) > 2 else 0

cap = cv2.VideoCapture(int(source) if source.isdigit() else source)
cap.set(cv2.CAP_PROP_POS_MSEC, second * 1000)
ok, frame = cap.read()
cap.release()
if not ok:
    raise RuntimeError(f"Não foi possível ler o vídeo: {source}")

# Reduz a imagem para caber na tela (as coordenadas são normalizadas, então não muda nada)
scale = min(1.0, 1280 / frame.shape[1], 720 / frame.shape[0])
frame = cv2.resize(frame, None, fx=scale, fy=scale)
h, w = frame.shape[:2]

zones = {}
for name in config.ZONES:
    x, y, bw, bh = cv2.selectROI(f"Desenhe a zona '{name}' e aperte ENTER", frame, showCrosshair=False)
    cv2.destroyAllWindows()
    if bw == 0 or bh == 0:
        continue
    zones[name] = (round(x / w, 2), round(y / h, 2), round((x + bw) / w, 2), round((y + bh) / h, 2))
    cv2.rectangle(frame, (x, y), (x + bw, y + bh), (180, 180, 180), 2)
    cv2.putText(frame, name, (x + 5, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (180, 180, 180), 2)

print("\nCole no config.py:\n")
print("ZONES = {")
for name, box in zones.items():
    print(f"    '{name}': {box},")
print("}")
