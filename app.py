import flet as ft
import mysql.connector

def conectar_bd():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            database="uc5",
            password=""
        )
        return conexao
    except mysql.connector.Error as e:
        print("Erro ao conectar no banco:", e)
        return None

def buscar_dados():
    conexao = conectar_bd()
    if not conexao:
        return []

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, titulo, data_extracao FROM NOTICIAS")
        dados = cursor.fetchall()
        return dados
    except mysql.connector.Error as e:
        print("Erro ao buscar dados:", e)
        return []
    finally:
        if conexao:
            conexao.close()

def main(page: ft.Page):
    page.title = "Noticias Extraídas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 800
    page.window_height = 600

    titulo = ft.Text("📢 Notícias Extraídas", size=24, weight="bold", color="blue600")
    
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Título")),
            ft.DataColumn(ft.Text("Data de Extração")),
        ],
        rows=[],
        expand=True
    )

    def carregar_dados():
        tabela.rows.clear()
        for id_noticia, titulo, data in buscar_dados():
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(id_noticia))),
                        ft.DataCell(ft.Text(titulo, tooltip=titulo)),
                        ft.DataCell(ft.Text(data)),
                    ]
                )
            )
        page.update()

    btn_atualizar = ft.ElevatedButton("🔄 Atualizar", on_click=lambda e: carregar_dados(), bgcolor="blue600", color="white")

    page.add(
        ft.Column(
            controls=[
                titulo,
                tabela,
                btn_atualizar
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START
        )
    )

    carregar_dados()

ft.app(target=main)