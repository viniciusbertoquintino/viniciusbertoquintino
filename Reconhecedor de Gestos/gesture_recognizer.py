import cv2
import mediapipe as mp
import time

# ── Inicialização ──────────────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
mp_style = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,   # modo vídeo (rastreamento contínuo)
    max_num_hands=2,           # detecta até 2 mãos
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)

# ── Nomes dos 21 landmarks ─────────────────────────────────────────────────────
LANDMARK_NAMES = [
    "WRIST",
    "THUMB_CMC", "THUMB_MCP", "THUMB_IP", "THUMB_TIP",
    "INDEX_FINGER_MCP", "INDEX_FINGER_PIP", "INDEX_FINGER_DIP", "INDEX_FINGER_TIP",
    "MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP",
    "RING_FINGER_MCP", "RING_FINGER_PIP", "RING_FINGER_DIP", "RING_FINGER_TIP",
    "PINKY_MCP", "PINKY_PIP", "PINKY_DIP", "PINKY_TIP",
]

# Índices das pontas e das juntas MCP (base) de cada dedo
FINGER_TIPS = [4, 8, 12, 16, 20]   # polegar, indicador, médio, anelar, mindinho
FINGER_MCP  = [2, 5,  9, 13, 17]   # juntas de referência (base)


# ── Lógica de contagem de dedos ────────────────────────────────────────────────
def count_fingers(landmarks, hand_label: str) -> tuple[int, list[bool]]:
    """
    Retorna (total_dedos_levantados, lista_booleana_por_dedo).
    hand_label: 'Left' ou 'Right' (label retornado pelo MediaPipe).
    """
    fingers_up = []

    # Polegar: compara x em vez de y (eixo horizontal)
    thumb_tip = landmarks[FINGER_TIPS[0]]
    thumb_ip  = landmarks[FINGER_MCP[0]]

    # MediaPipe usa "Left"/"Right" do ponto de vista da câmera (espelhado)
    if hand_label == "Right":
        fingers_up.append(thumb_tip.x < thumb_ip.x)
    else:
        fingers_up.append(thumb_tip.x > thumb_ip.x)

    # Demais 4 dedos: ponta acima da junta PIP (eixo y invertido)
    for tip_idx, mcp_idx in zip(FINGER_TIPS[1:], FINGER_MCP[1:]):
        fingers_up.append(landmarks[tip_idx].y < landmarks[mcp_idx].y)

    return sum(fingers_up), fingers_up


# ── Mapeamento de gestos ───────────────────────────────────────────────────────
def get_gesture(count: int, fingers: list[bool]) -> str:
    """Interpreta gestos comuns a partir da contagem e posição dos dedos."""
    f = fingers  # alias curto

    # Punho fechado
    if count == 0:
        return "Punho fechado ✊"

    # Mão aberta
    if count == 5:
        return "Mao aberta ✋"

    # Polegar pra cima (só polegar levantado)
    if f[0] and not any(f[1:]):
        return "Joinha 👍"

    # Polegar pra baixo (nenhum dedo, mas o polegar não foi contado — raro, deixamos como referência)

    # V (indicador + médio)
    if not f[0] and f[1] and f[2] and not f[3] and not f[4]:
        return "Paz / V ✌"

    # Apontando (só indicador)
    if not f[0] and f[1] and not f[2] and not f[3] and not f[4]:
        return "Apontando ☝"

    # Rock (indicador + mindinho)
    if not f[0] and f[1] and not f[2] and not f[3] and f[4]:
        return "Rock 🤘"

    # OK (polegar + indicador com os demais dobrados) — simplificado pela contagem
    if f[0] and f[1] and not f[2] and not f[3] and not f[4]:
        return "OK 👌 (aprox.)"

    # Três dedos (indicador + médio + anelar)
    if not f[0] and f[1] and f[2] and f[3] and not f[4]:
        return "Tres dedos"

    return f"{count} dedo(s)"


# ── Utilitário de overlay ──────────────────────────────────────────────────────
def draw_info(frame, gesture: str, count: int, hand_label: str, fps: float, x: int, y: int):
    """Desenha caixa de texto estilizada sobre o frame."""
    label = f"{hand_label}  |  {gesture}  |  {count}/5 dedos"
    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)

    pad = 8
    rx, ry = x - pad, y - th - pad * 2
    cv2.rectangle(frame, (rx, ry), (rx + tw + pad * 2, y + pad), (20, 20, 20), -1)
    cv2.rectangle(frame, (rx, ry), (rx + tw + pad * 2, y + pad), (0, 200, 120), 2)
    cv2.putText(frame, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 160), 2)

    # FPS no canto superior esquerdo
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)


# ── Loop principal ─────────────────────────────────────────────────────────────
def main():
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

        # Espelha para parecer com um espelho
        frame = cv2.flip(frame, 1)

        # Converte BGR → RGB (MediaPipe exige RGB)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False          # pequena otimização
        results = hands.process(rgb)
        rgb.flags.writeable = True

        # ── Processa cada mão detectada ──
        if results.multi_hand_landmarks:
            for hand_lms, hand_info in zip(
                results.multi_hand_landmarks,
                results.multi_handedness,
            ):
                # Desenha os 21 pontos e conexões
                mp_draw.draw_landmarks(
                    frame,
                    hand_lms,
                    mp_hands.HAND_CONNECTIONS,
                    mp_style.get_default_hand_landmarks_style(),
                    mp_style.get_default_hand_connections_style(),
                )

                # Label: "Left" ou "Right" (do MediaPipe)
                label = hand_info.classification[0].label

                lms = hand_lms.landmark
                count, fingers = count_fingers(lms, label)
                gesture = get_gesture(count, fingers)

                # Posição do pulso para ancorar o texto
                h, w, _ = frame.shape
                wx = int(lms[0].x * w)
                wy = int(lms[0].y * h)
                text_y = max(wy - 30, 60)

                draw_info(frame, gesture, count, label, 0, wx, text_y)

        # FPS real
        now = time.time()
        fps = 1.0 / (now - prev_time + 1e-9)
        prev_time = now
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

        cv2.imshow("Reconhecedor de Gestos — MediaPipe Hands", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    hands.close()


if __name__ == "__main__":
    main()
