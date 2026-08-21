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

    return concluidos

faturamento = faturamento()
print(faturamento)

# Quantidade de atendimentos > total de serviços realizados
# quantos foram cancelados e pendentes
def atendimentos():
    with open('atendimentos.csv', mode='r', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo)
        #total de servicos realizados
        realizados = len(list(reader))
        print(f'Total de serviços agendados: {realizados}')

atendimentos = atendimentos()
print(atendimentos)

# Serviço mais vendido
def serviço():
    pass

# ticket médio
def ticket_medio():
    pass

# Somar oq cada cliente gastou e Mostrar o cliente que mais gastou em serviços
def gastos_clientes():
    pass

# Alerta de pendentes
def alerta_pendentes():
    pass
