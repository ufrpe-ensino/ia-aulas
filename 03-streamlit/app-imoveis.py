import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

st.set_page_config(page_title="Visualização de Dados Imóveis Recife", layout="wide")
st.title("Visualização de Dados e Estatísticas Descritivas - Imóveis Recife")



# Obter página da query string
# page = st.query_params.get("page", "estatisticas").lower()

# Carregar dados
@st.cache_data
def load_data():
    data_url = "https://raw.githubusercontent.com/ProfLuciano/intro_cd/gh-pages/data/recife.csv"
    houses = pd.read_csv(data_url, encoding="ISO-8859-1")
    return houses

houses = load_data()
houses['operation'] = 'sell'
houses.loc[(houses['price'] > 100) & (houses['price'] < 30000), 'operation'] = 'rent'


# Sidebar com menu de links
st.sidebar.markdown("### Escolha a página:")
page = st.sidebar.selectbox(
    "Selecione uma página:",
    ("estatisticas", "geoloc"),
    key="page",
)

bairros = houses['suburb'].unique()
bairros = np.append(bairros, '-Todos-')
bairros = np.sort(bairros)
st.sidebar.markdown("### Filtros:")
bairro = st.sidebar.selectbox(
    "Selecione um bairro:",
    bairros,
    key="bairro",
)

if bairro != '-Todos-':
    houses = houses[houses['suburb'] == bairro]
    # st.sidebar.markdown(f"### Filtro aplicado: {bairro}")


if page == "estatisticas":
    st.header("Estatísticas Descritivas")
    st.dataframe(houses)

    col1, col2 = st.columns(2)

    with col1:
        st.write("Dimensões do DataFrame:", houses.shape)
        st.write("Tipos das colunas:")
        st.write(houses.dtypes)
        st.write("Estatísticas gerais:")
        st.write(houses.describe())
        st.subheader("Média, Mediana, Moda, Variância e Desvio Padrão do Preço")
        st.write({
            'Média': houses['price'].mean(),
            'Mediana': houses['price'].median(),
            'Moda': houses['price'].mode()[0],
            'Variância': houses['price'].var(),
            'Desvio padrão': houses['price'].std()
        })
        st.subheader("Estatísticas da Área")
        st.write(houses['area'].describe())

    with col2:
        st.subheader("Correlação de Pearson (Venda)")
        pearson_corr = houses.loc[houses.operation=='sell', ['price', 'bedrooms', 'area', 'bathrooms', 'ensuites']].corr(method='pearson')
        fig, ax = plt.subplots()
        sns.heatmap(pearson_corr, annot=True, cmap='coolwarm', center=0, ax=ax)
        st.pyplot(fig)

        st.subheader("Correlação de Spearman (Venda)")
        spearman_corr = houses.loc[houses.operation=='sell', ['price', 'bedrooms', 'area', 'bathrooms', 'ensuites']].corr(method='spearman')
        fig2, ax2 = plt.subplots()
        sns.heatmap(spearman_corr, annot=True, cmap='coolwarm', center=0, ax=ax2)
        st.pyplot(fig2)

    st.header("Visualizações")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Histograma dos Preços (milhares)")
        fig3, ax3 = plt.subplots()
        (houses['price']/1000).hist(bins=30, figsize=(8,4), ax=ax3)
        ax3.set_title('Distribuição dos Preços (milhares)')
        ax3.set_xlabel('Preço (milhares)')
        ax3.set_ylabel('Frequência')
        st.pyplot(fig3)

        st.subheader("Gráfico de Barras: Quantidade de Imóveis por Tipo")
        fig5, ax5 = plt.subplots()
        houses['type'].value_counts().plot(kind='bar', figsize=(8,4), ax=ax5)
        ax5.set_title('Quantidade de Imóveis por Tipo')
        ax5.set_xlabel('Tipo')
        ax5.set_ylabel('Contagem')
        st.pyplot(fig5)

    with col4:
        st.subheader("Boxplot da Área dos Imóveis")
        fig4, ax4 = plt.subplots()
        houses.boxplot(column=['area'], ax=ax4)
        ax4.set_title('Boxplot da Área dos Imóveis')
        ax4.set_ylabel('Área (m²)')
        st.pyplot(fig4)

        st.subheader("Gráfico de Dispersão: Área vs Preço")
        fig6, ax6 = plt.subplots()
        houses.plot.scatter(x='area', y='price', alpha=0.5, ax=ax6)
        ax6.set_title('Área vs Preço')
        ax6.set_xlabel('Área (m²)')
        ax6.set_ylabel('Preço')
        st.pyplot(fig6)
elif page == "geoloc":
    st.header("Visualização Geográfica")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Mapa de Pontos (Venda e Aluguel)")
        mapa = folium.Map(location=[-8.05, -34.9], zoom_start=12)
        for _, row in houses.iterrows():
            if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=3,
                    color='blue' if row['operation'] == 'sell' else 'green',
                    fill=True,
                    fill_opacity=0.6,
                    popup=f"Preço: R${row['price']}\nTipo: {row['type']}"
                ).add_to(mapa)
        st_folium(mapa, width=700, height=400)

    with col2:
        st.subheader("Heatmap dos Preços de Venda")
        rent_houses = houses[(houses['operation'] == 'sell') & 
                             houses['latitude'].notnull() & 
                             houses['longitude'].notnull() & 
                             houses['price'].notnull()]
        heatmap_map = folium.Map(location=[-8.05, -34.9], zoom_start=12)
        HeatMap(
            data=rent_houses[['latitude', 'longitude', 'price']].values,
            radius=10,
            max_zoom=13
        ).add_to(heatmap_map)
        st_folium(heatmap_map, width=700, height=400)

