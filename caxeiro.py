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

def torneio(pop, npop, distancia, pop_intermediaria, pm, pc, M_len):
    pv = 0.9
    while(len(pop_intermediaria) < npop):
        p1 = random.randrange(0,npop)
        p2 = random.randrange(0, npop)
        p3 = random.randrange(0,npop)
        p4 = random.randrange(0, npop)
        while(p1 == p2):
            p2 = random.randrange(0, npop)
        r = random.randrange(0, 1)
        if (distancia[p2] > distancia[p1]):
            vencedor1 = p1
            if (r > pv):
                vencedor1 = p2
        else:
            vencedor1 = p2
            if (r > pv):
                vencedor1 = p1

        while(p3 == p4):
            p4 = random.randrange(0, npop)
        r = random.randrange(0, 1)
        if (distancia[p4] > distancia[p3]):
            vencedor2 = p3
            if (r > pv):
                vencedor2 = p4
        else:
            vencedor2 = p4
            if (r > pv):
                vencedor2 = p3
        
        prob_cruzamento = random.random()
        if prob_cruzamento <= pc:
            cruzamento(pop, npop, pop_intermediaria, vencedor1, vencedor2, M_len)
        else:
            pop_intermediaria.append(pop[vencedor1])
            pop_intermediaria.append(pop[vencedor2])
    mutacao(pop_intermediaria, pm, M_len)


def selecao_roleta(pop, npop, distancia, pop_intermediaria, roleta, pm, pc, M_len):
    distancia_aux = []
    roleta = []
    cont = 0
    while(len(pop_intermediaria) < npop):

        for i in distancia:
            distancia_aux.append(1/i)

        sum_distancia = sum(distancia_aux)

        for i in distancia_aux:
            roleta.append(i/sum_distancia)

        sortp1 = random.random()
        sortp2 = random.random()
        # print('Sorte valor p1: {}'.format(sortp1))
        # print('Sorte valor p2: {}'.format(sortp2))

        vencedor1 = 0
        vencedor2 = 0
        somatorio_roleta = 0
        
        for i in roleta:
            if(somatorio_roleta < sortp1):
                somatorio_roleta += i
                vencedor1 = roleta.index(i)
        #print('Vencedor 1: {}'.format(vencedor1))
        
        somatorio_roleta = 0
        for i in roleta:
            if(somatorio_roleta < sortp2):
                somatorio_roleta += i
                vencedor2 = roleta.index(i)
        #print('Vencedor 2: {}'.format(vencedor2))

        # print('Soma: {}'.format(sum(roleta)))

        prob_cruzamento = random.random()
        if prob_cruzamento <= pc:
            cruzamento(pop, npop, pop_intermediaria, vencedor1, vencedor2, M_len)
        else:
            pop_intermediaria.append(pop[vencedor1])
    mutacao(pop_intermediaria, pm, M_len)


