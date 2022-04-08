import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st
import json


def collect():
    #Escopo utilizado
    scope = ['https://spreadsheets.google.com/feeds']

    #Dados de autenticação - troquei o from_json_keyfile_name pelo *dict e aí ele aceitou o arquivo TOML do Secrects
    #valor original
    #credentials = ServiceAccountCredentials.from_json_keyfile_name('cotasprev-cfcb011c0f86.json', scope) 
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["cotasprevread"], scope)

    gc = gspread.authorize(credentials)

    #Abre a planilha
    wks = gc.open_by_key('1XUIUWzHTXpCy7XMBpe5zBaQUpAQqdy27kbbC-Dooh3w')

    #Seleciona a primeira página da planilha
    worksheet = wks.get_worksheet(0)
    return worksheet

def sheet_pandas(worksheet):
    dados = worksheet.get_all_records()
    df = pd.DataFrame(dados)
    return df
