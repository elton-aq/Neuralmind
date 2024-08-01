# Relatório do Projeto: Construção de um Chatbot para o Vestibular da Unicamp 2025

## [Chatbot](https://neuralmind-d62thqvrmakhyf7ih3byy4.streamlit.app)

## 1. Introdução

### Objetivo do Projeto
O objetivo deste projeto é desenvolver um chatbot inteligente que responda perguntas sobre o vestibular da Unicamp 2025. Utilizando a abordagem Retrieval Augmented Generation (RAG), o chatbot busca fornecer respostas precisas e contextuais baseadas na Resolução GR-029/2024.

### Visão Geral do Projeto
O projeto envolve a construção de um assistente conversacional usando um modelo de linguagem grande (LLM). O chatbot é desenvolvido com LLaMA3-70B, frameworks gratuitos como langchain e streamlit, e hospedado em uma plataforma gratuita. Inclui a criação de um índice para recuperação de informações e a implementação de um sistema de avaliação de respostas.

## 2. Metodologia

### Tecnologias e Ferramentas
- **Linguagem de Programação:** Python
- **Modelos de Linguagem:** LLaMA3-70B
- **Frameworks de Chatbot:** Langchain, Streamlit
- **Ferramentas de Busca:** Whoosh
- **Plataforma de Hospedagem:** Streamlit Share

### Desenvolvimento do Chatbot

O chatbot foi projetado para responder a perguntas com base em um contexto construído com dos documentos recuperados.

### Estrutura do Dataset
O dataset foi criado a partir da Resolução GR-029/2024. O processo incluiu:
1. **Extração de Texto:** Uso de PyPDF2 para extrair o texto do PDF.
2. **Pré-processamento:** Limpeza e formatação do texto para remover informações irrelevantes e dividir o texto em linhas.

## 3. Implementação

### Arquitetura do Sistema
A arquitetura inclui:
- **Frontend:** Desenvolvido com Streamlit, com uma abordagem simples e direta.
- **Backend:** Utiliza Whoosh para a recuperação de informações e LLaMA3-70B para a geração de respostas com contexto.
- **Modelo de Linguagem:** LLaMA3-70B para processamento de linguagem natural.

### Código

- **Função de Pré-processamento:** Remove informações irrelevantes e divide o texto em linhas.
- **Função de Extração de Texto:** Extrai texto de um PDF.
- **Função de Recuperação de Documentos:** Recupera documentos relevantes com base numa query.
- **Função de Geração de Resposta:** Utiliza o modelo LLaMA3-70B para gerar respostas a partir do contexto.
