import numpy as np
import json
from sentence_transformers import SentenceTransformer
from pathlib import Path

p_dados = Path(__file__).parent / 'dados'
print('Começando o processo...')
try:
    model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B") #modelo escolhido. Justificativa no Readme
    with open('dados/noticias_limpas.json', 'r', encoding='utf-8') as x:
        news_nemb = json.load(x) 
except RuntimeError:
    print('Conexão não encontrada. Necessária conexão.')
    exit()
except FileNotFoundError:
    print('Arquivo noticias_limpas.json não encontrado, tente executar clean.py novamente.')
    exit()

embd = [] 
for n in news_nemb:
    txt_embd = model.encode(n["texto"])
    embd.append(txt_embd)

np.save('dados/embeddings_qwen.npy', embd) #escolhido usar numpy por segurança e velocidade.
print("Sucesso!")
quit_program = input('Pressione enter para sair...')