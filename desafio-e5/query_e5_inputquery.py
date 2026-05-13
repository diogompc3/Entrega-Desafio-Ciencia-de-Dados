import numpy as np
import json
from sentence_transformers import SentenceTransformer, util
from pathlib import Path

p_dados = Path(__file__).parent / 'dados'
p_respostas = Path(__file__).parent / 'respostas'

# Como as embeddings não tiveram os metadados embutidos, necessário carregar as noticias_limpas também.
try:  #checando se os arquivos necessários foram gerados. Deveriam ter sido caso tenham seguido as etapas, então pedindo para executar os scripts anteriores se preciso.
    arq_1 = p_dados / 'embeddings.npy'
    arq_2 = p_respostas / 'noticias_limpas.json'
    embd_news = np.load(arq_1)                            
    with open(arq_2, 'r', encoding='utf-8') as f:        
        print('Arquivo com as noticias limpas existe, prosseguindo:')
        news = json.load(f)
    model = SentenceTransformer("intfloat/multilingual-e5-small")               
except RuntimeError:    #caso não exista conexão, avisar usuário.
    print('Conexão não encontrada. Esse script necessita de uma conexão com a internet.') 
    exit()
except ValueError:
    print('embeddings_qwen.py está corrompido ou se encontra em um formato inesperado.\nPor favor tente executar embed_qwen.py novamente.')
    exit()
except FileNotFoundError:
    print('Um dos arquivos requeridos não existem.\nPor favor tente executar clean.py e/ou embed_qwen.py.')
    exit()
            

stay = "s"
while stay.startswith("s"):               
    query = 'query: ' + input('Insira aqui a informação desejada: ')
    with open(p_respostas / 'output_e5_inputquery.txt', 'a', encoding='utf-8')as f:
        print(f"Pergunta: {query.replace("query: ", "")}", file = f)
    embd_query = model.encode(query, normalize_embeddings=True)
    results = util.semantic_search(embd_query, embd_news, top_k=3, score_function=model.similarity)[0]      #Aqui foram limitados a 3 resultados
    print('Os resultados de sua busca são: \n')    
    for pos, n in enumerate(results):                                       
        news_index = news[n['corpus_id']]
        final_result = (
            f"Resultado: {pos + 1} (Score: {n['score']:.4f})\n"     #Por observação, os resultados variam o bastante para 3 casas decimais serem o suficiente.
            f"Título: {news_index['titulo']}\n"
            f"Fonte: {news_index['fonte']}\n"
            f"Data: {news_index['data']}\n"
            f"Notícia: {news_index['texto']}\n"
        )
        print(final_result)
        with open(p_respostas / 'output_e5_inputquery.txt', 'a', encoding='utf-8')as f:
            print(final_result, file = f)
    stay = input("Deseja fazer mais uma pergunta? [S]im para continuar ou qualquer outra tecla para sair. ").lower()
quit_program = input('Pressione enter para sair...')