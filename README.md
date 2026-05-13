# Desafio Técnico — Estágio em Ciência de Dados — Resposta

---

## Resumo

Projeto criado para o desafio técnico para a vaga de Estágio em Ciência de Dados. O projeto consiste em 3 etapas, limpeza e tratamento do texto, geração de embeddings e a implementação de um motor de busca semântico.

---
## Como rodar o projeto:

### Requerimentos:


Bibliotecas externas principais: pandas, numpy, SentenceTransformer, beautifulsoup4. Conferir requirements.txt para visualizar a lista completa.

Execute o comando abaixo em um terminal aberto na pasta com o arquivo requirements.txt para instalar todas as dependências:

```
 pip install -r requirements.txt
```
Python em uso: 3.14

### Executando:

Os scritps sendo executados precisam estar na mesma pasta onde se encontram as pastas 'dados' e 'respostas'. Execute os scripts nessa ordem: 

1. clean.py
    - Limpeza do texto
2. embed_e5.py  
    - Criação das embeddings
3. query_e5.py  
    - Execução da busca

As janelas abertas por cada script só seram fechadas após o usuário pressionar enter.

Se desejar executar buscas diferentes das presentes já no código, altere a variável *queries* em query_e5.py com suas queries, ou use o script query_e5_inputquery.py, que irá te pedir para inserir uma query ao executa-lo para comparar com os vetores. 

Se desejar visualizar respostas da ultima execução, no caso das vindas do script query_e5.py, estarão presentes em Respostas/output_e5.txt. As respostas das queries vindas de query_e5_inputquery.py estarão em Respostas/output_e5_inputquery.txt, e serão gravadas cumulativamente. 

---
## Etapa 1 — Limpeza e Tratamento de Texto

Foi criada uma função onde foram estabelecidos os critérios para limpar o texto sujo. 

A limpeza das entidades e tags html foi feita usando a biblioteca beautifulsoup, enquanto a limpeza dos espaços duplos, quebras de linhas em excesso e os cabeçalhos com metadados foi feita com regex.

Para formular o comando regex para limpar os metadados no texto, foi primeiro observado que esse conteudo sujo se encontrava no inicio do documento, até a primeira quebra de linha. Considerando esse padrão, foi feito o comando para deletar todo conteúdo até essa primeira quebra. 

Foi também adicionada uma condicional para apenas deletar caso esteja presente a data no formato XX/XX/XXXX, outro padrão apresentado nas notícias, como meio de aumentar a segurança do comando, pensando na possibilidade de que sejam inclusas noticias que fujam de um dos padrões, o que poderia resultar ou no texto não sendo limpo ou no pior dos casos de serem deletadas partes da noticia.

Para lidar com o caso extremo da noticia de id original 18, foi optado por inserir um comando para definir qualquer noticia com uma quantidade de caracteres menor que 11 para o valor None.

Para manipular os dados e carregar o json nessa etapa, foi optado usar biblioteca pandas, por ser possível gerar codigos mais diretos para lidar com os problemas ainda presentes. Principalmente foi usado o Series.apply() para aplicar a função cleaning a toda a coluna texto do Data Frame, DataFrane.dropna() para deletar toda a linha que continha o caso extremo, e DataFrame.index para corrigir o indice das notícias. Esse conteudo foi então salvo em desafio-e5/dados/noticias_limpas.json. 

---

## Etapa 2 — Geração de Embeddings e justificativa do modelo escolhido

As bibliotecas externas aqui usadas foram numpy e SentenceTransformers.

Para buscar as opções de modelos foram usadas a documentação do Sentence Transformer que já conta com certas sugestões, e a [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard), onde foram encontrados os modelos aqui usados. 

