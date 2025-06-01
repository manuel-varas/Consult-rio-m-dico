import mysql.connector as conn
from os import system
system("cls")
conexao = conn.connect(
host = "localhost",
user = "root",
password = "M@taturu.1981",
database = "consultorio_medical"
)

cursor = conexao.cursor()

print("Conectado ao Banco de Dados.")