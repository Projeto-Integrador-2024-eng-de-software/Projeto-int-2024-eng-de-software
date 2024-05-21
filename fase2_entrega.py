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
    #tabela com todos os produtos
cursor = connection.cursor()
cursor.execute("select * from PRODUTOS")
rows = cursor.fetchall()

headers = ["Código", "Nome", "Descrição", "Custo", "Custo Fixo", "Comissão Vendas", "Imposto", "Rentabilidade"]
dados_produtos = [[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]] for row in rows]

print(tabulate.tabulate(dados_produtos, headers=headers, tablefmt='fancy_grid'))
    
    #tabela com cada produto
cursor.execute("SELECT * FROM PRODUTOS")
rows = cursor.fetchall()

for row in rows:
    Ca = row[3]
    Cf = row[4]
    Cv = row[5]
    Iv = row[6]
    Ml = row[7]
    soma=Cf+Cv+Iv+Ml

    if(soma>100):
        print("ATENÇÃO!! VOCÊ NÃO PODE ULTRAPASSAR O VALOR DE 100% NA SOMA")
        break
        


    elif soma <= 100:
      Pv = Ca / (1 - (soma / 100))

    if(Ml>100):
      soma=soma*-1

    
    if (Pv<0):
      Pv=Pv*(-1)
    print(f"{Pv}")
    Rb = Pv - Ca

    custoAq = Ca
    pca=Ca/Pv*100
    receitaBruta = Pv-Ca
    Prb=receitaBruta/Pv*100
    impostos = (Iv/100) * Pv
    comissãoVendas =(Cv/100) * Pv
    rentabilidade = (Ml/100) * Pv
    outrosCustos = Cf+Cv+Iv
    outrosCustos1 = (Cf + Cv + Iv)/(100) * Pv 
    custoFixo = (Cf/100) * Pv

    if Ml > 20:
      nomeTab = "O lucro será Alto"
    elif Ml> 10 and Ml <= 20:
      nomeTab = "O lucro será Médio"
    elif Ml > 0 and Ml <= 10:
      nomeTab = "O lucro será Baixo"
    elif Ml == 0:
      nomeTab = "Não irá ter lucro nem prejuizo (equilíbrio)"
    elif Ml < 0:  
      nomeTab = "Prejuizo"
    
    lucro = Ml
    tabela1 = {
            "tabela2": ["Código", "Nome", "Descrição", "Custo", "Custo Fixo", "Comissão Vendas", "Imposto", "Rentabilidade"],
            "dados_tabela": [[row[0], row[1], row[2], Ca, row[4], row[5], row[6], row[7]]],
        }

    tabela2 = {
        "Descrição": ["A-Preço de venda", "B-Custo de aquisação(fornecedor)", "C-Receita Bruta(A-B)","D-Custo fixo/administrativo","E-Comissão de vendas", "F-Impostos", "G-Rentabilidade", "F-Outros Custos"],
        "Valor": [(f"{Pv:,.2f}"),(f"{custoAq:,.2f}"),(f"{receitaBruta:,.2f}"),(f"{custoFixo:,.2f}"),(f"{comissãoVendas:,.2f}"),(f"{impostos:,.2f}"),(f"{rentabilidade:,.2f}"),(f"{outrosCustos1:,.2f}")],
        "%": ["100%", (f"{pca:,.2f}%"), (f"{Prb:,.2f}%"),(f"{ row[4]}%"),(f"{ row[5]}%"), (f"{ row[6]}%"), (f"{ row[7]}%"), (f"{outrosCustos}%")]
    }
    tabLuc = {
          "Resultado": [f"{lucro}%", f"{nomeTab}"]
                }
        
    print("Dados do Produto:")
    print(tabulate.tabulate(tabela1['dados_tabela'], headers=tabela1['tabela2'], tablefmt='fancy_grid'))
    print("Tabela de Porcentagem:")
    print(tabulate.tabulate(tabela2, tablefmt='fancy_grid'))
    print(tabulate.tabulate(tabLuc, headers='keys', tablefmt="fancy_grid"))
    print("\nOutros Dados:")
    for key, value in tabela1.items():
        if key not in ['tabela2', 'dados_tabela', 'tabela_porcentagem']:
            print(f"{key}: {value}")
        print()

cursor.close()
connection.close()

