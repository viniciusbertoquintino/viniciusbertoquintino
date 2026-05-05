# 🤘 Reconhecedor de Gestos com MediaPipe Hands

Detecta mãos em tempo real via webcam e reconhece gestos usando os 21 landmarks do **MediaPipe Hands** + **OpenCV**.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10%2B-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## ✋ Gestos reconhecidos

| Gesto | Dedos levantados |
|---|---|
| ✊ Punho fechado | Nenhum |
| ✋ Mão aberta | Todos (5) |
| 👍 Joinha | Só o polegar |
| ✌ Paz / V | Indicador + médio |
| ☝ Apontando | Só o indicador |
| 🤘 Rock | Indicador + mindinho |
| 3 dedos | Indicador + médio + anelar |

Suporta até **2 mãos simultaneamente** e exibe o FPS em tempo real.

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Webcam conectada

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/gesture-recognizer-mediapipe.git
cd gesture-recognizer-mediapipe

# 2. (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install opencv-python mediapipe
```

---

## ▶️ Como usar

```bash
python gesture_recognizer.py
```

- Aponte a câmera para sua mão
- O gesto detectado aparece em tempo real na tela
- Pressione **Q** para encerrar

---

## 🧠 Como funciona

O MediaPipe Hands retorna **21 pontos 3D (landmarks)** por mão:

```
                8   12  16  20
                |   |   |   |
                7   11  15  19
            4   6   10  14  18
            |   5   9   13  17
            3   |   |   |   |
            2   ----+---+---+
             \      |
              1     0 (WRIST)
```

Para cada dedo, o código verifica se a **ponta** está acima da **junta base (MCP)**:

```python
# Dedo levantado se a ponta estiver acima da base (y menor = mais alto na imagem)
fingers_up.append(landmarks[tip].y < landmarks[mcp].y)

# Polegar usa o eixo X (dobra lateralmente)
fingers_up.append(thumb_tip.x < thumb_ip.x)  # mão direita
```

---

## 📁 Estrutura do projeto

```
gesture-recognizer-mediapipe/
├── gesture_recognizer.py   # Script principal
└── README.md
```

---

## ➕ Adicionando novos gestos

Edite a função `get_gesture()` em `gesture_recognizer.py`:

```python
def get_gesture(count: int, fingers: list[bool]) -> str:
    f = fingers  # [polegar, indicador, médio, anelar, mindinho]

    # Exemplo: polegar + mindinho levantados = "Ligação 🤙"
    if f[0] and not f[1] and not f[2] and not f[3] and f[4]:
        return "Ligação 🤙"

    # ... outros gestos
```

---

## 📦 Dependências

| Biblioteca | Versão mínima | Função |
|---|---|---|
| `opencv-python` | 4.5+ | Captura de vídeo e renderização |
| `mediapipe` | 0.10+ | Detecção de mãos e landmarks |

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais detalhes.
