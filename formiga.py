# coding: utf-8
import math
import random
# import matplotlib.pyplot as plt
import numpy as np
import csv
from pathlib import Path

def func_obj(M_len, permutacao, M_dist):
    distancia = 0
    for c, p in enumerate(permutacao):
        if c < M_len - 1:
            distancia += M_dist[permutacao[c]][permutacao[c+1]]
    distancia += M_dist[permutacao[M_len-1]][permutacao[0]]

    return distancia

def criar_populacao_inicial(formigas, M_len):
    index = random.sample(range(0, M_len), M_len)
    for i in range(M_len):
        formigas.append([])
        for j in range(M_len):
            if j == 0:
                formigas[i].append(index[i])
            else:
                formigas[i].append(-1)


def probabilidade(formiga, M_len, M_fer, M_dist_inversa, alpha, beta):
    z = 1
    while z < M_len :
        p = []
        cidades = []

        for j in range(M_len):
            if j not in formiga:
                cidades.append(j)
                p.append(pow(M_fer[formiga[z-1]][j],alpha) * pow(M_dist_inversa[formiga[z-1]][j], beta))
              
        roleta = [x/sum(p) for x in p]

        
        sort = random.random()
        somatorio_roleta = 0
        aux_roleta = 0
        for r in roleta:
            if(somatorio_roleta < sort):
                somatorio_roleta += r
                aux_roleta = roleta.index(r)

        formiga[z] = cidades[aux_roleta]
        z += 1


#def atualiza_feromonio()

def programa(npop, nger, pc, iteracao, pm):
    formigas = []
    pop_intermediaria = []
    thebest = []
    distancia = []
    roleta = []
    alpha = 1
    beta = 5

    index = random.randrange(0, npop-1)

    M_dist = np.loadtxt("./lau15_dist.txt", dtype="int")
    M_len = len(M_dist)

    M_fer = [[ pow(10, -16) for i in range(M_len)] for j in range(M_len) ]

    M_dist_inversa = []

    for i in range(M_len):
        M_dist_inversa.append([])
        for j in range(M_len):
            if i != j:
                M_dist_inversa[i].append(1/M_dist[i][j])
            else:
                M_dist_inversa[i].append(0)

    criar_populacao_inicial(formigas, M_len)
    for f in formigas:
        print(f)
    for f in formigas:
        probabilidade(f, M_len, M_fer, M_dist_inversa, alpha, beta)

    for f in formigas:
        print(f)

    # i = 0
    # while i < npop:
    #     aux = list(range(0, M_len))
    #     random.shuffle(aux)
    #     pop.append(aux)
    #     i += 1


    # g=0
    # while g < nger:
    #     for ind in pop:
    #         distancia.append(func_obj(M_len, ind, M_dist))

    #     # selecao_roleta(pop, npop, distancia, pop_intermediaria, roleta, pm, pc, M_len)
    #     torneio(npop, distancia, pop_intermediaria, pop, pm, pc, M_len)
    #     distancia_min = elitismo(pop, npop, pop_intermediaria, distancia, thebest, index)

    #     w.writerow([iteracao, npop, nger, pc, pm, pop_intermediaria[index], distancia_min])

    #     pop = pop_intermediaria[:]
    #     pop_intermediaria = []    
    #     distancia = []
    #     g += 1
        # for i in pop:
        #    print(i)
        # print('------------------------------------')

    # print(distancia_min)
    # grafico(nger, distancia_min)


def start():
    npop = 100
    nger = 100
    pc = 1.0
    pm = 0.1

    iteracao = 0

    programa(npop, nger, pc, iteracao, pm)
    # file = open('datas2.csv', 'w', newline='')
    
    # w = csv.writer(file)

    # if Path('datas2.csv').stat().st_size == 0:
    #     w.writerow(["Iteracao", "Populacao", "NumGeracoes", "TaxaDeCruzamento", "ProbMutacao", "Individuo", "Valordistancia"])

    # for i in range(10):
    #     programa(npop, nger, pc, iteracao, w, pm)
    #     iteracao += 1


# def grafico(nger, thebest):
#     x = np.arange(1, nger+1,1)
#     plt.plot(x, thebest, 'k--')
#     plt.plot(x, thebest, 'go')
#     plt.show()

start()