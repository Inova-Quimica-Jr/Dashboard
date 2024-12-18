import streamlit as st
import pandas as pd
import seaborn as sns
import requests
import json
import matplotlib.pyplot as plt

# Configuração da página do Streamlit
st.set_page_config(page_icon= 'Icon.jpg',page_title="Inova Quimica Jr", layout="wide")

# Titulo da página
st.markdown(
    """
    <h1 style='text-align: center; color: #FFFFFF;'>Lobby da Inova Química Jr</h1>
    """,
    unsafe_allow_html=True
)

# Define o número de coluna que o Dashboard tera e a proporção de tamanho exp: 1:1:1
col1, col2, col3 = st.columns([1, 1, 1])

# URL base da API do Pipefy
url = "https://api.pipefy.com/graphql"

# URL base do Excel da Gameficação
url_game = 'https://drive.google.com/uc?id=1szuXLsXhHZPELuTAo5ClL8Ez2fOn422R' #Caso precise atualizar este link tomar cuidado para não colocar o link do documento na forma editavel
dados_game = pd.read_excel(url_game, header=4) # Essas configurações irão depender da formatação feina no excel
dados_game.rename(columns={'Total': 'Pontuação Departamentos', 'Total.1': 'Pontuação Individual'}, inplace=True) # Isso renomeia as colunas para melhor compreensão para codar
dados_game.drop(['Unnamed: 0', 'Unnamed: 3','Unnamed: 4' ], axis=1, inplace=True) # Exclui colunas desnecessarias

# Cabeçalhos com a chave de autenticação
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJQaXBlZnkiLCJpYXQiOjE3MjUyOTIyNDgsImp0aSI6ImM0OTNlYjllLTc4ZTUtNGYxYy05MGQ0LTI3NDNkNGNhYzRkZiIsInN1YiI6NzYyNDU1LCJ1c2VyIjp7ImlkIjo3NjI0NTUsImVtYWlsIjoiaXFqckBpcS51c3AuYnIifX0.Kj8wdVuN7nlyQgaEuMXGnep8hkDovLlsrf8-AsD_c6pzZoeK2vUvtkn0Z1uk6ptsPOf6ZUszTdsswlIMkmLOgg",
    "Content-Type": "application/json"}

# Função para obter os dados do pipefy da equipe de projetos
def obter_cards_do_pipe_do_projetos(url, headers):
    # Definir a query GraphQL para obter os cards do pipe
    query = """
    {
    pipe(id: "1260884") {
        id
        name
        phases {
        name
        cards {
            edges {
            node {
                id
                title
                due_date
                assignees {
                id
                name
                }
                created_at
                updated_at
                fields {
                name
                value
                }
            }
            }
        }
        }
    }
    }
    """

    # Fazer a requisição para a API do Pipefy
    response = requests.post(url, headers=headers, json={"query": query})

    # Verifica se a requisição foi bem-sucedida
    if response.status_code != 200:
        st.write(f"Erro: {response.status_code} - {response.text}")
        return None

    # Processa a resposta em JSON
    projetos = response.json()

    # Identificar todos os campos possíveis nos fields
    all_field_names = set()
    for phase in projetos['data']['pipe']['phases']:
        for card in phase['cards']['edges']:
            for field in card['node'].get('fields', []):
                all_field_names.add(field['name'])

    # Convertendo o conjunto para lista ordenada
    all_field_names = sorted(all_field_names)

    # Processamento dos dados
    data = []
    for phase in projetos['data']['pipe']['phases']:
        phase_name = phase['name']
        for card in phase['cards']['edges']:
            card_node = card['node']
            card_id = card_node['id']
            card_title = card_node['title']
            card_due_date = card_node.get('due_date', None)
            card_assignees = [assignee['name'] for assignee in card_node.get('assignees', [])]
            card_created_at = card_node['created_at']
            card_updated_at = card_node['updated_at']

            # Criar um dicionário com os campos
            fields_dict = {field_name: None for field_name in all_field_names}  # Inicializar todos como None
            for field in card_node.get('fields', []):
                fields_dict[field['name']] = field['value']  # Preencher com valores existentes

            # Adicionar os dados básicos do card + os fields
            data.append([phase_name, card_id, card_title, card_due_date, card_assignees, card_created_at, card_updated_at] + list(fields_dict.values()))

    # Criação do DataFrame com todas as colunas
    columns = ['Phase', 'Card ID', 'Title', 'Due Date', 'Assignees', 'Created At', 'Updated At'] + all_field_names
    df_projetos = pd.DataFrame(data, columns=columns)

    return df_projetos

