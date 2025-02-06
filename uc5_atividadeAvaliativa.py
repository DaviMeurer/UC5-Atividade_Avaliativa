from bs4 import BeautifulSoup
import mysql
import mysql.connector
import requests
import datetime

url = "https://www.pontaporainforma.com.br/"

def consulta_noticias():
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            conteudo = BeautifulSoup(response.content, "html.parser")

            noticias = conteudo.find_all("h3", class_ = "entry-title td-module-title")
            datas = conteudo.find_all("time", class_ = "entry-date updated td-module-date")

            i = 0
            lista_noticia = []
            lista_data = []
            for manchete in noticias:
                titulo = manchete.get_text()
                lista_noticia.append(titulo)

            for data in datas:
                lista_data.append(data[i].get_text())
                i+=1
            print (lista_noticia, lista_data)
    except requests.exceptions.RequestException as e:
        print ("Erro:", e)
    except Exception as e:
        print ("Erro: ", e)

def envia_BD():
    conexao = None
    cursor = None
    try:
        conexao = mysql.connector.connect(
            host = "localhost",
            user = "root",
            database = "uc5",
            password = ""
        )
        print("Conectado!")

        cursor = mysql.connector.cursor()
        SQL = "INSERT into NOTICIAS VALUES (%s, %s)"
        cursor.execute(SQL, (li, data))
        print(f"Salvo")

    except mysql.connector.Error as e:
        print("Erro: ", e)
    finally:
            conexao.close()
            cursor.close()

consulta_noticias()