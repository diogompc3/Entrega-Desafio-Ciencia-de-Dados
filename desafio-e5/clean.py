import pandas as pd
import re
from bs4 import BeautifulSoup
from pathlib import Path

p_dados = Path(__file__).parent / 'dados'

def cleaning(txt):
    soup = BeautifulSoup(txt, "html.parser")                             #limpando entidades html
    txt_clean = soup.get_text()
    fax_date = r'^.*?\d{2}/\d{2}/\d{4}[^\n]*'                               #encontrar a primeira quebra de linha caso exista uma data no formato **/**/****.
    txt_clean = re.sub(fax_date, '', txt_clean, flags=re.IGNORECASE)   
    txt_clean = re.sub(r'\s+', ' ', txt_clean).strip()              #substituindo espaços e quebras de linhas desnecessárias. 
    if len(txt_clean) < 10: 
        txt_clean = None                                        #Nos casos extremos, retornar NaT, para ter toda a linha deletada posteriormente.
    return txt_clean

print('Iniciando limpeza...')
df = pd.read_json(p_dados/ 'noticias_brutas.json')             #Utilizando pandas para manipular os dados json
df['texto'] = df['texto'].apply(cleaning)
df.dropna(ignore_index = True, inplace = True)              #removendo a linha que retornou NaT
df['id'] = df.index + 1                                     #Corrigindo o index para manter a lógica anterior das notícias brutas

df.to_json(path_or_buf=p_dados / 'noticias_limpas.json', orient='records', force_ascii=False, indent=4)
print('Sucesso!')
quit_program = input('Pressione enter para sair...')