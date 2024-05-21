import tabulate as tabulate 
import pandas as pd 
from colorama import init, Fore, Back, Style
import oracledb
import getpass

#conexão com o oracle
userpwd = getpass.getpass("Enter password: ")
connection = oracledb.connect(user="PEDRO", password=userpwd,
                              host="localhost", port=1521, service_name="XEPDB1")
cursor = connection.cursor()


  #listagem de produto
cursor = connection.cursor()
cursor.execute("select * from PRODUTOS")
rows = cursor.fetchall()
for row in rows:
    print(row)
#update
Cpa=int(input("Digite o código do produto que deseja atualizar:"))
up=str(input("Deseja atualizar o nome?(S/N)"))
up=up.lower()
if(up=='s'):
  Np=str(input("Digite o novo nome do produto:"))
  lista=[(Np,Cpa)]
  cursor = connection.cursor()
  cursor.executemany("""UPDATE PRODUTOS set nome_prod= :1 WHERE cod_prod= :2""",lista)
  connection.commit()

up=str(input("Deseja atualizar a descrição?(S/N)"))
up=up.lower()
if(up=='s'):
  Dp=str(input("Digite a nova descrição do produto:"))
  lista=[(Dp,Cpa)]
  cursor = connection.cursor()
  cursor.executemany("""UPDATE PRODUTOS set desc_prod= :1 WHERE cod_prod= :2""",lista)
  connection.commit()

up=str(input("Deseja atualizar o custo?(S/N)"))
up=up.lower()
if(up=='s'):
  Ca=str(input("Digite o novo custo do produto:"))
  lista=[(Ca,Cpa)]
  cursor = connection.cursor()
  cursor.executemany("""UPDATE PRODUTOS set custo_prod= :1 WHERE cod_prod= :2""",lista)
  connection.commit()

up=str(input("Deseja atualizar o custo fixo?(S/N)"))
up=up.lower()
if(up=='s'):
  Cf=str(input("Digite o novo custo fixo do produto:"))
  lista=[(Cf,Cpa)]
  cursor = connection.cursor()
  cursor.executemany("""UPDATE PRODUTOS set custo_fixo= :1 WHERE cod_prod= :2""",lista)
  connection.commit()

up=str(input("Deseja atualizar a comissão de vendas?(S/N)"))
up=up.lower()
if(up=='s'):
  Cv=str(input("Digite a nova comissão de vendas do produto:"))
  lista=[(Cv,Cpa)]
  cursor = connection.cursor()
  cursor.executemany("""UPDATE PRODUTOS set comissao_venda= :1 WHERE cod_prod= :2""",lista)
  connection.commit()

up=str(input("Deseja atualizar o imposto?(S/N)"))
up=up.lower()
if(up=='s'):
  Iv=str(input("Digite o novo imposto do produto:"))
  lista=[(Iv,Cpa)]
  cursor = connection.cursor()
  cursor.executemany("""UPDATE PRODUTOS set imposto= :1 WHERE cod_prod= :2""",lista)
  connection.commit()

up=str(input("Deseja atualizar a margem de lucro?(S/N)"))
up=up.lower()
if(up=='s'):
  Ml=str(input("Digite a nova margem de lucro do produto :"))
  lista=[(Ml,Cpa)]
  cursor = connection.cursor()
  cursor.executemany("""UPDATE PRODUTOS set margem_lucro= :1 WHERE cod_prod= :2""",lista)
  connection.commit()


cursor.close()
connection.close()


