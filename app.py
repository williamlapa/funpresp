import streamlit as st
import pandas as pd
from datetime import date, datetime
import chart
import requests
from bs4 import BeautifulSoup
import db

COMMENT_TEMPLATE_MD = """{} - {}
> {}"""

def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")

st.set_page_config(layout="centered", page_icon="💬", page_title="Aplicativo Comentários")

MODELO_DATA = date.today().strftime('%Y-%m-%d')

st.title("💬 📈 💵 Comparação Perfis Funpresp")

# Importa planilha
@st.cache
def get_data_from_excel():
    usecols = [
              "Unnamed: 1",
              "Unnamed: 2", 
              "Unnamed: 3", 
              "Unnamed: 4", 
              "Unnamed: 5"
              ]
    resposta = requests.get('https://www.funpresp.com.br/fique-por-dentro/cotas/')
    soup = BeautifulSoup(resposta.text, 'html.parser')

    for i in soup.find_all('a'):
        # Testa se a palavra Historico está nos hiperlinks do excel obtidos na página e atribui variável link:
        if 'Historico' in i.get('href'):
          link = i.get('href')

    df_exec = pd.read_excel(link, 
              sheet_name='cotas plano Executivo', 
              skiprows= 5,
              usecols=usecols
              )

    df_legi = pd.read_excel(link, 
              sheet_name='cotas plano Legislativo', 
              skiprows= 5,
              usecols=usecols
              )
    #Ajustes nos data frames
    
    df_exec = df_exec.rename({"Unnamed: 1":"Data","Unnamed: 2":"Perfil_1", "Unnamed: 3":"Perfil_2", "Unnamed: 4":"Perfil_3","Unnamed: 5":"Perfil_4" }, axis='columns')
    df_exec = df_exec.set_index('Data')
    df_exec = df_exec.melt(value_name='cota', var_name='Perfil', ignore_index=False)
    df_exec['plano'] = 'Executivo'
    df_exec.reset_index('Data',inplace=True)
    df_exec = df_exec.astype({"Data": "datetime64[ms]"})
        
    df_legi = df_legi.rename({"Unnamed: 1":"Data","Unnamed: 2":"Perfil_1", "Unnamed: 3":"Perfil_2", "Unnamed: 4":"Perfil_3","Unnamed: 5":"Perfil_4" }, axis='columns')
    df_legi = df_legi.set_index('Data')
    df_legi = df_legi.melt(value_name='cota', var_name='Perfil', ignore_index=False)
    df_legi['plano'] = 'Legislativo'
    df_legi.reset_index('Data',inplace=True)
    df_legi = df_legi.astype({"Data": "datetime64[ms]"})

    df_total = df_exec.append(df_legi)
    return df_total

df_total = get_data_from_excel()

# usa o perfil definido no sidebar

plano = st.radio('Escolha o plano:', df_total["plano"].unique())

values = st.slider('Escolha o período: ',
     int(df_total.Data.dt.year.unique().min()), int(df_total.Data.dt.year.unique().max()), 
     (int(df_total.Data.dt.year.unique().min()), int(df_total.Data.dt.year.unique().max())))
st.write('Período:', values)

start_data = values[0]
final_data = values[1]
df_selection = df_total.query("@start_data <= Data <= @final_data & plano ==@plano")

source = df_selection
all_symbols = source.Perfil.unique() #Lista com nome dos perfis
symbols = st.multiselect("Escolha o perfil para visualização", all_symbols, all_symbols)

space(1)

# Criar grafico

source = source[source.Perfil.isin(symbols)]
chart = chart.get_chart(source, plano)
st.altair_chart(chart, use_container_width=True)

space(2)

# Comments part

conn = db.connect()
comments = db.collect(conn)

with st.expander("💬 Open comments"):

    # Show comments

    st.write("**Comments:**")

    for index, entry in enumerate(comments.itertuples()):
        st.markdown(COMMENT_TEMPLATE_MD.format(entry.name, entry.date, entry.comment))

        is_last = index == len(comments) - 1
        is_new = "just_posted" in st.session_state and is_last
        if is_new:
            st.success("☝️ Your comment was successfully posted.")

    space(2)

    # Insert comment

    st.write("**Add your own comment:**")
    form = st.form("comment")
    name = form.text_input("Name")
    comment = form.text_area("Comment")
    submit = form.form_submit_button("Add comment")

    if submit:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        db.insert(conn, [[name, comment, date]])
        if "just_posted" not in st.session_state:
            st.session_state["just_posted"] = True
        st.experimental_rerun()