import cv2
import mediapipe as mp
import time
import urllib.request
import os

from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
from mediapipe.tasks.python.components.containers import landmark as lm_module

# ── Modelo ─────────────────────────────────────────────────────────────────────
MODEL_PATH = "hand_landmarker.task"
MODEL_URL   = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"

if not os.path.exists(MODEL_PATH):
    print("Baixando modelo hand_landmarker.task ...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Download concluído.")

# ── Índices dos landmarks ──────────────────────────────────────────────────────
FINGER_TIPS = [4, 8, 12, 16, 20]
FINGER_MCP  = [2, 5,  9, 13, 17]

# Conexões para desenhar o esqueleto da mão manualmente
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17),
]


# ── Lógica de contagem de dedos ────────────────────────────────────────────────
def count_fingers(landmarks, hand_label: str) -> tuple[int, list[bool]]:
    fingers_up = []

    thumb_tip = landmarks[FINGER_TIPS[0]]
    thumb_ip  = landmarks[FINGER_MCP[0]]

    if hand_label == "Right":
        fingers_up.append(thumb_tip.x < thumb_ip.x)
    else:
        fingers_up.append(thumb_tip.x > thumb_ip.x)

    for tip_idx, mcp_idx in zip(FINGER_TIPS[1:], FINGER_MCP[1:]):
        fingers_up.append(landmarks[tip_idx].y < landmarks[mcp_idx].y)

    return sum(fingers_up), fingers_up


# ── Mapeamento de gestos ───────────────────────────────────────────────────────
def get_gesture(count: int, fingers: list[bool]) -> str:
    f = fingers

    if count == 0:
        return "Punho fechado"
    if count == 5:
        return "Mao aberta"
    if f[0] and not any(f[1:]):
        return "Joinha"
    if not f[0] and f[1] and f[2] and not f[3] and not f[4]:
        return "Paz / V"
    if not f[0] and f[1] and not f[2] and not f[3] and not f[4]:
        return "Apontando"
    if not f[0] and f[1] and not f[2] and not f[3] and f[4]:
        return "Rock"
    if f[0] and f[1] and not f[2] and not f[3] and not f[4]:
        return "OK (aprox.)"
    if not f[0] and f[1] and f[2] and f[3] and not f[4]:
        return "Tres dedos"

    return f"{count} dedo(s)"


# ── Desenho dos landmarks ──────────────────────────────────────────────────────
def draw_landmarks(frame, landmarks):
    h, w, _ = frame.shape
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

    for a, b in HAND_CONNECTIONS:
        cv2.line(frame, pts[a], pts[b], (0, 200, 120), 2)
    for x, y in pts:
        cv2.circle(frame, (x, y), 4, (255, 255, 255), -1)
        cv2.circle(frame, (x, y), 4, (0, 150, 90), 1)


# ── Overlay de informações ─────────────────────────────────────────────────────
def draw_info(frame, gesture: str, count: int, hand_label: str, x: int, y: int):
    label = f"{hand_label}  |  {gesture}  |  {count}/5 dedos"
    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)

    pad = 8
    rx, ry = x - pad, y - th - pad * 2
    cv2.rectangle(frame, (rx, ry), (rx + tw + pad * 2, y + pad), (20, 20, 20), -1)
    cv2.rectangle(frame, (rx, ry), (rx + tw + pad * 2, y + pad), (0, 200, 120), 2)
    cv2.putText(frame, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 160), 2)


# ── Loop principal ─────────────────────────────────────────────────────────────
def main():
    base_opts = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
    opts = mp_vision.HandLandmarkerOptions(
        base_options=base_opts,
        num_hands=2,
        min_hand_detection_confidence=0.7,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        running_mode=mp_vision.RunningMode.VIDEO,
    )
    detector = mp_vision.HandLandmarker.create_from_options(opts)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: nao foi possivel abrir a webcam.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    prev_time = time.time()
    print("Pressione  Q  para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        timestamp_ms = int(time.time() * 1000)
        result = detector.detect_for_video(mp_image, timestamp_ms)

        if result.hand_landmarks:
            for landmarks, handedness in zip(result.hand_landmarks, result.handedness):
                hand_label = handedness[0].display_name  # "Left" ou "Right"

                draw_landmarks(frame, landmarks)

                count, fingers = count_fingers(landmarks, hand_label)
                gesture = get_gesture(count, fingers)

                h, w, _ = frame.shape
                wx = int(landmarks[0].x * w)
                wy = int(landmarks[0].y * h)
                text_y = max(wy - 30, 60)

                draw_info(frame, gesture, count, hand_label, wx, text_y)

        now = time.time()
        fps = 1.0 / (now - prev_time + 1e-9)
        prev_time = now
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

        cv2.imshow("Reconhecedor de Gestos - MediaPipe Hands", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    detector.close()


if __name__ == "__main__":
    main()
