import csv

# Faturamento real > somar apenas os serviços com status concluído
def faturamento():
    # Quais já foram concluidos
    concluidos = []
    with open('atendimentos.csv', mode='r', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo)

        for linha in reader:
            status = linha[0].split(',')

            if status[-1] == 'concluido':
                concluidos.append(status)

        print(f'Foram concluidos: {len(concluidos)}')

    #Pegar o valor do serviço
    valores = []
    with open('atendimentos.csv', mode='r', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo)

        for linha in reader:
            valor = linha[0].split(',')

            if valor[-2]:
                valores.append(valor[-2])

        int_list = list(map(int, valores))
        total = sum(int_list)
        print(f'Faturamento total: {total}')


# Quantidade de atendimentos > quantos foram cancelados e pendentes
def atendimentos():
    with open('atendimentos.csv', mode='r', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo)
        #total de servicos realizados
        realizados = len(list(reader))
        print(f'Total de servicos agendados: {realizados}')

    pendentes = []
    with open('atendimentos.csv', mode='r') as arquivo:
        reader = csv.reader(arquivo)

        for linha in reader:
            status = linha[0].split(",")

            if status[-1] == 'pendente':
                pendentes.append(linha)
                total = len(pendentes)
        print(f'Total de servicos pendentes: {total}')
        print(f'Servicos pendentes: {pendentes}')

    cancelados = []
    with open('atendimentos.csv', mode='r') as arquivo:
        reader = csv.reader(arquivo)

        for linha in reader:
            status = linha[0].split(",")

            if status[-1] == 'cancelado':
                cancelados.append(linha)
                total = len(cancelados)
        print(f'Total de servicos cancelados: {total}')
        print(f'Servicos cancelados: {cancelados}')


# Serviço mais vendido
def serviço():
    mais_vendido = []
    with open('atendimentos.csv', mode='r', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo)
    
        for linha in reader:
            servico = linha[0].split(',')
    
            if servico[-3]:
                mais_vendido.append(servico[-3])
    
        print(f'Serviço mais vendido: {max(set(mais_vendido), key=mais_vendido.count)}')


# ticket médio
def ticket_medio():
    valores = []
    with open('atendimentos.csv', mode='r', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo)

        for linha in reader:
            valor = linha[0].split(',')

            if valor[-2]:
                valores.append(valor[-2])

        int_list = list(map(int, valores))
        total = sum(int_list)
        ticket_medio = total / len(int_list)
        print(f'Ticket médio: {ticket_medio:.2f}')


# Somar oq cada cliente gastou e Mostrar o cliente que mais gastou em serviços
def gastos_clientes():
    maior_gasto = {}
    with open('atendimentos.csv', mode='r', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo)

        for linha in reader:
            cliente = linha[0].split(',')

            if cliente[-5]:
                maior_gasto.update({cliente[-5]: int(cliente[-2])})

    print(f'Cliente que mais gastou: {max(maior_gasto, key=maior_gasto.get)} com o valor de R${max(maior_gasto.values())}')
        

# Alerta de pendentes
def alerta_pendentes():
    pendentes = []
    with open('atendimentos.csv', mode='r', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo)

        for linha in reader:
            status = linha[0].split(",")

            if status[-1] == 'pendente':
                pendentes.append(linha)
                qntd = len(pendentes)
                if qntd >= 3:
                    print(f'Alerta: Há {qntd} serviços pendentes!')


# Atendimentos:
# - Total: 5
# - Concluídos: 3
# - Cancelados: 1
# - Pendentes: 1

# Serviço mais vendido: Banho
# Ticket médio: R$ 60,00

# Cliente que mais gastou: Ana
# Total gasto: R$ 100,00
