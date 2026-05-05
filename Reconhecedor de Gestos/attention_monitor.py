import cv2
import mediapipe as mp
import numpy as np
import time
import os
import urllib.request

from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

# ── Modelo FaceLandmarker ──────────────────────────────────────────────────────
FACE_MODEL_PATH = "face_landmarker.task"
FACE_MODEL_URL  = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"

if not os.path.exists(FACE_MODEL_PATH):
    print("Baixando modelo face_landmarker.task ...")
    urllib.request.urlretrieve(FACE_MODEL_URL, FACE_MODEL_PATH)
    print("Download concluído.")

# ── YOLO (opcional — só carrega se ultralytics estiver instalado) ──────────────
try:
    from ultralytics import YOLO
    yolo = YOLO("yolov8n.pt")   # baixa automaticamente na primeira execução
    YOLO_AVAILABLE = True
    PHONE_CLASS = 67            # índice COCO para "cell phone"
except ImportError:
    YOLO_AVAILABLE = False
    print("ultralytics não instalado — detecção de celular desativada.")
    print("  pip install ultralytics")

# ── Landmarks relevantes ───────────────────────────────────────────────────────
# EAR (Eye Aspect Ratio) — olho esquerdo e direito
L_EYE = [33, 160, 158, 133, 153, 144]
R_EYE = [362, 385, 387, 263, 373, 380]

# Pontos para estimativa de pose da cabeça (nose tip, chin, eye corners, mouth corners)
HEAD_POSE_PTS = [1, 152, 33, 263, 61, 291]

# Iris centers
L_IRIS = 468
R_IRIS = 473

# ── Parâmetros ─────────────────────────────────────────────────────────────────
EAR_THRESH       = 0.22   # abaixo disso = olho fechado
BLINK_FRAMES     = 3      # frames consecutivos fechados para contar piscada
YAW_THRESH       = 25     # graus — cabeça virada para o lado
PITCH_THRESH     = 20     # graus — cabeça baixa/alta
DISTRACT_SECONDS = 2.0    # segundos olhando fora para considerar "distraído"

# Modelo 3D canônico do rosto (pontos HEAD_POSE_PTS em mm)
MODEL_3D = np.array([
    [0.0,    0.0,    0.0   ],   # ponta do nariz
    [0.0,   -63.6,  -12.5 ],   # queixo
    [-43.3,  32.7,  -26.0 ],   # canto olho esquerdo
    [ 43.3,  32.7,  -26.0 ],   # canto olho direito
    [-28.9, -28.9,  -24.1 ],   # canto boca esquerdo
    [ 28.9, -28.9,  -24.1 ],   # canto boca direito
], dtype=np.float64)


# ── Helpers ────────────────────────────────────────────────────────────────────
def ear(landmarks, indices, w, h):
    pts = np.array([[landmarks[i].x * w, landmarks[i].y * h] for i in indices])
    A = np.linalg.norm(pts[1] - pts[5])
    B = np.linalg.norm(pts[2] - pts[4])
    C = np.linalg.norm(pts[0] - pts[3])
    return (A + B) / (2.0 * C + 1e-6)


def head_pose(landmarks, w, h):
    img_pts = np.array(
        [[landmarks[i].x * w, landmarks[i].y * h] for i in HEAD_POSE_PTS],
        dtype=np.float64,
    )
    focal = w
    cam_matrix = np.array([
        [focal, 0,     w / 2],
        [0,     focal, h / 2],
        [0,     0,     1    ],
    ], dtype=np.float64)
    dist = np.zeros((4, 1))

    ok, rvec, _ = cv2.solvePnP(MODEL_3D, img_pts, cam_matrix, dist,
                                flags=cv2.SOLVEPNP_ITERATIVE)
    if not ok:
        return 0.0, 0.0

    rot, _ = cv2.Rodrigues(rvec)
    # Extrai yaw e pitch dos ângulos de Euler
    pitch = np.degrees(np.arctan2(rot[2][1], rot[2][2]))
    yaw   = np.degrees(np.arctan2(-rot[2][0],
                                   np.sqrt(rot[2][1]**2 + rot[2][2]**2)))
    return yaw, pitch


def draw_bar(frame, x, y, w, h, ratio, color, label):
    cv2.rectangle(frame, (x, y), (x + w, y + h), (40, 40, 40), -1)
    fill = int(w * min(max(ratio, 0), 1))
    cv2.rectangle(frame, (x, y), (x + fill, y + h), color, -1)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 1)
    cv2.putText(frame, label, (x, y - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)


def draw_status(frame, label, value, y, ok_color=(0, 220, 100), bad_color=(0, 60, 220)):
    color = ok_color if value else bad_color
    text  = f"{label}: {'SIM' if value else 'NAO'}"
    cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)


