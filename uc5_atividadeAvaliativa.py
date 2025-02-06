from bs4 import BeautifulSoup
import mysql
import mysql.connector
import requests
import datetime

url = "https://www.pontaporainforma.com.br/"

try:
    response = requests.get(url)
    response.raise_for_status()

    if response.status_code == 200:
        conteudo = BeautifulSoup(response.content, "html.parser")

        noticias = conteudo.find_all("h3", class_ = "entry-title td-module-title")
        data = conteudo.find_all("time", class_ = "entry-date updated td-module-date")
        i = 0
        for manchete in noticias:
            titulo = manchete.get_text()
            print(f"{i+1} {titulo}\n"
                f"{data[i].get_text()}\n")
            i+=1

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
        cursor.execute(SQL, (noticias, data))
        print(f"Salvo")

    except mysql.connector.Error as e:
        print("Erro: ", e)
    finally:
            conexao.close()
            cursor.close()
        