# Função para obter os dados do pipefy da equipe de vendas
def obter_cards_do_pipe_do_vendas(url, headers):
    # Definir a query GraphQL para obter os cards do pipe
    query = """
    {
    pipe(id: "914531") {
        id
        name
        phases {
        name
        cards {
            edges {
            node {
                id
                title
                due_date
                assignees {
                id
                name
                }
                created_at
                updated_at
                fields {
                name
                value
                }
            }
            }
        }
        }
    }
    }
    """

    # Fazer a requisição para a API do Pipefy
    response = requests.post(url, headers=headers, json={"query": query})

    # Verifica se a requisição foi bem-sucedida
    if response.status_code != 200:
        st.write(f"Erro: {response.status_code} - {response.text}")
        return None

    # Processa a resposta em JSON
    vendas = response.json()

    # Identificar todos os campos possíveis nos fields
    all_field_names = set()
    for phase in vendas['data']['pipe']['phases']:
        for card in phase['cards']['edges']:
            for field in card['node'].get('fields', []):
                all_field_names.add(field['name'])

    # Convertendo o conjunto para lista ordenada
    all_field_names = sorted(all_field_names)

    # Processamento dos dados
    data = []
    for phase in vendas['data']['pipe']['phases']:
        phase_name = phase['name']
        for card in phase['cards']['edges']:
            card_node = card['node']
            card_id = card_node['id']
            card_title = card_node['title']
            card_due_date = card_node.get('due_date', None)
            card_assignees = [assignee['name'] for assignee in card_node.get('assignees', [])]
            card_created_at = card_node['created_at']
            card_updated_at = card_node['updated_at']

            # Criar um dicionário com os campos
            fields_dict = {field_name: None for field_name in all_field_names}  # Inicializar todos como None
            for field in card_node.get('fields', []):
                fields_dict[field['name']] = field['value']  # Preencher com valores existentes

            # Adicionar os dados básicos do card + os fields
            data.append([phase_name, card_id, card_title, card_due_date, card_assignees, card_created_at, card_updated_at] + list(fields_dict.values()))

    # Criação do DataFrame com todas as colunas
    columns = ['Phase', 'Card ID', 'Title', 'Due Date', 'Assignees', 'Created At', 'Updated At'] + all_field_names
    df_vendas = pd.DataFrame(data, columns=columns)

    return df_vendas

# Tranforma os pipefy em "Excels python" chamados de DataFrame'df'
df_projetos = obter_cards_do_pipe_do_projetos(url, headers)
df_vendas = obter_cards_do_pipe_do_vendas(url, headers)

# Esta função gera um Grafico de distribuição, utilizando um df, uma coluna deste df, e um titulo a sua escolha
def gerar_grafico_distribuicao(df, coluna, titulo=''):
    # Fazer a contagem dos valores na coluna especificada
    contagem = (df[coluna]
                .str.split(',', expand=True)
                .stack()
                .str.replace(r'[\[\]"]', '', regex=True)
                .str.strip()
                .value_counts())
    
    # Aplicar o estilo do Seaborn
    sns.set_theme(style="darkgrid")
    
    # Definir cores personalizadas com base no tamanho da contagem
    cores = sns.color_palette('pastel')[0:len(contagem)]
    
    # Criar o gráfico de rosca
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(contagem, autopct='%1.1f%%', wedgeprops=dict(width=1), colors=cores)

    fig.patch.set_alpha(0)  # Fundo do gráfico transparente
    ax.patch.set_alpha(0)   # Fundo dos eixos transparente

    # Adicionar título ao gráfico
    plt.title(titulo, color='white', fontsize=16, fontweight='bold', loc='center')
    
    # Adicionar legenda com as cores
    ax.legend(wedges, contagem.index, title="Categorias", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    # Estilizar com Seaborn
    sns.despine(left=True)
    
    # Exibir o gráfico
    st.pyplot(fig)

#Esta função gera um grafico de barras, As informações que constam entre paraenteses devem ser dados ao chamar a função, caso contrario utilizara o padrão que esta setado( isso não se aplica aos tres primeiros parametros, estes são mandatorios).
def gerar_grafico_barras(data, x_col, y_col, title='', x_label='', y_label='Pontos', color='skyblue',title_fontsize=20, label_fontsize=14, rotation=0):

    fig, ax = plt.subplots(figsize=(10, 8))  # Definir o tamanho da figura

    # Criar o gráfico de barras
    ax.bar(data[x_col].dropna().astype(str), data[y_col].dropna(), color=color)

    # Definir fundo transparente
    fig.patch.set_alpha(0)    # Fundo da figura transparente
    ax.set_facecolor('none')  # Fundo do gráfico transparente
    ax.grid(False)            # Fundo sem grades

    # Adicionar título e rótulos com texto branco e tamanhos de fonte ajustáveis
    ax.set_title(title, color='white', fontsize=title_fontsize)
    ax.set_xlabel(x_label, color='white', fontsize=label_fontsize)
    ax.set_ylabel(y_label, color='white', fontsize=label_fontsize)
    ax.tick_params(axis='x', colors='white', labelsize=label_fontsize)  # Cor e tamanho dos rótulos do eixo X
    ax.tick_params(axis='y', colors='white', labelsize=label_fontsize)  # Cor e tamanho dos rótulos do eixo Y
    plt.xticks(rotation=rotation, color='white', fontsize=label_fontsize)
    # Exibir o gráfico
    st.pyplot(fig)

def gerar_ranking(data,x_col,y_col, title='Pódio', x_label='', y_label='Pontuação', title_fontsize=20, label_fontsize=18,):
    
    data = data.nlargest(3,data[y_col].name)

    # Reindexar para centralizar o maior
    data = data.reset_index(drop=True)
    data = data.reindex([1, 0, 2])
    
    # Cores para as barras
    colors = ['silver', 'gold', 'saddlebrown']
    
    # Criar o gráfico
    fig, ax = plt.subplots(figsize=(10, 8))
    
    fig.patch.set_alpha(0)    # Fundo da figura transparente
    ax.set_facecolor('none')  # Fundo do gráfico transparente
    ax.grid(False)            # Fundo sem grades

    # Adicionar título e rótulos com texto branco e tamanhos de fonte ajustáveis
    ax.set_title(title, color='white', fontsize=title_fontsize)
    ax.set_xlabel(x_label, color='white', fontsize=label_fontsize)
    ax.set_ylabel(y_label, color='white', fontsize=label_fontsize)
    ax.tick_params(axis='x', colors='white', labelsize=label_fontsize)  # Cor e tamanho dos rótulos do eixo X
    ax.tick_params(axis='y', colors='white', labelsize=label_fontsize)  # Cor e tamanho dos rótulos do eixo Y
    plt.xticks(color='white', fontsize=label_fontsize)
    plt.xticks(color='white')

    # Criar o gráfico de barras
    bars = plt.bar(data[x_col], data[y_col], 
                   color=colors, width=0.6)

    # Adicionar os valores no topo das barras
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, 
                 bar.get_height() + 2,  # Posição ligeiramente acima da barra
                 str(int(bar.get_height())), 
                 ha='center', va='bottom', fontsize=15, fontweight='bold', color='white')
    
    # Mostrar o gráfico
    st.pyplot(fig)

