import psycopg2
from datetime import datetime, timezone
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as condicao_esperada
import schedule
from time import sleep

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
        sql.execute(query, valores)
    else:
        print('Dados já cadastrados anteriormente!')
    #Se já houver dados iguais, não gravar um novo produto
# novo_produto(sql,conexao,'Iphone 15',13000.50,'apple.com/iphone15',datetime.now(),'www.imagem.com/imagem1.jpg')
    conexao.commit()

# Criar um web scraper(atras do selenium)

# Iniciar o webdriver


def iniciar_driver():
    chrome_options = Options()

    arguments = ['--lang=en-US', '--window-size=1300,1000',
                 '--incognito']

    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1

    })

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
        ]
    )
    return driver, wait

def varrer_site1():
    # 1 - entrar no site - http://site1produto.netlify.app/
    driver, wait = iniciar_driver()
    driver.get("http://site1produto.netlify.app/")
    # 2 - anotar o nome do produto
    nome = wait.until(condicao_esperada.visibility_of_all_elenebts_located((By.XPATH,"//div[@class='detail-box']/a")))
    # 3 - anotar preço
    precos = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH,"//h6[@class='price_heading']")))
    # 4 - anotar o link de onde foi extraido a informacao
    site = driver.current_url
    # 5 - anotar o link da imagem
    links_imagem = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH,"//div[@class='img-box']/img")))
    nome_iphone = nomes[0].text
    nome_gopro = nomes[1].text

    precos_iphone = precos[0].text.split(' ')[1]
    precos_gopro = precos[1].text.split(' ')[1]

    links_imagem_iphone = links_imagem[0].get.attribute('src')
    links_imagem_gopro = links_imagem[1].get.attribute('src') 

    novo_produto(sql, conexao, nome_iphone, preco_iphone, site, datetime.now(), links_imagem_iphone)
    novo_produto(sql, conexao, nome_gopro, preco_gopro, site, datetime.now(), links_imagem_gopro)   
        
    

def varrer_site2():
    
    driver, wait = iniciar_driver()
    driver.get("http://site2produto.netlify.app/")    
    nome = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH,"//div[@class='why-text']")))
    precos = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH,"//div[@class='why-text']//h5")))
    imagens = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH,"//img[@class='img-fluid']")))

    nome_iphone = nomes[0].text.split('\n')[0]
    nome_gopro = nomes[1].text.split("\n")[0]

    precos_iphone = precos[0].text.split('$')[1]
    precos_gopro = precos[1].text.split('$')[1]

    links_imagem_iphone = links_imagem[0].get.attribute('src')
    links_imagem_gopro = links_imagem[1].get.attribute('src') 

    novo_produto(sql, conexao, nome_iphone, float(preco_iphone), driver.current_url, datetime.now(), links_imagem_iphone)
    novo_produto(sql, conexao, nome_gopro, float(preco_gopro), driver.current_url, datetime.now(), links_imagem_gopro)   

    print('site2 varrido')
        

def varrer_site3():
    driver, wait = iniciar_driver()
    driver.get("http://site3produto.netlify.app/")    
    nome = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH,"//div[@class='product_item_text']//h6/a")))
    precos = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH,"//div[@class='product_item_text']//h5")))
    imagens = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH,"//img[@class='product_item_pic set-bg']")))

    nome_iphone = nomes[0].text.split('\n')[0]  
    nome_gopro = nomes[1].text.split("\n")[0]

    precos_iphone = precos[0].text.split('$')[1]
    precos_gopro = precos[1].text.split('$')[1]

    links_imagem_iphone = driver.current_url+imagens[0].get.attribute('style').split(" ")[1][5:-3]
    links_imagem_gopro = driver.current_url+imagens[1].get.attribute('style').split(" ")[1][5:-3]

    novo_produto(sql, conexao, nome_iphone, float(preco_iphone), driver.current_url, datetime.now(), links_imagem_iphone)
    novo_produto(sql, conexao, nome_gopro, float(preco_gopro), driver.current_url, datetime.now(), links_imagem_gopro)   

    print('site3 varrido')

    def roda_tarefas():
        varrer_site1()
        varrer_site2()
        varrer_site3()

    schedule.every().day.at('06:00').do(roda_tarefas)
    while True:
        schedule.run_pending()
        sleep(1)