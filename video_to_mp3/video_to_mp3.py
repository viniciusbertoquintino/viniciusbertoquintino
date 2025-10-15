#!/usr/bin/env python3
"""
Conversor de Vídeo para MP3
Converte arquivos de vídeo para formato de áudio MP3 usando moviepy
"""

import os
import sys
import argparse
from pathlib import Path
from moviepy.editor import VideoFileClip
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_video_to_mp3(video_path, output_path=None, bitrate="192k"):
    """
    Converte um arquivo de vídeo para MP3
    
    Args:
        video_path (str): Caminho para o arquivo de vídeo
        output_path (str, optional): Caminho de saída. Se None, usa o mesmo nome do vídeo
        bitrate (str): Taxa de bits do MP3 (padrão: 192k)
    
    Returns:
        str: Caminho do arquivo MP3 criado
    """
    try:
        # Verificar se o arquivo de vídeo existe
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Arquivo de vídeo não encontrado: {video_path}")
        
        # Definir caminho de saída se não especificado
        if output_path is None:
            video_name = Path(video_path).stem
            output_path = f"{video_name}.mp3"
        
        logger.info(f"Iniciando conversão: {video_path} -> {output_path}")
        
        # Carregar o vídeo
        video = VideoFileClip(video_path)
        
        # Extrair áudio e converter para MP3
        audio = video.audio
        audio.write_audiofile(
            output_path,
            bitrate=bitrate,
            verbose=False,
            logger=None
        )
        
        # Fechar os objetos para liberar memória
        audio.close()
        video.close()
        
        logger.info(f"Conversão concluída com sucesso: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Erro durante a conversão: {str(e)}")
        raise

def batch_convert(directory_path, output_dir=None, bitrate="192k"):
    """
    Converte todos os vídeos de um diretório para MP3
    
    Args:
        directory_path (str): Caminho do diretório com vídeos
        output_dir (str, optional): Diretório de saída. Se None, usa o mesmo diretório
        bitrate (str): Taxa de bits do MP3
    
    Returns:
        list: Lista de arquivos MP3 criados
    """
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Diretório não encontrado: {directory_path}")
    
    # Formatos de vídeo suportados
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v']
    
    # Encontrar todos os arquivos de vídeo
    video_files = []
    for file in os.listdir(directory_path):
        if any(file.lower().endswith(ext) for ext in video_extensions):
            video_files.append(os.path.join(directory_path, file))
    
    if not video_files:
        logger.warning("Nenhum arquivo de vídeo encontrado no diretório")
        return []
    
    logger.info(f"Encontrados {len(video_files)} arquivos de vídeo para converter")
    
    # Criar diretório de saída se especificado
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    converted_files = []
    for video_file in video_files:
        try:
            # Definir caminho de saída
            if output_dir:
                filename = Path(video_file).stem + ".mp3"
                output_path = os.path.join(output_dir, filename)
            else:
                output_path = None
            
            # Converter
            mp3_file = convert_video_to_mp3(video_file, output_path, bitrate)
            converted_files.append(mp3_file)
            
        except Exception as e:
            logger.error(f"Erro ao converter {video_file}: {str(e)}")
            continue
    
    return converted_files

def main():
    """Função principal com interface de linha de comando"""
    parser = argparse.ArgumentParser(
        description="Converte arquivos de vídeo para MP3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python video_to_mp3.py video.mp4
  python video_to_mp3.py video.mp4 -o audio.mp3
  python video_to_mp3.py video.mp4 -b 320k
  python video_to_mp3.py -d /caminho/para/videos -o /caminho/saida
        """
    )
    
    # Argumentos
    parser.add_argument(
        'input',
        nargs='?',
        help='Arquivo de vídeo ou diretório para converter'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Arquivo ou diretório de saída'
    )
    
    parser.add_argument(
        '-d', '--directory',
        help='Converter todos os vídeos de um diretório'
    )
    
    parser.add_argument(
        '-b', '--bitrate',
        default='192k',
        help='Taxa de bits do MP3 (padrão: 192k)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Modo verboso'
    )
    
    args = parser.parse_args()
    
    # Configurar logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        if args.directory:
            # Conversão em lote
            converted_files = batch_convert(args.directory, args.output, args.bitrate)
            print(f"\n✅ Conversão em lote concluída!")
            print(f"📁 {len(converted_files)} arquivos convertidos:")
            for file in converted_files:
                print(f"   • {file}")
                
        elif args.input:
            # Conversão de arquivo único
            mp3_file = convert_video_to_mp3(args.input, args.output, args.bitrate)
            print(f"\n✅ Conversão concluída com sucesso!")
            print(f"🎵 Arquivo MP3 criado: {mp3_file}")
            
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n❌ Operação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
