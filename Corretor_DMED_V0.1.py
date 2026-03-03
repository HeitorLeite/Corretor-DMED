import os

class DmedProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = []

    def load_file(self):
        """Lê o arquivo de texto e armazena as linhas na memória."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            # Mantém a estrutura removendo apenas a quebra de linha invisível no final
            self.lines = [line.strip('\n') for line in f if line.strip('\n')]

    def save_file(self, output_path):
        """Salva as linhas corrigidas em um novo arquivo."""
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in self.lines:
                f.write(f"{line}\n")

    def fix_missing_cpf_dtop(self):
        """
        Percorre o arquivo de baixo para cima.
        Soma o valor do dependente (DTOP) sem CPF ao titular (TOP) e remove a linha defeituosa.
        """
        # Começa pelo índice da última linha do arquivo
        i = len(self.lines) - 1

        while i >= 0:
            line = self.lines[i]
            fields = line.split('|')

            # Garante que a linha possui os campos mínimos antes de tentar acessar os índices
            if len(fields) >= 6:
                tipo = fields[0]
                cpf = fields[2]

                # Identifica a regra 1: Linha DTOP com o CPF vazio
                if tipo == 'DTOP' and cpf.strip() == '':
                    valor_dependente_str = fields[5]
                    tamanho_original = len(valor_dependente_str)
                    
                    # Converte para inteiro de forma segura
                    valor_dependente = int(valor_dependente_str) if valor_dependente_str.isdigit() else 0

                    # Busca o titular (TOP) imediatamente acima desta linha
                    for j in range(i - 1, -1, -1):
                        titular_fields = self.lines[j].split('|')

                        if titular_fields[0] == 'TOP':
                            valor_titular_str = titular_fields[5]
                            valor_titular = int(valor_titular_str) if valor_titular_str.isdigit() else 0

                            # Realiza a soma do valor do titular com o do dependente
                            novo_valor = valor_titular + valor_dependente

                            # Formata preservando a quantidade de zeros à esquerda (ex: 001689)
                            titular_fields[5] = str(novo_valor).zfill(tamanho_original)

                            # Substitui a linha do titular pela versão com o valor atualizado
                            self.lines[j] = '|'.join(titular_fields)

                            # Remove a linha do dependente que estava sem CPF
                            del self.lines[i]
                            
                            # Interrompe a busca para cima, pois o titular correspondente já foi corrigido
                            break 

            # Move para a linha de cima
            i -= 1

    def process(self, output_path):
        """Orquestra o fluxo de leitura, aplicação das correções e salvamento."""
        self.load_file()
        
        # Aplica a correção de CPF ausente em dependentes
        self.fix_missing_cpf_dtop()
        
        # Espaço reservado para expandir e incluir novas chamadas de correção futuramente:
        # self.fix_outros_erros()
        
        self.save_file(output_path)
        print(f"\n[+] Processamento concluído com sucesso!")
        print(f"[+] Arquivo corrigido salvo em: {output_path}")

if __name__ == "__main__":
    import os
    print("--- Utilitário de Correção de DMED ---")
    caminho_entrada = input("Digite o caminho completo do arquivo DMED original: ").strip('\"\'')
    caminho_saida = input("Digite o caminho completo para salvar o arquivo corrigido: ").strip('\"\'')

    # Validação inteligente: se o usuário passar apenas o diretório, adicionamos um nome padrão
    if os.path.isdir(caminho_saida):
        caminho_saida = os.path.join(caminho_saida, "DMED_Corrigido.txt")
        print(f"[*] Diretório detectado na saída. O arquivo será salvo como: {caminho_saida}")

    if os.path.exists(caminho_entrada):
        processor = DmedProcessor(caminho_entrada)
        processor.process(caminho_saida)
    else:
        print("\n[!] Erro: Arquivo de entrada não encontrado. Verifique o caminho e tente novamente.")