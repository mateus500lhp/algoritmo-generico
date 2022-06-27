# coding: utf-8
import math
import random
import matplotlib.pyplot as plt
import numpy as np
import csv
from pathlib import Path
import time

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
    mutacao(npop, pm, M_len, pop_intermediaria)

def selecaoRoleta(populacao, individuo_fit, pop_intermediaria, tamanho_populacao,
                  taxa_cruzamento,num_city, pm):
    aux_fitness = []
    roleta = []

    for ind in individuo_fit:
        aux_fitness.append(1 / ind)

    pfitness = sum(aux_fitness)

    for ind in aux_fitness:
        roleta.append(ind / pfitness)

    while (len(pop_intermediaria) < tamanho_populacao):

        auxroleta = 0
        pai1 = 0
        pai2 = 0
        sort1 = random.uniform(0,pfitness)
        sort2 = random.uniform(0,pfitness)

        for i in roleta:
            if auxroleta < sort1:
                auxroleta += i
                pai1 = roleta.index(i)

        auxroleta = 0

        for i in roleta:
            if auxroleta < sort2:
                auxroleta += i
                pai2 = roleta.index(i)

        if (pai1 != pai2):
            prob_sort = random.random()
            if (taxa_cruzamento >= prob_sort):
                # cruzamento(pop, npop, pop_intermediaria, vencedor1, vencedor2, M_len)
                cruzamento(populacao, tamanho_populacao, pop_intermediaria, pai1, pai2, num_city)
    mutacao(tamanho_populacao, pm, num_city, pop_intermediaria)


def selecao_roleta(pop, npop, distancia, pop_intermediaria, roleta, pm, pc, M_len):
    distancia_aux = []
    roleta = []
    cont = 0
    for i in distancia:
        distancia_aux.append(1/i)

    sum_distancia = sum(distancia_aux)

    for i in distancia_aux:
        roleta.append(i/sum_distancia)
    while(len(pop_intermediaria) < npop):



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
    mutacao(npop, pm, M_len, pop_intermediaria)


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

def mutacao(tamanho_populacao, taxa_mutacao, num_city, populacao_intermediaria):
    # para realizar a mutacao precisamos percorrer por toda a populacao_intermediaria
    for i in range(tamanho_populacao):
        mutacao = random.random()
        # sorteio uma taxa de mutação
        if mutacao <= taxa_mutacao:  # sematriz_distancia minha taxa for igual ou menor que minha taxa de mutação
            mutacao1 = random.randrange(0, num_city)
            for j in range(mutacao1):
                troca1 = random.randrange(0, num_city)
                troca2 = random.randrange(0, num_city)

                while troca1 == troca2:
                    troca1 = random.randrange(0, num_city)
                    troca2 = random.randrange(0, num_city)

                if troca1 != troca2:
                    aux = populacao_intermediaria[i][troca1]
                    populacao_intermediaria[i][troca1] = populacao_intermediaria[i][troca2]
                    populacao_intermediaria[i][troca2] = aux

def elitismo(pop, npop, pop_intermediaria, distancia, thebest, index):
    distancia_min = min(distancia)
    thebest.append(distancia_min)
    posicao = distancia.index(distancia_min)
    pop_intermediaria[index] = pop[posicao][:]

    return distancia_min


def programa(npop, nger, pc, iteracao, w, pm, w2):
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

    pop_torneio = pop
    pop_roleta = pop_torneio
    
    pop_intermediaria_torneio = pop_intermediaria
    pop_intermediaria_roleta = pop_intermediaria_torneio

    g = 0
    while g < nger:
        for ind in pop_roleta:
            distancia.append(func_obj(M_len, ind, M_dist))

        # torneio(pop, npop, distancia, pop_intermediaria, pm, pc, M_len)
        tempo_inicial_r = time.time()
        # selecaoRoleta(pop_roleta, distancia, pop_intermediaria_roleta, npop,pc,M_len, pm)
        tempo_final_r = (time.time() - tempo_inicial_r)
        selecao_roleta(pop_roleta, npop, distancia, pop_intermediaria_roleta, roleta, pm, pc, M_len)
        tempo_final_r = (time.time() - tempo_inicial_r)
        distancia_min = elitismo(pop_roleta, npop, pop_intermediaria_roleta, distancia, thebest, index)

        w.writerow([iteracao,'Roleta', npop, nger, pc, pm, pop_intermediaria_roleta[index], distancia_min, tempo_final_r])

        pop_roleta = pop_intermediaria_roleta[:]
        pop_intermediaria_roleta = []    
        distancia = []
        g += 1

    z = 0
    while z < nger:
        for ind in pop_torneio:
            distancia.append(func_obj(M_len, ind, M_dist))

        tempo_inicial_t = time.time()
        torneio(pop_torneio, npop, distancia, pop_intermediaria_torneio, pm, pc, M_len)
        tempo_final_t = (time.time() - tempo_inicial_t)
        distancia_min = elitismo(pop_torneio, npop, pop_intermediaria_torneio, distancia, thebest, index)

        w2.writerow([iteracao,'Torneio', npop, nger, pc, pm, pop_intermediaria_torneio[index], distancia_min, tempo_final_t])

        pop_torneio = pop_intermediaria_torneio[:]
        pop_intermediaria_torneio = []    
        distancia = []
        z += 1


def start():
    npop = 25
    nger = 25
    pc = 0.6
    pm = 0.01


    iteracao = 0
    file = open('datas3.csv', 'a', newline='')
    file2 = open('datas4.csv', 'a', newline='')
    
    w = csv.writer(file)
    w2 = csv.writer(file2)

    if Path('datas.csv').stat().st_size == 0:
        w.writerow(["Iteracao", "TipoSelecao", "Populacao", "NumGeracoes", "TaxaDeCruzamento", "ProbMutacao", "Individuo", "Valordistancia", "TempoFinal"])

    for i in range(10):
        programa(npop, nger, pc, iteracao, w, pm, w2)
        iteracao += 1

start()