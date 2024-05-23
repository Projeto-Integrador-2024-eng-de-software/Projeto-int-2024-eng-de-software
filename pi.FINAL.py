import tabulate as tabulate 
import oracledb
import getpass
import numpy as np
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
        soma = Cf + Cv + Iv
        while(soma > 100):
            print(f"Soma dos custos não pode ser mais que 100%")
            print(f"Recomece a inserção das informações para inserção")
            Cp = int(input("Informe o código do produto: "))
            Np = str(input("Informe o nome do produto: "))
            Dp = str(input("Informe a descrição do produto: "))
            Ca = float(input("Informe o custo do produto: "))
            Cf = float(input("Informe o custo fixo: "))
            Cv = float(input("Informe o quanto será a comissão de vendas: "))
            Iv = float(input("Informe os impostos: "))
            Ml = float(input("Informe a rentabilidade: "))

        if soma != 100:
            Pv = Ca / (1 - ((soma + Ml) / 100))
        else:
            Pv = Ca / 1

        if(Ml > 100):
            soma = soma * -1

        if (Pv < 0):
            Pv = Pv * (-1)
            print(f"{Pv}")
            Rb = Pv - Ca

        custoAq = Ca
        pca = Ca / Pv * 100
        receitaBruta = Pv - Ca
        Prb = receitaBruta / Pv * 100
        impostos = (Iv / 100) * Pv
        comissãoVendas = (Cv / 100) * Pv
        rentabilidade = (Ml / 100) * Pv
        outrosCustos = Cf + Cv + Iv
        outrosCustos1 = (Cf + Cv + Iv) / 100 * Pv 
        custoFixo = (Cf / 100) * Pv

        #tabela da inserção
        tabela = {
            "Descrição": ["A-Preço de venda", "B-Custo de aquisação(fornecedor)", "C-Receita Bruta(A-B)", "D-Custo fixo/administrativo", "E-Comissão de vendas", "F-Impostos", "G-Rentabilidade", "F-Outros Custos"],
            "Valor": [Pv, custoAq, receitaBruta, custoFixo, comissãoVendas, impostos, rentabilidade, outrosCustos1],
            "%": ["100%", (f"{pca}%"), (f"{Prb}%"), (f"{Cf}%"), (f"{Cv}%"), (f"{Iv}%"), (f"{Ml}%"), (f"{outrosCustos}%")]
        }

        print(tabulate.tabulate(tabela, headers='keys', tablefmt='fancy_grid'))

        #analise de faixa de lucro 
        if Ml > 20:
            nomeTab = "O lucro será Alto"
        elif Ml > 10 and Ml <= 20:
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
        
        # Criptografia da descrição
        # Matriz chave
        matriz_chave = np.array([[4, 3], [1, 2]])
        matriz_chave_inv = np.linalg.inv(matriz_chave)

        # Modulo 27 alfabeto (A-Z + espaço)
        mod = 27

        # Função para encontrar o inverso modular de um número
        def mod_inv(a, m):
            for x in range(1, m):
                if (a * x) % m == 1:
                    return x
            raise ValueError(f"Não existe inverso modular para {a} no módulo {m}")

        # Inverso da matriz chave no modulo 27
        det = int(np.round(np.linalg.det(matriz_chave)))
        det_inv = mod_inv(det % mod, mod)
        matriz_chave_inv_mod = (det_inv * np.round(det * np.linalg.inv(matriz_chave)).astype(int) % mod) % mod

        # Mapear caracteres para índices e vice-versa
        def char_para_indice(char):
            if char == ' ':
                return 26
            return ord(char) - ord('A')

        def indice_para_char(indice):
            if indice == 26:
                return ' '
            return chr(indice + ord('A'))

        # Função para criptografar uma mensagem
        def criptografar(mensagem):
            mensagem = mensagem.upper()

            if len(mensagem) % 2 != 0:
                mensagem += ' '
            
            mensagem_criptografada = ""
            for i in range(0, len(mensagem), 2):
                par = [char_para_indice(mensagem[i]), char_para_indice(mensagem[i+1])]
                par_criptografado = np.dot(matriz_chave, par) % mod
                mensagem_criptografada += ''.join(indice_para_char(x) for x in par_criptografado)
            
            return mensagem_criptografada

        mensagem = Dp
        mensagem_criptografada = criptografar(mensagem)
        print(f"Mensagem original: {mensagem}")
        print(f"Mensagem criptografada: {mensagem_criptografada}")

        #inserção no banco de dados
        data = [(Cp, Np, mensagem_criptografada, Ca, Cf, Cv, Iv, Ml)]
        cursor.executemany("INSERT INTO PRODUTOS (cod_prod, nome_prod, desc_prod, custo_prod, custo_fixo, comissao_vendas, imposto, margem_lucro) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)", data)
        connection.commit()

    #listagem de produto
    elif (A == 2):
        # Matriz chave
        matriz_chave = np.array([[4, 3], [1, 2]])

        # Modulo 27 alfabeto (A-Z + espaço)
        mod = 27

        # Inverso da matriz chave no modulo 27
        det = int(np.round(np.linalg.det(matriz_chave)))
        det_inv = 11
        matriz_chave_inv_mod = (det_inv * np.round(det * np.linalg.inv(matriz_chave)).astype(int) % mod) % mod

        # Mapear caracteres para índices e vice-versa
        def char_para_indice(char):
            if char == ' ':
                return 26
            return ord(char) - ord('A')

        def indice_para_char(indice):
            if indice == 26:
                return ' '
            return chr(indice + ord('A'))

        # Função para descriptografar uma mensagem
        def descriptografar(mensagem):
            mensagem_descriptografada = ""
            for i in range(0, len(mensagem), 2):
                par = [char_para_indice(mensagem[i]), char_para_indice(mensagem[i+1])]
                par_descriptografado = np.dot(matriz_chave_inv_mod, par) % mod
                mensagem_descriptografada += ''.join(indice_para_char(x) for x in par_descriptografado)
            
            return mensagem_descriptografada.strip()

        cursor.execute("SELECT * FROM PRODUTOS")
        rows = cursor.fetchall()

        products = []
        for row in rows:
            cod_prod = row[0]
            nome_prod = row[1]
            desc_prod_crip = row[2]
            custo_prod = row[3]
            custo_fixo = row[4]
            comissao_vendas = row[5]
            imposto = row[6]
            margem_lucro = row[7]

            desc_prod = descriptografar(desc_prod_crip)
            
            products.append([cod_prod, nome_prod, desc_prod, custo_prod, custo_fixo, comissao_vendas, imposto, margem_lucro])

        print(tabulate.tabulate(products, headers=["Código", "Nome", "Descrição", "Custo", "Custo Fixo", "Comissão Vendas", "Imposto", "Margem Lucro"], tablefmt='fancy_grid'))

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