def Faz_tabela_de_Posição(data,x_col,y_col):
    data = data.sort_values(by= data[y_col].name,ascending=False).reset_index(drop=True)
    data[y_col] = data[y_col].round(2)
    data['Posição'] = data.index + 1
    data['Posição'] = data['Posição'].astype(str) + '° lugar'
    Tabela_Posição = data[[x_col,y_col,'Posição']].dropna()
    st.dataframe(Tabela_Posição.reset_index(drop=True), use_container_width=True, hide_index=True)
    

with col1:
    Opções = ['Vendas', 'Gameficação', 'Projetos em Andamento']
    Visualização = st.selectbox('Escolha sobre o que deseja ver', Opções
    )
    if Visualização == 'Vendas':
        Projetos = st.selectbox('Veja por seção de projetos', df_vendas['Tipo de Serviço']
                        .str.split(',', expand=True)
                        .stack()
                        .str.replace(r'[\[\]"]', '', regex=True)
                        .str.strip()
                        .value_counts()
                        .index
                        .tolist())
        df_filtrado = df_vendas[df_vendas['Tipo de Serviço'].str.contains(Projetos, na=False, regex=False)]
        st.dataframe(df_filtrado[['Title', 'Valor fechado']], hide_index=True)



with col2: 
    if Visualização == 'Vendas':
        gerar_grafico_distribuicao(df_vendas, 'Tipo de Serviço', 'Distribuição de Tipos de Serviço')


    elif Visualização == 'Gameficação':
        
        gerar_grafico_barras(dados_game,'Nomes', 'Pontuação Individual', 'Pontuação Individual', rotation=90 )
        
        gerar_grafico_barras(dados_game,'Departamentos', 'Pontuação Departamentos', 'Pontuação Departamentos')


    elif Visualização == 'Projetos em Andamento':
        df_filtrado = df_projetos[df_projetos['Phase'].str.contains('Execução', na=False, regex=False)]
        st.dataframe(df_filtrado[['Title', 'Descrição']], hide_index=True)


with col3:
    if Visualização == 'Vendas':
        st.write('Em construção')

    elif Visualização == 'Gameficação':
        Faz_tabela_de_Posição(dados_game,'Nomes', 'Pontuação Individual')
        Faz_tabela_de_Posição(dados_game,'Departamentos', 'Pontuação Departamentos')

    elif Visualização == 'Projetos em Andamento':
        st.write('Em construção')

