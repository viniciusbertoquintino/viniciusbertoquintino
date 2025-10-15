# 🎵 Conversor de Vídeo para MP3

Um conversor robusto e flexível de arquivos de vídeo para formato MP3 usando Python e MoviePy.

## ✨ Funcionalidades

- ✅ **Conversão de arquivo único** - Converte um vídeo específico para MP3
- ✅ **Conversão em lote** - Converte todos os vídeos de um diretório
- ✅ **Múltiplos formatos** - Suporta MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V
- ✅ **Controle de qualidade** - Permite ajustar a taxa de bits (bitrate)
- ✅ **Caminhos flexíveis** - Suporte a caminhos absolutos, relativos e variáveis de ambiente
- ✅ **Interface de linha de comando** - Fácil de usar via terminal
- ✅ **Tratamento de erros** - Validações e mensagens de erro claras
- ✅ **Modo verboso** - Logs detalhados do processo

## 🚀 Instalação

```bash
pip install -r requirements_video_to_mp3.txt
```

## 📖 Como Usar

### Opções de Entrada

| Opção | Descrição | Exemplo |
|-------|-----------|---------|
| `arquivo.mp4` | Arquivo posicional (compatibilidade) | `python video_to_mp3.py video.mp4` |
| `-i, --input` | Arquivo de entrada | `python video_to_mp3.py -i video.mp4` |
| `-d, --directory` | Diretório de entrada (lote) | `python video_to_mp3.py -d /videos` |
| `--input-dir` | Diretório de entrada (lote) | `python video_to_mp3.py --input-dir /videos` |

### Opções de Saída

| Opção | Descrição | Exemplo |
|-------|-----------|---------|
| `-o, --output` | Arquivo ou diretório de saída | `python video_to_mp3.py -i video.mp4 -o audio.mp3` |
| `--output-dir` | Diretório de saída (lote) | `python video_to_mp3.py -d /videos --output-dir /audios` |

### Outras Opções

| Opção | Descrição | Padrão |
|-------|-----------|--------|
| `-b, --bitrate` | Taxa de bits do MP3 | `192k` |
| `-v, --verbose` | Modo verboso | `False` |

## 💡 Exemplos de Uso

### Conversão Básica
```bash
# Conversão simples
python video_to_mp3.py video.mp4

# Especificando arquivo de saída
python video_to_mp3.py video.mp4 -o audio.mp3
```

### Caminhos Completos
```bash
# Usando caminhos absolutos
python video_to_mp3.py -i /caminho/entrada/video.mp4 -o /caminho/saida/audio.mp3

# Usando variáveis de ambiente
python video_to_mp3.py -i $HOME/Videos/video.mp4 -o $HOME/Music/audio.mp3

# No Windows
python video_to_mp3.py -i %USERPROFILE%\\Videos\\video.mp4 -o %USERPROFILE%\\Music\\audio.mp3
```

### Conversão em Lote
```bash
# Converter todos os vídeos de uma pasta
python video_to_mp3.py -d /caminho/para/videos

# Com diretório de saída específico
python video_to_mp3.py -d /videos -o /audios

# Usando as opções longas
python video_to_mp3.py --input-dir /videos --output-dir /audios
```

### Controle de Qualidade
```bash
# Qualidade básica (arquivo menor)
python video_to_mp3.py video.mp4 -b 128k

# Qualidade alta (arquivo maior)
python video_to_mp3.py video.mp4 -b 320k

# Combinando opções
python video_to_mp3.py -i video.mp4 -o audio.mp3 -b 256k -v
```

### Modo Verboso
```bash
# Ver detalhes do processo
python video_to_mp3.py video.mp4 -v

# Em lote com detalhes
python video_to_mp3.py -d /videos --output-dir /audios -v
```

## 🎵 Bitrates Recomendados

| Bitrate | Qualidade | Tamanho | Uso Recomendado |
|---------|-----------|---------|-----------------|
| `128k` | Básica | Pequeno | Podcasts, fala |
| `192k` | Boa | Médio | Música geral (padrão) |
| `256k` | Alta | Grande | Música de qualidade |
| `320k` | Máxima | Muito grande | Arquivo master |

## 🔧 Recursos Técnicos

- **Normalização de Caminhos**: Expande variáveis de ambiente (`$HOME`, `%USERPROFILE%`) e `~`
- **Caminhos Absolutos**: Converte automaticamente para caminhos absolutos
- **Validação**: Verifica existência de arquivos e diretórios
- **Gerenciamento de Memória**: Fecha arquivos automaticamente após uso
- **Tratamento de Erros**: Continua processamento mesmo com erros individuais
- **Logs Detalhados**: Informações completas do processo (modo verboso)

## 📁 Estrutura de Arquivos

```
video_to_mp3/
├── video_to_mp3.py              # Script principal
├── requirements_video_to_mp3.txt # Dependências
└── README.md                    # Esta documentação
```

## ⚠️ Requisitos

- Python 3.6+
- MoviePy
- FFmpeg (instalado no sistema)

## 🐛 Solução de Problemas

### Erro: "FFmpeg not found"
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Baixar de https://ffmpeg.org/download.html
```

### Erro: "MoviePy not found"
```bash
pip install moviepy
```

### Arquivo não encontrado
- Verifique se o caminho está correto
- Use caminhos absolutos se necessário
- No Windows, use barras duplas (`\\`) ou barras normais (`/`)

## 📝 Licença

Este projeto é de código aberto e pode ser usado livremente.
