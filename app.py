import psycopg2
from datetime import datetime, timezone
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from selenium.webdriver.suport.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.suport import expected_conditions as condicao_esperada

conexao = psycopg2.connect(
    database='railway',
    user='postgres',
    password='iLmWOVPGZU4fdqNqJxRl',
    host='containers-us-west-142.railway.app',
    port='5465'
)

sql = conexao.cursor()

def novo_produto(sql,conexao,nome,preco,site,data_cotacao,link_imagem):
    #Verificar se existe um produto igual já cadastrado
    query = "SELECT * FROM app_buscapreco_produto WHERE nome=%s and preco=%s and site=%s"
    valores = (nome, preco, site)
    resutado = sql.execute(query, valores)
    dados = sql.fetchall()

    if len(dados) == 0: 
        #Se não houver dados iguais, gravar um novo produto
        query = "INSERT INTO app_buscapreco_produto(nome,preco,site,data_cotacao,link_imagem) VALUES(%S,%S,%S,%S,%S)"
        valores = (nome,preco,site,data_cotacao,link_imagem)
    #Se já houver dados iguais, não gravar um novo produto
    else: 