import csv
import json
from datetime import datetime

def processar_vagas():
    # Agora ele vai ler o CSV que você salvou no Excel
    arquivo_entrada = "vagas.csv" 
    arquivo_saida = "vagas.json"
    
    vagas_processadas = []
    hoje = datetime.now().date()
    
    print(f"Lendo o arquivo: {arquivo_entrada}...")

    try:
        # Abre o arquivo tentando UTF-8 primeiro
        try:
            f = open(arquivo_entrada, mode='r', encoding='utf-8')
            primeira_linha = f.readline()
            f.seek(0)
        except UnicodeDecodeError:
            f = open(arquivo_entrada, mode='r', encoding='latin-1')
            primeira_linha = f.readline()
            f.seek(0)

        # Detecta automaticamente se o Excel brasileiro salvou com ponto-e-vírgula ou vírgula
        delimitador = ';' if ';' in primeira_linha else ','
        leitor = csv.reader(f, delimiter=delimitador)
        
        for linha in leitor:
            # Pula cabeçalhos ou linhas curtas
            if len(linha) < 15:
                continue
                
            # Pula a linha que contém os nomes das colunas
            if "Código" in str(linha[2]) or "Ocupação" in str(linha[3]):
                continue

            try:
                cargo = linha[3].strip().upper()
                empresa = linha[6].strip().upper()
                status = linha[10].strip().lower()
                qtd_vagas = linha[11].strip()
                flexibilizada = linha[13].strip().lower()
                data_vencimento_str = linha[14].strip()

                # Só processa se a vaga estiver 'aberta'
                if status != 'aberta':
                    continue

                # Trava de Segurança: Ignora vagas vencidas
                data_vencimento = datetime.strptime(data_vencimento_str, "%d/%m/%Y").date()
                if data_vencimento >= hoje:
                    vagas_processadas.append({
                        "cargo": cargo,
                        "empresa": empresa,
                        "qtd": qtd_vagas,
                        "vencimento": data_vencimento_str,
                        "pcd": True if flexibilizada == 'sim' else False
                    })
            except Exception as e:
                # Ignora linhas em branco ou mal formatadas no final do relatório
                continue

        f.close()

        # Ordena em ordem alfabética para ficar organizado no celular do candidato
        vagas_processadas = sorted(vagas_processadas, key=lambda x: x['cargo'])

        # Cria o arquivo JSON
        with open(arquivo_saida, 'w', encoding='utf-8') as jf:
            json.dump(vagas_processadas, jf, ensure_ascii=False, indent=4)

        print(f"✅ Sucesso! {len(vagas_processadas)} vagas ATIVAS prontas para o GitHub.")

    except FileNotFoundError:
        print(f"❌ ERRO: O arquivo '{arquivo_entrada}' não foi encontrado.")
        print("Lembre-se de abrir o .xls do MTE no Excel e 'Salvar Como -> CSV'.")

if __name__ == "__main__":
    processar_vagas()