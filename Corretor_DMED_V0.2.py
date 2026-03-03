## Programa para corrigir arquivos DMED, focado em dependentes (DTOP) sem CPF.
## Versão 0.2 - Com interface interativa e melhorias na usabilidade.
## Desenvolvido por: Heitor Leite - 2026

import os
import sys

class DmedProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = []

    def load_file(self):
        """Lê o arquivo de texto e armazena as linhas na memória."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.lines = [line.strip('\n') for line in f if line.strip('\n')]

    def save_file(self, output_path):
        """Salva as linhas corrigidas em um novo arquivo."""
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in self.lines:
                f.write(f"{line}\n")

    def scan_errors(self):
        """
        Varre o arquivo e retorna uma lista com os números das linhas com erro.
        Usa índice baseado em 1 para facilitar a leitura humana.
        """
        linhas_com_erro = []
        for i, line in enumerate(self.lines):
            fields = line.split('|')
            if len(fields) >= 6:
                tipo = fields[0]
                cpf = fields[2]
                
                # Identifica DTOP com CPF vazio
                if tipo == 'DTOP' and cpf.strip() == '':
                    linhas_com_erro.append(i + 1) # i + 1 representa a linha real no arquivo de texto
                    
        return linhas_com_erro

    def fix_missing_cpf_dtop(self):
        """Percorre o arquivo de baixo para cima corrigindo e removendo linhas problemáticas."""
        i = len(self.lines) - 1
        while i >= 0:
            line = self.lines[i]
            fields = line.split('|')

            if len(fields) >= 6:
                tipo = fields[0]
                cpf = fields[2]

                if tipo == 'DTOP' and cpf.strip() == '':
                    valor_dependente_str = fields[5]
                    tamanho_original = len(valor_dependente_str)
                    valor_dependente = int(valor_dependente_str) if valor_dependente_str.isdigit() else 0

                    # Busca o titular (TOP) correspondente
                    for j in range(i - 1, -1, -1):
                        titular_fields = self.lines[j].split('|')

                        if titular_fields[0] == 'TOP':
                            valor_titular_str = titular_fields[5]
                            valor_titular = int(valor_titular_str) if valor_titular_str.isdigit() else 0

                            novo_valor = valor_titular + valor_dependente
                            titular_fields[5] = str(novo_valor).zfill(tamanho_original)

                            self.lines[j] = '|'.join(titular_fields)
                            del self.lines[i]
                            break 
            i -= 1

    def process(self, output_path):
        """Orquestra o novo fluxo interativo de validação e correção."""
        print("\n[*] Lendo o arquivo e mapeando dados...")
        self.load_file()
        
        print("[*] Iniciando varredura de erros...")
        linhas_com_erro = self.scan_errors()
        total_erros = len(linhas_com_erro)
        
        # Camada 1: Verifica se não há erros
        if total_erros == 0:
            print("\n[+] Excelente! Nenhum erro de CPF em dependentes foi encontrado.")
            print("[*] Nenhuma correção é necessária. O programa será encerrado.")
            sys.exit(0)
            
        # Camada 2: Exibe os erros encontrados
        print(f"\n[!] Atenção: Foram encontrados {total_erros} erro(s) de CPF ausente (DTOP).")
        
        # Trava de segurança para não poluir o terminal com milhares de números
        if total_erros <= 50:
            print(f"Linhas com erro: {linhas_com_erro}")
        else:
            print(f"Linhas com erro (primeiras 50): {linhas_com_erro[:50]}")
            print(f"... e mais {total_erros - 50} linhas com erro ocultas para não travar o terminal.")
        
        # Camada 3: Confirmação do usuário
        print("-" * 50)
        confirmacao = input("Deseja realizar a correção e gerar o novo arquivo? (S/N): ").strip().upper()
        
        if confirmacao == 'S':
            print("\n[*] Aplicando correções (processando de baixo para cima)...")
            self.fix_missing_cpf_dtop()
            
            print(f"[*] Salvando o arquivo corrigido...")
            self.save_file(output_path)
            
            print(f"\n[+] Processamento concluído com sucesso!")
            print(f"[+] Arquivo limpo salvo em: {output_path}")
        else:
            print("\n[-] Operação cancelada pelo usuário. O programa será encerrado sem modificar nada.")
            sys.exit(0)


if __name__ == "__main__":
    print("--- Utilitário de Correção de DMED v0.2 ---")
    
    caminho_entrada = input("Digite o caminho completo do arquivo DMED original: ").strip('\"\'')
    if not os.path.exists(caminho_entrada):
        print("\n[!] Erro: Arquivo de entrada não encontrado. Verifique o caminho e tente novamente.")
        sys.exit(1)
        
    caminho_saida = input("Digite o caminho completo para salvar o arquivo corrigido: ").strip('\"\'')
    if os.path.isdir(caminho_saida):
        caminho_saida = os.path.join(caminho_saida, "DMED_Corrigido.txt")
        print(f"[*] Diretório detectado na saída. O arquivo será salvo como: {caminho_saida}")

    processor = DmedProcessor(caminho_entrada)
    processor.process(caminho_saida)