# ── Estado global ──────────────────────────────────────────────────────────────
blink_counter    = 0
blink_total      = 0
eye_closed_frames = 0
distract_start   = None   # timestamp em que começou a distração
distracted_secs  = 0.0


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    global blink_counter, blink_total, eye_closed_frames, distract_start, distracted_secs

    base_opts = mp_python.BaseOptions(model_asset_path=FACE_MODEL_PATH)
    opts = mp_vision.FaceLandmarkerOptions(
        base_options=base_opts,
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        output_face_blendshapes=False,
        output_facial_transformation_matrixes=False,
        running_mode=mp_vision.RunningMode.VIDEO,
    )
    detector = mp_vision.FaceLandmarker.create_from_options(opts)

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
        h, w, _ = frame.shape

        rgb      = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        ts_ms    = int(time.time() * 1000)
        result   = detector.detect_for_video(mp_image, ts_ms)

        # ── Defaults ──
        attending  = False   # rosto detectado e olhando para frente
        focused    = False   # não piscando excessivamente + cabeça reta
        phone_seen = False   # celular detectado pelo YOLO

        yaw_deg = pitch_deg = 0.0
        ear_val = 1.0

        # ── Análise do rosto ──
        if result.face_landmarks:
            lms = result.face_landmarks[0]

            ear_l = ear(lms, L_EYE, w, h)
            ear_r = ear(lms, R_EYE, w, h)
            ear_val = (ear_l + ear_r) / 2.0

            # Blink
            if ear_val < EAR_THRESH:
                eye_closed_frames += 1
            else:
                if eye_closed_frames >= BLINK_FRAMES:
                    blink_total += 1
                eye_closed_frames = 0

            yaw_deg, pitch_deg = head_pose(lms, w, h)

            looking_forward = abs(yaw_deg) < YAW_THRESH and abs(pitch_deg) < PITCH_THRESH
            eyes_open       = ear_val >= EAR_THRESH

            attending = looking_forward and eyes_open

            # Foco: olhando para frente + não piscando continuamente
            focused = attending and (eye_closed_frames < BLINK_FRAMES)

            # Acumula tempo de distração
            if not attending:
                if distract_start is None:
                    distract_start = time.time()
                distracted_secs = time.time() - distract_start
            else:
                distract_start  = None
                distracted_secs = 0.0

            # Desenha pontos dos olhos
            for idx in L_EYE + R_EYE:
                cx, cy = int(lms[idx].x * w), int(lms[idx].y * h)
                cv2.circle(frame, (cx, cy), 2, (0, 255, 180), -1)

            # Iris
            for idx in [L_IRIS, R_IRIS]:
                cx, cy = int(lms[idx].x * w), int(lms[idx].y * h)
                cv2.circle(frame, (cx, cy), 5, (255, 200, 0), 1)

        # ── Detecção de celular (YOLO) ──
        if YOLO_AVAILABLE:
            yolo_results = yolo(frame, classes=[PHONE_CLASS], verbose=False, conf=0.45)
            for box in yolo_results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 80, 255), 2)
                cv2.putText(frame, "CELULAR", (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 80, 255), 2)
                phone_seen = True

        # ── Painel de status (canto superior esquerdo) ──
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (260, 230), (15, 15, 15), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        draw_status(frame, "Atencao",  attending,  30)
        draw_status(frame, "Foco",     focused,    60)
        draw_status(frame, "Celular",  not phone_seen, 90,
                    ok_color=(0, 220, 100), bad_color=(0, 60, 220))

        cv2.putText(frame, f"Yaw:   {yaw_deg:+.1f} graus", (10, 125),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (180, 180, 180), 1)
        cv2.putText(frame, f"Pitch: {pitch_deg:+.1f} graus", (10, 148),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (180, 180, 180), 1)
        cv2.putText(frame, f"EAR:   {ear_val:.2f}", (10, 171),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (180, 180, 180), 1)
        cv2.putText(frame, f"Piscadas: {blink_total}", (10, 194),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (180, 180, 180), 1)

        # Aviso de distração prolongada
        if distracted_secs >= DISTRACT_SECONDS:
            msg = f"DISTRAIDO há {distracted_secs:.0f}s!"
            (tw, _), _ = cv2.getTextSize(msg, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)
            cx = (w - tw) // 2
            cv2.putText(frame, msg, (cx, h - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 60, 255), 3)

        # Barra EAR
        draw_bar(frame, w - 170, 20, 150, 14,
                 ear_val / 0.4, (0, 200, 120), "EAR (olhos abertos)")

        # FPS
        now  = time.time()
        fps  = 1.0 / (now - prev_time + 1e-9)
        prev_time = now
        cv2.putText(frame, f"FPS: {fps:.1f}", (w - 100, h - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (150, 150, 150), 1)

        cv2.imshow("Monitor de Atencao - MediaPipe + YOLO", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    detector.close()


if __name__ == "__main__":
    main()
