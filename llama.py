import streamlit as st
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
from whoosh.analysis import StemmingAnalyzer
import os
import requests
import PyPDF2
import re
from groq import Groq

# Definindo o esquema
schema = Schema(content=TEXT(stored=True, analyzer=StemmingAnalyzer()))

# Criando o índice
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
index = create_in("indexdir", schema)

# Adicionando documentos ao índice
index = open_dir("indexdir")
writer = index.writer()

# Função de pré-processamento do texto
def preprocess_text(text):
    """
    Função para remover informações irrelevantes do texto e dividir o texto em linhas.
    """
    text = re.sub(r'\d{2}/\d{2}/\d{4}, \d{2}:\d{2}.*? \d{1,3}/\d{1,3}', '', text, flags=re.DOTALL)
    text = text.replace('\xa0', ' ')
    text = text.lower()
    lines = text.split('\n')
    
    processed_lines = []
    current_line = ''
    
    for line in lines:
        line = line.strip()  # Remove espaços em branco no início e no fim
        if line:  # Se a linha não estiver vazia
            if line[-1] in ['.', ':', ';', '-', '!', '?']:
                if current_line:
                    current_line += ' ' + line
                    processed_lines.append(current_line)
                current_line = ''
            else:
                current_line += ' ' + line
    
    # Adiciona a última linha se houver
    if current_line:
        processed_lines.append(current_line)
    
    return processed_lines

def extract_text_from_pdf(pdf_path):
    """
    
    """
    texto_total = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            texto_total += page.extract_text() + "\n"
    
    documents = preprocess_text(texto_total)
    
    # Adicionar cada linha ao índice como um documento separado
    for doc in documents:
        if doc.strip():  # Verifica se a linha não está vazia
            writer.add_document(content=doc)
    writer.commit()

    return documents

# Função para recuperar documentos relevantes
def retrieve_documents(query_str):
    ret = []
    with index.searcher() as searcher:
        query = QueryParser("content", index.schema).parse(query_str)
        results = searcher.search(query)
        for result in results:
            ret.append(result['content'])  

        return ret

# Função para gerar resposta usando o Llama
def generate_answer_llama(question, context):
    prompt = f"Contexto: {context}\n\nPergunta: {question}\nResposta: \n(lembre-se de não citar o contexto na resposta)"
    
    client = Groq(api_key='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')

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
        )

        answer = chat_completion.choices[0].message.content.strip()
        return answer

    except requests.exceptions.SSLError as e:
        print("Erro SSL: ", e)
        return "Houve um problema com a verificação do certificado SSL."
    except requests.exceptions.RequestException as e:
        print("Erro na requisição: ", e)
        return "Houve um problema com a requisição à API."

# Caminho para o arquivo PDF
pdf_path = '/home/elton/Documentos/Pessoal/Entrevistas/Neuralmint/Procuradoria Geral - Normas.pdf'
extract_text_from_pdf(pdf_path)

# Streamlit app
st.title("NeuralMind - Exercício seleção")
st.subheader("Chatbot vestibular da Unicamp 2025")

question = st.text_input("Digite sua pergunta:")
if question:
    # Exemplo de uso
    context = ''
    palavras_chave = " Vestibular Unicamp 2025 UV 2025"
    prompt_tratamento = f'retorne no prompt apenas os palavras chave e pronomes interrogativos desta frase (em pt/br): "{question}"'
    
    for i in range(3):
        answer = generate_answer_llama(prompt_tratamento+palavras_chave, 'não tem').replace('"', '').replace(',', '')
        top_documents = retrieve_documents(answer)
        if context not in top_documents and len(top_documents) > 0:
            context += " ".join(top_documents[:3])  # Use as três primeiras sentenças para formar o contexto
        prompt_tratamento = f'mude os pronomes interrogativos para seus sinonimos e retorne somente o resultado no prompt (em pt/br): {answer}\nSeja conciso.'


    answer = generate_answer_llama(question, context)
    st.subheader("Resposta Gerada:")
    st.write(answer)

