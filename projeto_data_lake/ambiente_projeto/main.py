import pandas as pd
import os
import glob
import json

   # Varável com o caminho dos arquivos
folder_path = "data_lake\Raw"

  # Glob para ler todos os arquivos com final .xlsx que vieram da base de dados de sistemas transacionais
arquivos_excel = glob.glob(os.path.join(folder_path, '*.xlsx'))

if not arquivos_excel:
    print("Nenhum arquivo excel encontrado")
else:

    dfs = []

    for arquivo in arquivos_excel:
       
        try: # Ler arquivo de excel
             df_temp = pd.read_excel(arquivo)
             
             # Pegar o nome do arquivo
             file_name = os.path.basename(arquivo)

             # Iniciando o tratamento de dados  - Criando uma nova coluna de nome Estado e manipulando os dados adcionando novas colunas 
             if 'bahia' in file_name.lower():
                 df_temp['Estado'] = 'BA'
             elif 'distrito' in file_name.lower():
                 df_temp['Estado'] = 'DF'
             elif 'minasgerais' in file_name.lower():
                 df_temp['Estado'] = 'MG'
             elif 'saopaulo' in file_name.lower():
                 df_temp['Estado'] = 'SP'

             df_temp['campanha'] = df_temp['utm_link'].str.extract(r'utm_campaign=(.*)')

             # Guarda os Arquivos tratados dentro de um DataFrame
             dfs.append(df_temp)

        # Tratamento de erro na leitura de arquivo  
        except Exception as e:
            print(f"Erro ao ler o arquivo: {arquivo} - {e}")
    
    if dfs:

        # Concatena todas as tabelas salvas no dfs em uma única tabela para importar dados em software de tomada de decisão
        result = pd.concat(dfs, ignore_index=True)

        # Caminho de saída de arquivo para o Data Lake com os dados já tratados 
        # para que eles possam se tornar Relatórios, DashBoard para tomada de decisão

        output_file = os.path.join('data_lake\Ready', 'clean.xlsx')
        
        # cria o motor de escrita no excel
        writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

        # Escreve os dados no motor configurado
        result.to_excel(writer, index=False)

        writer._save()
        
        # Transforma o aruivo para JSON formatação utilizada para estruturar dados em formato de texto
        #  e transmiti-los de um sistema para outro, como em aplicações cliente-servidor ou em aplicativos móveis
        #  para um persistência poliglota
        
        js = result.to_json(orient= 'records')
       # print(js)

        with open("data_lake\JSON\channels.json", "w") as outfile:
         json.dump(js, outfile)

    else:
        print("Nenhum dado a ser salvo")