O modelo escolhido para a entrega desse desafio foi o [multilingual-e5-small](https://huggingface.co/intfloat/multilingual-e5-small). Ele foi escolhido pela sua rapidez e  eficiência para lidar com dados multilinguais. Como a base de dados aqui usada ainda é uma base pequena, com apenas 19 notícias, o seu número menor de parametros e dimensões de embedding apresentam um ganho em eficiência maior que a perca de precisão. 

Foi feito um teste com outro modelo, o [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B), que apresenta uma quantidade de parametros e dimensões maiores. Foi observada na etapa da geração de embeddings demora maior que o e5 e uso muito maior da cpu. 

Foi decidido manter o uso do modelo multilingual-e5-small, quando na etapa do motor de busca semântico foi observado que os resultados, apesar de apresentarem scores diferentes por conta do funcionamento particular de cada modelo, foram muito similares. Com top_k = 5, apenas houve uma discrepancia preocupante, na busca por "mudanças na taxa de juros", onde o modelo Qwen3-Embedding-0.6B teve um desempenho superior.

A causa disso aparenta ser uma relação superior da "mudança na taxa de juros" com a taxa Selic, enquanto o e5 priorizou a presença da palavra "juros" na notícia. O modelo qwen3 assim trouxe notícias mais relevantes. Dito isso, os usos muito superiores de recursos e demora tanto na criação das embeddings quando (em menor escala) no motor de busca, justificam a permanência no modelo e5. Os arquivos dos scripts e das embeddings usando o qwen3 ainda estarão presentes nesse repositório para fins de registro.

Por fim, as embeddings foram salvas em um arquivo npy, como ndarrays, por representar maior segurança para o usuário do que um arquivo .pkl e ser lido com mais rapidez e menor uso de memória que .json.

---

## Etapa 3 — Motor de Busca Semântico

Nessa etapa foi usada a função util.semantic_search para executar a busca semantica. Dessa forma não é necessário converter as embeddings geradas para tensor usando torch separadamente, a função já realizando esse trabalho. Os resultados então são visualizados no terminal e gravados em um arquivo.

A documentação do modelo usado foi seguida, sendo adicionada 'passage: ' aos textos ainda na fase anterior, e 'query: ' nessa fase com as queries. Também foi verificado que todos os vetores foram normalizados, como também indica a documentação.
No script usando o modelo qwen3, igualmente a documentação foi seguida, tentando seguir os exemplos dados.

Ao olhar as scores de cada resultado, considere que as scores no modelo e5 vão de 0.7 até 1.0, de acordo com a documentação.

---
## Resultados Etapa 3:

Resultados também disponíveis em desafio-e5/dados/output_e5.txt. Também inclusos os resultados do script querry_qwen.py em desafio-qwen3/output_qwen.py.

```
"mudanças na taxa de juros"
```
Resultado: 1 (Score: 0.8657)
Título: Copom mantém Selic em 13,75% ao ano pela quarta reunião consecutiva
Fonte: Banco Central do Brasil
Data: 2023-08-02
Notícia: O Comitê de Política Monetária (Copom) do Banco Central do Brasil decidiu, por unanimidade, manter a taxa básica de juros (Selic) em 13,75% ao ano. Esta é a quarta reunião consecutiva em que o comitê opta pela manutenção. Segundo o comunicado oficial, o Copom avaliou que o ambiente inflacionário ainda exige cautela, embora o IPCA acumulado nos últimos doze meses tenha apresentado desaceleração consistente. O colegiado ponderou, ainda, os efeitos defasados da política monetária já em vigor sobre a atividade econômica. Leia o comunicado completo em www.bcb.gov.br

Resultado: 2 (Score: 0.8565)
Título: Inadimplência das famílias sobe para 6,3% em julho, aponta BC
Fonte: Banco Central do Brasil
Data: 2023-08-25
Notícia: A inadimplência das famílias — operações com atraso superior a 90 dias — subiu para 6,3% em julho, alta de 0,1 ponto percentual em relação a junho, segundo dados do Banco Central . O indicador acumula crescimento de 0,8 pp nos últimos doze meses. O endividamento das famílias com o sistema financeiro atingiu 49,1% da renda acumulada em doze meses. O comprometimento da renda com o serviço da dívida ficou em 28,5%. O crédito pessoal não consignado, modalidade mais cara e de maior risco, apresentou inadimplência de 9,1%. Especialistas atribuem a piora ao efeito defasado dos juros altos sobre as finanças das famílias.

Resultado: 3 (Score: 0.8511)
Título: Selic deve recuar a 9% até o fim de 2024, projetam economistas
Fonte: Banco Central do Brasil
Data: 2023-08-15
Notícia: Economistas consultados pelo Banco Central no Relatório Focus revisaram para baixo a projeção para a taxa Selic ao final de 2024, de 9,25% para 9,00% ao ano. A mudança reflete a percepção de que o ciclo de afrouxamento monetário poderá ser mais agressivo caso a inflação continue a recuar. Para o final de 2023, a mediana das expectativas permanece em 11,75%. O IPCA esperado para 2023 foi revisado de 4,92% para 4,84%, ainda acima da meta de 3,25%. O presidente do BC, Roberto Campos Neto, reiterou que as decisões serão tomadas "reunião a reunião", sem compromissos antecipados com um ritmo de corte específico.

Resultado: 4 (Score: 0.8493)
Título: Crédito total no Brasil atinge R\$ 5,6 trilhões com desaceleração no crescimento
Fonte: Banco Central do Brasil
Data: 2023-08-25
Notícia: O estoque total de crédito no sistema financeiro nacional atingiu R$ 5,6 trilhões em julho de 2023, segundo o Relatório de Crédito do Banco Central . O crescimento anual desacelerou para 8,3%, ante 16,4% registrado em julho de 2022. O crédito às pessoas físicas cresceu 11,4% em doze meses, enquanto o crédito a empresas avançou apenas 5,1%. A taxa média de juros nas operações de crédito livre ficou em 40,2% ao ano, ainda em patamar elevado. O Banco Central observa que a desaceleração reflete tanto as condições financeiras mais restritivas quanto a maior seleção de risco pelas instituições financeiras.

Resultado: 5 (Score: 0.8454)
Título: Inflação ao produtor (IPA) desacelera e pressão sobre preços finais diminui
Fonte: FGV IBRE
Data: 2023-08-10
Notícia: O Índice de Preços ao Produtor Amplo (IPA), que mede a variação de preços no atacado, registrou deflação de 0,55% em julho, segundo a FGV IBRE . O resultado reforça a tendência de menor pressão inflacionária sobre os preços ao consumidor nos próximos meses. Os produtos agropecuários registraram queda de 1,12%, enquanto os industriais recuaram 0,21%. Analistas da FGV destacam que a transmissão da deflação no atacado para o consumidor ocorre com defasagem de dois a três meses. O IGP-M, que também computa o IPA em sua fórmula, acumula queda de 5,18% nos últimos doze meses até julho.

```
"mercado de trabalho e desemprego"
```
Resultado: 1 (Score: 0.8738)
Título: Taxa de desemprego cai para 7,9% no segundo trimestre, menor nível desde 2014
Fonte: IBGE
Data: 2023-08-29
Notícia: A taxa de desemprego no Brasil recuou para 7,9% no segundo trimestre de 2023, o menor nível desde o quarto trimestre de 2014, quando foi de 6,5%. Os dados são da Pesquisa Nacional por Amostra de Domicílios (PNAD Contínua), do IBGE. O número de desocupados caiu para 8,5 milhões de pessoas, uma redução de 1,1 milhão em relação ao trimestre anterior. O emprego formal, com carteira assinada, cresceu 2,3% no período. A renda média real dos trabalhadores também registrou crescimento de 3,7% na comparação anual, chegando a R$ 2.958. Acesse a PNAD Contínua completa

Resultado: 2 (Score: 0.8602)
Título: Desemprego juvenil no Brasil ainda preocupa apesar de melhora geral
Fonte: IBGE
Data: 2023-08-30
Notícia: Apesar da melhora generalizada no mercado de trabalho, a taxa de desemprego entre jovens de 18 a 24 anos ainda se mantém elevada, em 17,8% no segundo trimestre de 2023, mais do que o dobro da taxa geral de 7,9%, segundo a PNAD Contínua do IBGE . O emprego informal entre os jovens também preocupa: 52% dos jovens empregados não possuem carteira assinada. Programas governamentais de qualificação profissional e aprendizagem foram apontados como essenciais para reduzir esse hiato. Especialistas do Ministério do Trabalho destacam que a inserção de jovens no mercado formal exige, além de qualificação, mudanças estruturais na economia.

Resultado: 3 (Score: 0.8410)
Título: IGP-M registra terceira deflação consecutiva em agosto
Fonte: FGV IBRE
Data: 2023-08-30
Notícia: O Índice Geral de Preços — Mercado (IGP-M) registrou variação de -0,53% em agosto, a terceira deflação consecutiva. No acumulado de doze meses, o índice acumula queda de 6,96%, segundo a FGV IBRE . O IPA (atacado) recuou 0,80%, com destaque para a queda nos preços dos produtos agropecuários (-1,45%). O IPC (consumidor) subiu 0,19%, influenciado principalmente pelos grupos de Alimentação e Saúde e Cuidados Pessoais. O INCC (construção civil) avançou 0,22%, reflexo das pressões pontuais em mão de obra no setor.

Resultado: 4 (Score: 0.8349)
Título: Confiança do consumidor sobe pelo quarto mês seguido em agosto
Fonte: FGV IBRE
Data: 2023-08-29
Notícia: O Índice de Confiança do Consumidor (ICC) da FGV IBRE avançou 1,2 pontos em agosto, para 92,4 pontos, a quarta alta consecutiva. O resultado ainda está abaixo da média histórica de 100 pontos, mas aponta para recuperação gradual do otimismo das famílias. A melhora foi observada tanto no componente de Situação Atual (+0,8 pontos) quanto nas Expectativas (+1,5 pontos). Entre os fatores apontados pelos consumidores como positivos estão a queda do desemprego e o ar arrefecimento da inflação. Para acessar o relatório completo, visite o Portal FGV IBRE .

Resultado: 5 (Score: 0.8318)
Título: Inflação ao produtor (IPA) desacelera e pressão sobre preços finais diminui
Fonte: FGV IBRE
Data: 2023-08-10
Notícia: O Índice de Preços ao Produtor Amplo (IPA), que mede a variação de preços no atacado, registrou deflação de 0,55% em julho, segundo a FGV IBRE . O resultado reforça a tendência de menor pressão inflacionária sobre os preços ao consumidor nos próximos meses. Os produtos agropecuários registraram queda de 1,12%, enquanto os industriais recuaram 0,21%. Analistas da FGV destacam que a transmissão da deflação no atacado para o consumidor ocorre com defasagem de dois a três meses. O IGP-M, que também computa o IPA em sua fórmula, acumula queda de 5,18% nos últimos doze meses até julho.

```
"inflação e preços ao consumidor"
```
Resultado: 1 (Score: 0.8913)
Título: IPCA de julho registra 0,12%, menor resultado para o mês desde 2006
Fonte: IBGE
Data: 2023-08-09
Notícia: O Índice Nacional de Preços ao Consumidor Amplo (IPCA) ficou em 0,12% em julho de 2023, o menor resultado para o mês desde 2006, quando havia recuado 0,04%. No acumulado do ano, o índice chega a 3,19%, e em doze meses, a 3,99%. O grupo de Alimentação e Bebidas foi o principal responsável pela desaceleração, com variação negativa de 0,07%. Já Transportes apresentaram alta de 0,39%, puxados pelo aumento nos preços dos combustíveis. Dados completos disponíveis em ibge.gov.br .

Resultado: 2 (Score: 0.8872)
Título: Inflação ao produtor (IPA) desacelera e pressão sobre preços finais diminui
Fonte: FGV IBRE
Data: 2023-08-10
Notícia: O Índice de Preços ao Produtor Amplo (IPA), que mede a variação de preços no atacado, registrou deflação de 0,55% em julho, segundo a FGV IBRE . O resultado reforça a tendência de menor pressão inflacionária sobre os preços ao consumidor nos próximos meses. Os produtos agropecuários registraram queda de 1,12%, enquanto os industriais recuaram 0,21%. Analistas da FGV destacam que a transmissão da deflação no atacado para o consumidor ocorre com defasagem de dois a três meses. O IGP-M, que também computa o IPA em sua fórmula, acumula queda de 5,18% nos últimos doze meses até julho.

Resultado: 3 (Score: 0.8849)
Título: IGP-M registra terceira deflação consecutiva em agosto
Fonte: FGV IBRE
Data: 2023-08-30
Notícia: O Índice Geral de Preços — Mercado (IGP-M) registrou variação de -0,53% em agosto, a terceira deflação consecutiva. No acumulado de doze meses, o índice acumula queda de 6,96%, segundo a FGV IBRE . O IPA (atacado) recuou 0,80%, com destaque para a queda nos preços dos produtos agropecuários (-1,45%). O IPC (consumidor) subiu 0,19%, influenciado principalmente pelos grupos de Alimentação e Saúde e Cuidados Pessoais. O INCC (construção civil) avançou 0,22%, reflexo das pressões pontuais em mão de obra no setor.

Resultado: 4 (Score: 0.8611)
Título: Confiança do consumidor sobe pelo quarto mês seguido em agosto
Fonte: FGV IBRE
Data: 2023-08-29
Notícia: O Índice de Confiança do Consumidor (ICC) da FGV IBRE avançou 1,2 pontos em agosto, para 92,4 pontos, a quarta alta consecutiva. O resultado ainda está abaixo da média histórica de 100 pontos, mas aponta para recuperação gradual do otimismo das famílias. A melhora foi observada tanto no componente de Situação Atual (+0,8 pontos) quanto nas Expectativas (+1,5 pontos). Entre os fatores apontados pelos consumidores como positivos estão a queda do desemprego e o ar arrefecimento da inflação. Para acessar o relatório completo, visite o Portal FGV IBRE .

Resultado: 5 (Score: 0.8471)
Título: Copom mantém Selic em 13,75% ao ano pela quarta reunião consecutiva
Fonte: Banco Central do Brasil
Data: 2023-08-02
Notícia: O Comitê de Política Monetária (Copom) do Banco Central do Brasil decidiu, por unanimidade, manter a taxa básica de juros (Selic) em 13,75% ao ano. Esta é a quarta reunião consecutiva em que o comitê opta pela manutenção. Segundo o comunicado oficial, o Copom avaliou que o ambiente inflacionário ainda exige cautela, embora o IPCA acumulado nos últimos doze meses tenha apresentado desaceleração consistente. O colegiado ponderou, ainda, os efeitos defasados da política monetária já em vigor sobre a atividade econômica. Leia o comunicado completo em www.bcb.gov.br

---
