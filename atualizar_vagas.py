import csv
import json
from datetime import datetime
import os

def processar_vagas():
    arquivo_entrada = "ConsultaVagasPorCriterios.csv" # Mude para o nome exato do seu arquivo
    arquivo_saida = "vagas.json"
    
    vagas_processadas = []
    hoje = datetime.now().date()
    
    print(f"Lendo o arquivo: {arquivo_entrada}...")

    # Usando latin-1 ou cp1252 porque sistemas do governo costumam usar esse padrão no Windows
    try:
        f = open(arquivo_entrada, mode='r', encoding='utf-8')
        f.read()
        f.seek(0)
    except UnicodeDecodeError:
        f = open(arquivo_entrada, mode='r', encoding='latin-1')

    leitor = csv.reader(f)
    
    for linha in leitor:
        # Pula as linhas de cabeçalho (que têm poucas colunas)
        if len(linha) < 15:
            continue
            
        # Pula a linha que contém os nomes das colunas
        if "Código" in linha[2] or "Ocupação" in linha[3]:
            continue

        try:
            # Mapeamento baseado no arquivo do IMO que você enviou
            cargo = linha[3].strip().upper()
            empresa = linha[6].strip().upper()
            status = linha[10].strip().lower()
            qtd_vagas = linha[11].strip()
            flexibilizada = linha[13].strip().lower() # Se "Sim", geralmente aceita PCD
            data_vencimento_str = linha[14].strip()

            # Só processa se a vaga estiver 'aberta'
            if status != 'aberta':
                continue

            # Verifica se a vaga está no prazo
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
            # Ignora linhas em branco ou mal formatadas no final do arquivo
            continue

    f.close()

    # Ordena as vagas em ordem alfabética pelo Cargo
    vagas_processadas = sorted(vagas_processadas, key=lambda x: x['cargo'])

    # Salva no formato JSON para o site ler
    with open(arquivo_saida, 'w', encoding='utf-8') as jf:
        json.dump(vagas_processadas, jf, ensure_ascii=False, indent=4)

    print(f"✅ Sucesso! {len(vagas_processadas)} vagas válidas foram salvas no '{arquivo_saida}'.")

if __name__ == "__main__":
    processar_vagas()