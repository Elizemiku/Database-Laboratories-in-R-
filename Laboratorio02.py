#!/usr/bin/python

# Nome: Elizabeth Borgognoni Souto RA: 170409
# Laboratorio02

# importando os pacotes necessarios
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Exercicio 01 #

# Questao 1

# importando a tabela chuvas e transformando os //// em valores NaN como o NA do R
chuva = pd.read_csv("http://www.ime.unicamp.br/~gvludwig/2018s2-me315/INMET-14JAN2018-14AUG2018-SOROCABA.csv",
                    na_values=["////"])

# analisando a estrutura do dataframe como o comando str no R faz
chuva.info()

# mudando as variaveis datas para tipo de datetime
chuva['data'] = pd.to_datetime(chuva['data'], dayfirst=True)

# mudando as variavel precipitacao para float
chuva['precipitacao'] = chuva['precipitacao'].astype(float)

# excluindo a primeira e ultima linha de chuva selecionando apenas as linhas de index 1 a 4974
chuva = chuva.iloc[1:4975]

# soma de precipitacao de cada dia
chuva_por_dia = chuva[['data', 'precipitacao']].groupby('data').sum().reset_index()

# criando a variavel para acumular a chuva de 10 em 10 dias criando grupos
variavel_auxiliar = pd.date_range(start='2018-01-15', end='2018-08-13', freq='10D')

# funcao que cria os grupos de 10 em 10 dias

def group10(x):
    datas = variavel_auxiliar
    for i in range(0, len(datas)-1):
        if ((x >= datas[i]) & (x < datas[i+1])):
            return i
        else:
             pass
    return float('NaN')

# aplicando os grupos no dataframe e tirando os valores NaN
chuva_por_dia['grupo'] = chuva_por_dia['data'].apply(func = group10)
chuva_por_dia = chuva_por_dia.dropna()
chuva_por_grupo = chuva_por_dia.groupby('grupo').sum().reset_index()

# Grafico de series temporais
# Agrupei os dias e fiz um grafico de 2 em 2 meses
fig, ax = plt.subplots()
ax.plot(chuva_por_dia['data'], chuva_por_dia['precipitacao'])
ax.set_title('Grafico de series temporais')
plt.show()

# funcao de alisamento da questao 2
# x (lista), alpha - constante de 0 a 1

def alis_exp(x, alpha):
    """Funcao que calcula o alisamento exponencial"""
    if (alpha <= 0.0) | (alpha >= 1.0):
        raise ValueError("alpha deve ser um numero entre 0 e 1")
    else:
        n = len(x)-1
        y = np.empty(n, float)
        y[0] = x[0]
        for i in range(1, n):
            y[i] = alpha*x[i] + (1-alpha)*y[i - 1]
        return y

# testar com os parametros alpha = 0.2 e alpha = 0.8 e x = precipitacao de chuva_por_grupo
chuva_por_grupo['alisadoA'] = pd.DataFrame(alis_exp(chuva_por_grupo['precipitacao'], 0.2))
chuva_por_grupo['alisadoB'] = pd.DataFrame(alis_exp(chuva_por_grupo['precipitacao'], 0.8))

# manipulacao para fazer o grafico com o eixo de datas
chuva_por_grupo['data'] = variavel_auxiliar[:-1]

# grafico do alisamento exponencial
chuva_por_grupo.plot(x = 'data', y = ['precipitacao', 'alisadoA', 'alisadoB'])
plt.title('Alisamento exponencial por data') # para colocar titulo no grafico
plt.show()

# Exercicio 02 #

# importando a tabela baby e transformando os //// em valores NaN como o NA do R
baby = pd.read_csv("http://www.ime.unicamp.br/~gvludwig/2018s2-me315/baby-names.csv")

# analisando a estrutura do dataframe como o comando str no R faz
baby.info()

# construindo as tabelas

babymeninos = baby[(baby.sex == 'boy')]
babymeninas = baby[(baby.sex == 'girl')]

# pegando a ultima letra de cada nome
babymeninos['endswith'] = babymeninos.loc[:, 'name'].apply(lambda x: x[-1])
babymeninas['endswith'] = babymeninas.loc[:, 'name'].apply(lambda x: x[-1])

# para criar a quantidade de ultimas letras que aparecem por grupo de decada
endswith_meninos = babymeninos.groupby((babymeninos.year // 10) * 10)['endswith'].value_counts()
endswith_meninas = babymeninas.groupby((babymeninas.year // 10) * 10)['endswith'].value_counts()

# para poder criar os anos por decadas preciso arrumar as colunas e juntar as decadas
meninos = endswith_meninos.to_frame()
meninas = endswith_meninas.to_frame()

meninos = meninos.rename(columns = {'year':'year', 'endswith':'endswith', 'endswith':'count'}).reset_index()
meninas = meninas.rename(columns = {'year':'year', 'endswith':'endswith', 'endswith':'count'}).reset_index()

meninos_freq = meninos.pivot_table(index='year', columns='endswith', values='count')
meninas_freq = meninas.pivot_table(index='year', columns='endswith', values='count')

# grafico dos meninos

meninos_freq.plot()
plt.title('Grafico dos meninos')# para colocar o titulo no grafico
# para colocar a legenda do lado direito do grafico
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

# grafico das meninas
meninas_freq.plot()
plt.title('Grafico das meninas')# para colocar o titulo no grafico
# para colocar a legenda do lado direito do grafico
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

# resposta da pergunta
print('Observando o grafico das ultimas letras dos nomes dos meninos percebemos que a hipótese de Wattenberg coincide com a tabela apresentada')
