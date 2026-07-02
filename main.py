import os
import glob
import logging
from core import ServicoEmail

logging.basicConfig(level=logging.INFO)

def localizar_arquivo_excel():
    """Busca arquivos .xlsx na pasta do projeto de forma dinâmica."""
    arquivos = glob.glob("*.xlsx") + glob.glob("*.xls")
    
    if not arquivos:
        print("Nenhum arquivo Excel encontrado na pasta do projeto.")
        caminho = input("Digite o nome ou o caminho do seu arquivo Excel manualmente: ").strip()
        if os.path.exists(caminho):
            return caminho
        logging.error("Arquivo não encontrado. Encerrando script.")
        return None
            
    if len(arquivos) == 1:
        logging.info(f"Arquivo detectado automaticamente: {arquivos[0]}")
        return arquivos[0]
        
    print("\nVários arquivos Excel foram encontrados:")
    for idx, arquivo in enumerate(arquivos, start=1):
        print(f"[{idx}] {arquivo}")
        
    try:
        escolha = int(input("\nDigite o número do arquivo que deseja processar: "))
        if 1 <= escolha <= len(arquivos):
            return arquivos[escolha - 1]
    except ValueError:
        pass
        
    logging.error("Seleção inválida. Encerrando script.")
    return None

def main():
    logging.info("=== Serviço de E-mail de Advertências Iniciado ===")
    
    caminho_arquivo = localizar_arquivo_excel()
    
    if caminho_arquivo:
        ServicoEmail.processar_e_enviar(caminho_arquivo)
    
    logging.info("=== Execução Finalizada ===")

if __name__ == "__main__":
    main()