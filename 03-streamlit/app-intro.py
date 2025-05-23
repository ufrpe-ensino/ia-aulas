import streamlit as st

st.title("Aula Introdutória: Streamlit")

st.header("Bem-vindo(a)!")
st.write("""
Este app foi criado para praticarmos o básico do Streamlit.
Siga as instruções e complete os exercícios propostos.
""")

st.subheader("Exemplo: Texto e Input")
nome = st.text_input("Digite seu nome:")
if nome:
    st.success(f"Olá, {nome}! Bem-vindo(a) à aula de Streamlit.")

st.subheader("Exemplo: Slider")
idade = st.slider("Selecione sua idade:", 0, 100, 18)
st.write(f"Sua idade é: {idade}")

st.markdown("---")

st.header("Exercícios")

st.subheader("Exercício 1: Checkbox")
# TODO: Adicione um checkbox que, quando marcado, exibe uma mensagem de parabéns.

st.subheader("Exercício 2: Selectbox")
# TODO: Adicione um selectbox com opções de cursos e exiba a opção escolhida.

st.subheader("Exercício 3: Upload de Arquivo")
# TODO: Adicione um componente para upload de arquivo e mostre o nome do arquivo enviado.

st.markdown("---")
st.info("Preencha os exercícios acima editando este arquivo!")