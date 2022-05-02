# coding: utf-8
import math
import random
import matplotlib.pyplot as plt
import numpy as np

def func_obj(individuo, p01_c, p01_w, p01_p):
  
  p = 0
  u = 0
  fitness = 0
  for alelo, peso, utilidade in zip(individuo, p01_w, p01_p):
    if alelo == 1:
      p += peso
      u += utilidade

  if(p < p01_c):
    fitness = u
  else:
    fitness = u - (u * (p- p01_c) )

  return fitness


def cria_populacao_inicial(npop, pop, tamanho):
	for i in range(npop):
		pop.append([])
		for j in range(tamanho):
			r = random.random()
			if r <= 0.5:
				pop[i].append(0)
			else:
				pop[i].append(1)


def torneio(npop, fit, pop_intermediaria, pop, tamanho, pm):
    pv = 0.9
    while(len(pop_intermediaria) < npop):
        p1 = random.randrange(0,npop)
        p2 = random.randrange(0, npop)
        p3 = random.randrange(0,npop)
        p4 = random.randrange(0, npop)
        while(p1 == p2):
            p2 = random.randrange(0, npop)
        r = random.randrange(0, 1)
        if (fit[p2] < fit[p1]):
            vencedor1 = p1
            if (r < pv):
                vencedor1 = p2
        else:
            vencedor1 = p2
            if (r < pv):
                vencedor1 = p1

        while(p3 == p4):
            p4 = random.randrange(0, npop)
        r = random.randrange(0, 1)
        if (fit[p4] < fit[p3]):
            vencedor2 = p3
            if (r < pv):
                vencedor2 = p4
        else:
            vencedor2 = p4
            if (r < pv):
                vencedor2 = p3
        
        cruzamento(pop, npop ,pop_intermediaria, vencedor1, vencedor2, tamanho, pm)


def cruzamento(pop, npop, pop_intermediaria, vencedor1, vencedor2, tamanho, pm):
    alelo = random.randrange(1,tamanho-1)

    filho1 = pop[vencedor1][alelo:]
    filho1.extend(pop[vencedor2][:alelo])

    filho2 = pop[vencedor2][alelo:]
    filho2.extend(pop[vencedor1][:alelo])

    pop_intermediaria.append(filho1)
    pop_intermediaria.append(filho2)

    mutacao(pop_intermediaria, npop, pm, tamanho)
    

def mutacao(pop_intermediaria, npop, pm, tamanho):
    for i in range(0, len(pop_intermediaria)):
        for j in range(0, tamanho):
            mutacao = random.random()
            if mutacao <= pm:
                if pop_intermediaria[i][j] == 0:
                    pop_intermediaria[i][j] = 1
                else:
                    pop_intermediaria[i][j] = 0


def elitismo(pop, npop, pop_intermediaria, fit, tamanho, thebest):
    fit_max = max(fit)
    thebest.append(fit_max)
    posicao = fit.index(fit_max)
    index = random.randrange(0, npop-1)
    pop_intermediaria[index] = pop[posicao][:]


def programa():
    pop = []
    pop_intermediaria = []
    thebest = []

    npop = 100 #tamanho da população
    nger = 50 #numero de gerações
    
    pc = 1 #probabilidade de cruzamento
    pm = 0.1 #probabilidade de mutação

    arq1 = open("p01_c.txt")
    arq2 = open("p01_p.txt")
    arq3 = open("p01_s.txt")
    arq4 = open("p01_w.txt")
    linhas_arq1 =  arq1.read()
    linhas_arq2 =  arq2.readlines()
    linhas_arq3 =  arq3.readlines()
    linhas_arq4 =  arq4.readlines()

    p01_c = float(linhas_arq1)
    p01_p = []
    p01_s = []
    p01_w = []

    for i in linhas_arq2:
        p01_p.append(float(i))
    
    for i in linhas_arq3:
        p01_s.append(float(i))

    for i in linhas_arq4:
        p01_w.append(float(i))

    tamanho = len(p01_w)
    fit = []
    arq1.close()
    arq2.close()
    arq3.close()
    arq4.close()

    cria_populacao_inicial(npop, pop, tamanho)

    g=0
    while g < nger:
        for i in pop:
            fit.append(func_obj(i, p01_c, p01_w, p01_p))

        torneio(npop, fit, pop_intermediaria, pop, tamanho, pm)
        elitismo(pop, npop, pop_intermediaria, fit, tamanho, thebest)
        pop = pop_intermediaria
        pop_intermediaria = []

        fit = []
        g += 1
        for i in pop:
            print(i)
        print('------------------------------------')

    print(thebest)
    grafico(nger, thebest)


def grafico(nger, thebest):
    x = np.arange(1, nger+1,1)
    plt.plot(x, thebest, 'k--')
    plt.plot(x, thebest, 'go')
    plt.show()

programa()