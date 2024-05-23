import tabulate as tabulate 
import pandas as pd 
from colorama import init, Fore, Back, Style
import oracledb
import getpass
A=0
while(A!=5):
    A=int(input("Digite 1 para inserir, 2 para listar, 3 para atualizar, 4 para deletar ou 5 para cancelar: "))
    #conexão com o oracle
    userpwd = getpass.getpass("Enter password: ")
    connection = oracledb.connect(user="PEDRO", password=userpwd,
                                host="localhost", port=1521, service_name="XEPDB1")
    cursor = connection.cursor()

    #inserir um produto
    if(A==1):
    # todas as variaves do cadastro de produto
        Cp = int(input("Informe o código do produto: "))
        Np = str(input("Informe o nome do produto: "))
        Dp = str(input("Informe a descrição do produto: "))
        Ca = float(input("Informe o custo do produto: "))
        Cf = float(input("Informe o custo fixo: "))
        Cv = float(input("Informe o quanto será a comissão de vendas: "))
        Iv = float(input("Informe os impostos: "))
        Ml = float(input("Informe a rentabilidade: "))



        #calculo do preço de venda  
        soma=Cf+Cv+Iv
        while(soma>100):
            print(f"Soma dos custos não pode ser mais que 100%")
            print(f"Recomeçe a inserção das informações para inserção")
            Cp = int(input("Informe o código do produto: "))
            Np = str(input("Informe o nome do produto: "))
            Dp = str(input("Informe a descrição do produto: "))
            Ca = float(input("Informe o custo do produto: "))
            Cf = float(input("Informe o custo fixo: "))
            Cv = float(input("Informe o quanto será a comissão de vendas: "))
            Iv = float(input("Informe os impostos: "))
            Ml = float(input("Informe a rentabilidade: "))

        if soma != 100:
            Pv = Ca / (1 - ((soma+Ml) / 100))
        else:
            Pv = Ca /1

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


        #tabela da inserção
        tabela = {
            "Descrição": ["A-Preço de venda", "B-Custo de aquisação(fornecedor)", "C-Receita Bruta(A-B)","D-Custo fixo/administrativo","E-Comissão de vendas", "F-Impostos", "G-Rentabilidade", "F-Outros Custos"],
            "Valor": [Pv,custoAq,receitaBruta,custoFixo,comissãoVendas,impostos,rentabilidade,outrosCustos1],
            "%": ["100%", (f"{pca}%"), (f"{Prb}%"),(f"{Cf}%"),(f"{Cv}%"), (f"{Iv}%"), (f"{Ml}%"), (f"{outrosCustos}%")]
        }

        print(tabulate.tabulate(tabela, headers='keys', tablefmt='fancy_grid'))

        #analise de faixa de lucro 

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

        #tabela de lucro
        tabLuc = {
        "Resultado": [f"{lucro}%", f"{nomeTab}"]
        }
        print(tabulate.tabulate(tabLuc, headers='keys', tablefmt="fancy_grid"))
        #inserção no banco de dados
        data=[(Cp,Np,Dp,Ca,Cf,Cv,Iv,Ml)]
        cursor.executemany("insert into PRODUTOS (cod_prod, nome_prod, desc_prod, custo_prod, custo_fixo, comissao_vendas, imposto, margem_lucro) values (:1, :2, :3, :4, :5, :6, :7, :8)",data)
        connection.commit()                                                    





    #listagem de produto
    elif (A == 2):
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
    
    #atualização de produtos
    elif(A==3):
        
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


    #deletar produtos
    elif(A==4):
        cursor = connection.cursor()
        cursor.execute("select * from PRODUTOS")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        Cpd=int(input("Digite o código do produto que deseja deletar:"))
        D=str(input("Deseja mesmo deletar o produto(S/N)? "))
        D=D.lower()
        if(D=='n'):
            print(f"Produto não deletado") 
        elif(D=='s'):
            delete="DELETE FROM PRODUTOS WHERE cod_prod= :Cpd"
            cursor.execute(delete, Cpd=Cpd)
            connection.commit()
            print(f"Produto deletado com sucesso")


    cursor.close()
    connection.close()