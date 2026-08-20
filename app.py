import csv

# Faturamento real > somar apenas os serviços com status concluído
def faturamento():
    # Quais já foram concluidos
    concluidos = []

    with open('atendimentos.csv', mode='r', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo)

        for linha in reader:
            dados = linha[0].split(',')

            if dados[-1] == 'concluido':
                concluidos.append(dados)
    #Pegar o valor do serviço

    return concluidos
faturamento = faturamento()
print(faturamento)



# Quantidade de atendimentos > total de serviços realizados, quantos foram concluídos,
# quantos foram cancelados e pendentes
def atendimentos():
    pass

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