def cruzamento(pop, npop, pop_intermediaria, vencedor1, vencedor2, M_len):
    alelo1 = random.randrange(2, M_len-1)
    alelo2 = random.randrange(2, M_len-1)
    filho1 = [-1 for i in range(M_len)]
    filho2 = [-1 for i in range(M_len)]


    while alelo1 > alelo2 or alelo1 == alelo2:
        alelo1 = random.randrange(2, M_len-1)
        alelo2 = random.randrange(2, M_len-1)

    if alelo1 < alelo2:

        filho1[alelo1:alelo2] = pop[vencedor1][alelo1:alelo2]

        tail = pop[vencedor2][alelo2:]
        head = pop[vencedor2][:alelo2]

        tail = tail + head

        i = 0
        j = alelo2
        while i < len(tail):
            if(tail[i] not in filho1):
                filho1[j] = tail[i]
                j += 1
                if j == M_len:
                    j=0
            i += 1

        pop_intermediaria.append(filho1)
        # print("filho 1 eqweqwe: {}".format(filho1))

        filho2[alelo1:alelo2] = pop[vencedor2][alelo1:alelo2]

        tail = pop[vencedor1][alelo2:]
        head = pop[vencedor1][:alelo2]

        tail = tail + head

        i = 0
        j = alelo2
        while i < len(tail):
            if(tail[i] not in filho2):
                filho2[j] = tail[i]
                j += 1
                if j == M_len:
                    j=0
            i += 1

        # print("filho 2 eqweqwe: {}".format(filho2))
        pop_intermediaria.append(filho2)

    if alelo1 > alelo2:

        filho1[alelo2:alelo1] = pop[vencedor1][alelo2:alelo1]

        tail = pop[vencedor2][alelo1:]
        head = pop[vencedor2][:alelo1]

        tail = tail + head

        i = 0
        j = alelo1
        while i < len(tail):
            if(tail[i] not in filho1):
                filho1[j] = tail[i]
                j += 1
                if j == M_len:
                    j=0
            i += 1

        pop_intermediaria.append(filho1)
        # print("filho 1 eqweqwe: {}".format(filho1))

        filho2[alelo2:alelo1] = pop[vencedor2][alelo2:alelo1]

        tail = pop[vencedor1][alelo1:]
        head = pop[vencedor1][:alelo1]

        tail = tail + head

        i = 0
        j = alelo1
        while i < len(tail):
            if(tail[i] not in filho2):
                filho2[j] = tail[i]
                j += 1
                if j == M_len:
                    j=0
            i += 1

        # print("filho 2 eqweqwe: {}".format(filho2))
        pop_intermediaria.append(filho2)


def mutacao(pop_intermediaria, pm, M_len):
    for i in range(0, len(pop_intermediaria)):
        for j in range(0, M_len):
            mutacao = random.random()
            if mutacao <= pm:
                muta = random.randrange(0, M_len)
                aux = pop_intermediaria[i][j]
                pop_intermediaria[i][j] = pop_intermediaria[i][muta]
                pop_intermediaria[i][muta] = aux


def elitismo(pop, npop, pop_intermediaria, distancia, thebest, index):
    distancia_min = min(distancia)
    thebest.append(distancia_min)
    posicao = distancia.index(distancia_min)
    pop_intermediaria[index] = pop[posicao][:]

    return distancia_min


def programa(npop, nger, pc, iteracao, w, pm):
    pop = []
    pop_intermediaria = []
    thebest = []
    distancia = []
    roleta = []

    index = random.randrange(0, npop-1)

    M_dist = np.loadtxt("./lau15_dist.txt", dtype="int")
    M_len = len(M_dist)

    i = 0
    while i < npop:
        aux = list(range(0, M_len))
        random.shuffle(aux)
        pop.append(aux)
        i += 1

    g=0
    while g < nger:
        for ind in pop:
            distancia.append(func_obj(M_len, ind, M_dist))

        torneio(pop, npop, distancia, pop_intermediaria, pm, pc, M_len)
        # selecao_roleta(pop, npop, distancia, pop_intermediaria, roleta, pm, pc, M_len)
        distancia_min = elitismo(pop, npop, pop_intermediaria, distancia, thebest, index)

        w.writerow([iteracao, npop, nger, pc, pm, pop_intermediaria[index], distancia_min])

        pop = pop_intermediaria[:]
        pop_intermediaria = []    
        distancia = []
        g += 1
        # for i in pop:
        #    print(i)
        # print('------------------------------------')

    # print(distancia_min)
    # grafico(nger, distancia_min)


def start():
    npop = 50
    nger = 50
    pc = 0.6
    pm = 0.01

    iteracao = 0
    file = open('datas.csv', 'a', newline='')
    
    w = csv.writer(file)

    if Path('datas.csv').stat().st_size == 0:
        w.writerow(["Iteracao", "Populacao", "NumGeracoes", "TaxaDeCruzamento", "ProbMutacao", "Individuo", "Valordistancia"])

    for i in range(10):
        programa(npop, nger, pc, iteracao, w, pm)
        iteracao += 1


def grafico(nger, thebest):
    x = np.arange(1, nger+1,1)
    plt.plot(x, thebest, 'k--')
    plt.plot(x, thebest, 'go')
    plt.show()

start()