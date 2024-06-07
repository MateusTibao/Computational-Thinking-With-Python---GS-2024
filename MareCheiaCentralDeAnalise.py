import json
from datetime import datetime
import matplotlib.pyplot as plt
import math

# IMPORTAÇÃO DE BIBLIOTECAS ▲
# TRATAMENTO DE DADOS ▼

def importar_dados(caminho_arquivo):
    # Importação de dados via arquivo .json
    try:
        with open(caminho_arquivo, 'r') as f:
            dados = json.load(f)
        return dados
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho_arquivo}' não encontrado. Impossível continuar, verifique e reinicie.")
        exit()
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo JSON '{caminho_arquivo}'. Verifique a formatação do arquivo.")
    return []

def selecionar_regiao(dados):
    # Exibição das regiões disponíveis usando generator expression com set evitando duplicatas e geração de lista antes do necessário
    regioes = list(set(item['regiao'] for item in dados))
    print("Regiões disponíveis:")
    for i, regiao in enumerate(regioes):
        print(f"{i + 1} - {regiao}")

    # Loop para seleção da região
    while True:
        try:
            opcao = int(input("\nDigite o número da região desejada: "))
            if 1 <= opcao <= len(regioes):
                regiao_selecionada = regioes[opcao - 1]
                return regiao_selecionada, [item for item in dados if item['regiao'] == regiao_selecionada]
            else:
                print("Opção inválida. Por favor, digite um número válido.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

def exibir_periodo_disponivel(dados):
    # Mesma lógica da exibição das região mas aqui as datas são ordenadas para ser possível selecionar a mais antiga e a mais recente
    datas = sorted(set(item['data'] for item in dados))
    data_inicio = datas[0]
    data_fim = datas[-1]
    print(f"\nPeríodo disponível de {data_inicio} a {data_fim}")

def selecionar_periodo():
    # Loop de seleção do período fazendo as devidas validações
    while True:
        data_inicio = input("\nDigite a data de início (AAAA-MM-DD): ").strip()
        data_fim = input("Digite a data de fim (AAAA-MM-DD): ").strip()
        if len(data_inicio) == 10 and len(data_fim) == 10:
            try:
                data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
                data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
                if data_inicio_dt <= data_fim_dt:
                    return {'data_inicio': data_inicio, 'data_fim': data_fim}
                else:
                    print("Erro: a data de início deve ser anterior ou igual à data de fim.")
            except ValueError:
                print("Erro: formatação de data inválida. Certifique-se de usar o formato AAAA-MM-DD.")
        else:
            print("Erro: formatação de data inválida. Certifique-se de usar o formato AAAA-MM-DD.")

def filtrar_por_periodo(dados, data_inicio, data_fim):
    # Converte strings de data de início e fim para objetos datetime
    data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
    data_fim = datetime.strptime(data_fim, '%Y-%m-%d')

    # Retorna uma lista de itens cuja data está dentro do intervalo especificado com list comprehension
    return [item for item in dados if data_inicio <= datetime.strptime(item['data'], '%Y-%m-%d') <= data_fim]

# TRATAMENTO DE DADO ▲
# CÁLCULOS ▼

def calcular_media(dados, atributo):
    # Cálculo da média e arrendamento do resultado
    valores = [item[atributo] for item in dados]
    return round(sum(valores) / len(valores), 2)

def calcular_desvio_padrao(dados, atributo):
    # Cálculo do desvio padrão e arrendamento do resultado
    valores = [item[atributo] for item in dados]
    media = calcular_media(dados, atributo)
    variancia = sum((x - media) ** 2 for x in valores) / len(valores)
    return round(math.sqrt(variancia), 2)

def calcular_minimo(dados, atributo):
    # Retorno do mínimo
    valores = [item[atributo] for item in dados]
    return min(valores) if valores else 0

def calcular_maximo(dados, atributo):
    # Retorno do mínimo
    valores = [item[atributo] for item in dados]
    return max(valores) if valores else 0

def calcular_variancia(dados, atributo):
    # Cálculo da variância
    valores = [item[atributo] for item in dados]
    media = calcular_media(dados, atributo)
    return round(sum((x - media) ** 2 for x in valores) / len(valores), 2)

def imprimir_calculos(dados, tipo_calculo, atributos):
    # Itera sobre cada atributo e seu nome, realizando o cálculo correspondente e imprimindo o resultado
    print(f"\n{tipo_calculo.capitalize()} para todos os atributos:\n")
    for atributo, nome in atributos.items():
        if tipo_calculo == 'media':
            valor = calcular_media(dados, atributo)
        elif tipo_calculo == 'desvio_padrao':
            valor = calcular_desvio_padrao(dados, atributo)
        elif tipo_calculo == 'minimo':
            valor = calcular_minimo(dados, atributo)
        elif tipo_calculo == 'maximo':
            valor = calcular_maximo(dados, atributo)
        elif tipo_calculo == 'variancia':
            valor = calcular_variancia(dados, atributo)
        print(f"{nome}: {valor}")

# CÁLCULOS ▲
# GRÁFICOS ▼

def gerar_grafico_linha(dados, atributo):
    # Geração do gráfico de linha usando matplotlib.pyplot
    datas = [item['data'] for item in dados]
    valores = [item[atributo] for item in dados]

    plt.figure(figsize=(10, 6))
    plt.plot(datas, valores, marker='o', linestyle='-', color='b')
    plt.xlabel('Data')
    plt.ylabel(atributo.capitalize())
    plt.title(f'Gráfico de {atributo.capitalize()} por data')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def gerar_grafico_colunas(dados, atributo):
    # Geração do gráfico de colunas usando matplotlib.pyplot
    datas = [item['data'] for item in dados]
    valores = [item[atributo] for item in dados]

    plt.figure(figsize=(10, 6))
    plt.bar(datas, valores, color='b')
    plt.xlabel('Data')
    plt.ylabel(atributo.capitalize())
    plt.title(f'Gráfico de Colunas de {atributo.capitalize()} por Data')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def exibir_opcoes_grafico(atributos):
    # Sub-menu para seleção do tipo de gráfico
    print("\nVÁRIAVEL DO GRÁFICO:")
    for i, atributo in enumerate(atributos):
        print(f"{i + 1} - {atributos[atributo]}")
    while True:
        try:
            opcao = int(input("\nDigite o número do atributo para gerar o gráfico: "))
            if 1 <= opcao <= len(atributos):
                return list(atributos.keys())[opcao - 1]
            else:
                print("Opção inválida. Por favor, digite um número válido.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

# GRÁFICOS ▲
# GERAIS ▼

def main():
    dados = importar_dados('dados.json')

    while True:
        # Seleção da região e do período antes do looping para enviar fluxo sem a seleção
        regiao_selecionada, dados_regiao = selecionar_regiao(dados)
        exibir_periodo_disponivel(dados)
        periodo_selecionado = selecionar_periodo()

        # Mapeiamento os nomes técnicos dos atributos para descrições legíveis para os usuários
        atributos = {
            'temp': 'Temperatura',
            'turbidez': 'Turbidez',
            'ph': 'pH',
            'presenca_de_peixes': 'Presença de Peixes'
        }

        # Loop do menu principal com acesso e recrutamento das funções do código
        while True:

            # Definição as datas de início e fim do período selecionado pelo usuário
            data_inicio = periodo_selecionado['data_inicio']
            data_fim = periodo_selecionado['data_fim']

            # Filtro final dos dados da região selecionada para o período especificado
            dados_periodo = filtrar_por_periodo(dados_regiao, data_inicio, data_fim)

            print(f"\nPeríodo: de {data_inicio} até {data_fim}\nRegião: {regiao_selecionada}\n")
            print("1 - Calcular Médias")
            print("2 - Calcular Desvios Padrões")
            print("3 - Calcular Variâncias")
            print("4 - Calcular Mínimas")
            print("5 - Calcular Máximas")
            print("6 - Gerar Gráfico de Linhas Específico")
            print("7 - Gerar Gráfico de Colunas Específico")
            print("8 - Selecionar Novo Período")
            print("0 - Selecionar Nova Região")
            print("S - Sair")

            opcao = input("\nDigite o número da opção desejada: ").strip().lower()

            if opcao == '1':
                imprimir_calculos(dados_periodo, 'media', atributos)
            elif opcao == '2':
                imprimir_calculos(dados_periodo, 'desvio_padrao', atributos)
            elif opcao == '3':
                imprimir_calculos(dados_periodo, 'variancia', atributos)
            elif opcao == '4':
                imprimir_calculos(dados_periodo, 'minimo', atributos)
            elif opcao == '5':
                imprimir_calculos(dados_periodo, 'maximo', atributos)
            elif opcao == '6':
                atributo = exibir_opcoes_grafico(atributos)
                gerar_grafico_linha(dados_periodo, atributo)
            elif opcao == '7':
                atributo = exibir_opcoes_grafico(atributos)
                gerar_grafico_colunas(dados_periodo, atributo)
            elif opcao == '8':
                periodo_selecionado = selecionar_periodo()
            elif opcao == '0':
                break
            elif opcao == 's':
                print("Encerrando o programa...")
                return
            else:
                print("Opção inválida. Por favor, digite um número válido ou 'S' para sair.")

main()
