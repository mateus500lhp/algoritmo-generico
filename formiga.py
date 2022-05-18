# coding: utf-8
import math
import random
import matplotlib.pyplot as plt
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
    cont = 0
    for i in range(M_len):
        formigas.append([])
        for j in range(M_len):
            if j == cont:
                formigas[i].append(1)
            else:
                formigas[i].append(0)
        cont += 1
        

def programa(npop, nger, pc, iteracao, pm):
    formigas = []
    pop_intermediaria = []
    thebest = []
    distancia = []
    roleta = []

    index = random.randrange(0, npop-1)

    M_dist = np.loadtxt("./lau15_dist.txt", dtype="int")
    M_len = len(M_dist)

    M_fer = [[ pow(10, -16) for i in range(M_len)] for j in range(M_len) ]

    criar_populacao_inicial(formigas, M_len)

    for i in formigas:
        print(i)

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


def grafico(nger, thebest):
    x = np.arange(1, nger+1,1)
    plt.plot(x, thebest, 'k--')
    plt.plot(x, thebest, 'go')
    plt.show()

start()