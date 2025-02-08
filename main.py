from bs4 import BeautifulSoup
import mysql.connector
import requests
import datetime

url = "https://www.pontaporainforma.com.br/"
lista_noticia = []  # lista para manchetes
lista_data = []  # lista para datas

def consulta_noticias():
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            conteudo = BeautifulSoup(response.content, "html.parser")

            noticias = conteudo.find_all("h3", class_="entry-title td-module-title")
            datas = conteudo.find_all("time", class_="entry-date updated td-module-date")

            for noticia, data in zip(noticias, datas):
                manchete_txt = noticia.get_text(strip=True)

                # pega a data correta
                data_txt = data["datetime"] if data.has_attr("datetime") else data.get_text(strip=True)

                # converte para YYYY-MM-DD
                try:
                    data_formatada = datetime.datetime.strptime(data_txt, "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    data_formatada = data_txt  # mantém o original se falhar

                lista_noticia.append(manchete_txt)
                lista_data.append(data_formatada)

            for i in range(len(lista_noticia)):
                print(lista_noticia[i], "--", lista_data[i])

    except requests.exceptions.RequestException as e:
        print("Erro ao acessar o site:", e)
    except Exception as e:
        print("Erro geral:", e)

def envia_BD(titulo, data):
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            database="uc5",
            password=""
        )
        print("Conectado ao banco de dados!")

        cursor = conexao.cursor()
        SQL = "INSERT INTO NOTICIAS (titulo, data_extracao) VALUES (%s, %s)"
        cursor.execute(SQL, (titulo, data))
        conexao.commit()
        print(f"Notícia salva: {titulo} - {data}")

    except mysql.connector.Error as e:
        print("Erro ao salvar no banco de dados:", e)
    finally:
        conexao.close()
        cursor.close()
        print("Conexão com o banco de dados encerrada.")

consulta_noticias()

# Insere no banco de dados apenas se houver dados suficientes
for i in range(min(max, len(lista_noticia))):
    envia_BD(titulo=lista_noticia[i], data=lista_data[i])
