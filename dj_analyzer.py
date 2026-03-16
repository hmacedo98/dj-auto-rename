import os
import sys
import essentia.standard as es

# Mapeamento completo para a Roda Camelot (Enarmonia tratada: C# = Db)
CAMELOT_MAP = {
    ('C', 'major'): '8B', ('C', 'minor'): '5A',
    ('C#', 'major'): '3B', ('C#', 'minor'): '12A',
    ('Db', 'major'): '3B', ('Db', 'minor'): '12A',
    ('D', 'major'): '10B', ('D', 'minor'): '7A',
    ('D#', 'major'): '5B', ('D#', 'minor'): '2A',
    ('Eb', 'major'): '5B', ('Eb', 'minor'): '2A',
    ('E', 'major'): '12B', ('E', 'minor'): '9A',
    ('F', 'major'): '7B', ('F', 'minor'): '4A',
    ('F#', 'major'): '2B', ('F#', 'minor'): '11A',
    ('Gb', 'major'): '2B', ('Gb', 'minor'): '11A',
    ('G', 'major'): '9B', ('G', 'minor'): '6A',
    ('G#', 'major'): '4B', ('G#', 'minor'): '1A',
    ('Ab', 'major'): '4B', ('Ab', 'minor'): '1A',
    ('A', 'major'): '11B', ('A', 'minor'): '8A',
    ('A#', 'major'): '6B', ('A#', 'minor'): '3A',
    ('Bb', 'major'): '6B', ('Bb', 'minor'): '3A',
    ('B', 'major'): '1B', ('B', 'minor'): '10A'
}

def exibir_creditos():
    print("="*60)
    print("        DJ HARMONIC RENAME TOOL - BY MACEDØ")
    print("="*60)
    print(" Este software utiliza a biblioteca Essentia para")
    print(" extração de BPM e Tonalidade de alta precisão.")
    print(" Saiba mais em: http://essentia.upf.edu")
    print("="*60)
    print("\n")

def processar_pasta(caminho_pasta):
    # Extensões suportadas pelo Essentia
    extensoes = ('.mp3', '.wav', '.flac', '.aiff', '.m4a')
    arquivos = [f for f in os.listdir(caminho_pasta) if f.lower().endswith(extensoes)]
    
    if not arquivos:
        print("[-] Nenhuma música encontrada na pasta selecionada.")
        return

    print(f"[*] Localizados {len(arquivos)} arquivos. Iniciando análise...\n")

    for nome_arquivo in arquivos:
        caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
        try:
            # Carregamento do áudio (Essentia MonoLoader)
            loader = es.MonoLoader(filename=caminho_completo)
            audio = loader()
            
            # Extração de BPM (RhythmExtractor2013)
            ritmo = es.RhythmExtractor2013()
            bpm_val, _, _, _, _ = ritmo(audio)
            bpm_final = int(round(bpm_val))
            
            # Extração de Tonalidade (KeyExtractor com Perfil EDMA para música eletrônica)
            extrator_tom = es.KeyExtractor(profileType='edma')
            tom, escala, _ = extrator_tom(audio)
            
            # Conversão para notação Camelot
            codigo_camelot = CAMELOT_MAP.get((tom, escala), "??")

            # Montagem do novo nome: [8B] [124BPM] - Nome Original.mp3
            extensao = os.path.splitext(nome_arquivo)[1]
            nome_limpo = os.path.splitext(nome_arquivo)[0]
            
            # Remove prefixos de análise anterior se existirem para evitar nomes duplicados
            if nome_limpo.startswith("["):
                # Tenta limpar nomes já processados anteriormente
                partes = nome_limpo.split(" - ", 1)
                if len(partes) > 1:
                    nome_limpo = partes[1]

            novo_nome = f"[{codigo_camelot}] [{bpm_final}BPM] - {nome_limpo}{extensao}"
            
            # Renomeação física do arquivo
            os.rename(caminho_completo, os.path.join(caminho_pasta, novo_nome))
            print(f"[OK] {codigo_camelot} | {bpm_final} BPM -> {nome_limpo}")

        except Exception as e:
            print(f"[ERRO] Falha ao processar {nome_arquivo}: {e}")

if __name__ == "__main__":
    exibir_creditos()
    
    # Input interativo para facilitar o uso no Windows
    input_caminho = input("Arraste a pasta com as músicas aqui e aperte ENTER: ").strip()
    
    # Limpeza básica do caminho (remove aspas se o usuário arrastar a pasta)
    pasta_alvo = input_caminho.replace('"', '').replace("'", "")

    if os.path.isdir(pasta_alvo):
        processar_pasta(pasta_alvo)
        print("\n" + "="*60)
        print(" CONCLUÍDO! Suas músicas foram organizadas harmonicamente.")
        print("="*60)
    else:
        print("[!] Erro: O caminho informado não é uma pasta válida.")

    input("\nPressione ENTER para fechar o programa...")
