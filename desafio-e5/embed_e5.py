import numpy as np
import json
from sentence_transformers import SentenceTransformer
from pathlib import Path

p_dados = Path(__file__).parent / 'dados'

print('Começando o processo...')
try: 
    model = SentenceTransformer("intfloat/multilingual-e5-small") #modelo escolhido. Justificativa no Readme
    with open(p_dados / 'noticias_limpas.json', 'r', encoding='utf-8') as x:
        news_n_emb = json.load(x)
except RuntimeError:
    print('Conexão não encontrada. Necessária conexão.')
    exit()
except FileNotFoundError:
    print('Arquivo noticias_limpas.json não encontrado, tente executar clean.py novamente.')
    exit()

embd = [] 
for n in news_n_emb:
    txt = "passage: " + n["texto"]                            #adição de "passage: " requerida segundo documentação do modelo.
    txt_embd = model.encode(txt, normalize_embeddings=True)
    embd.append(txt_embd)

np.save(p_dados / 'embeddings.npy', embd) #escolhido usar numpy por segurança e velocidade.
print("Sucesso!")
quit_program = input('Pressione enter para sair...')