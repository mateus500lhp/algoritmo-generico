# coding: utf-8
import math
import random
from random import randrange, uniform
import matplotlib.pyplot as plt
import numpy as np

def func_obj(x):

	n = float(len(x))

	t = 0
	for i in range(0, len(x)):
		t += x[i]*x[i]

	f_exp = -0.2 * math.sqrt((1*t)/n)

	t = 0
	for i in range(0, len(x)):
		t += math.cos(2 * math.pi * x[i])

	s_exp = 1/n * t
	f = -20 * math.exp(f_exp) - math.exp(s_exp) + 20 + math.exp(1)
    
	return f


def avaliacao(pop):
	fit.append(func_obj(pop))


def cria_populacao_inicial(npop, pop, dimensao, precisao):
	for i in range(npop):
		pop.append([])
		for j in range(dimensao*precisao):
			r = uniform(-2, 2)
			pop[i].append(r)


def torneio(npop, fit):
    pv = 0.9
    while(len(pop_intermediaria) < npop):
        p1 = random.randrange(0,npop)
        p2 = random.randrange(0, npop)
        p3 = random.randrange(0,npop)
        p4 = random.randrange(0, npop)
        while(p1 == p2):
            p2 = random.randrange(0, npop)
        r = random.randrange(0, 1)
        if (fit[p2] > fit[p1]):
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
        if (fit[p4] > fit[p3]):
            vencedor2 = p3
            if (r > pv):
                vencedor2 = p4
        else:
            vencedor2 = p4
            if (r > pv):
                vencedor2 = p3
        
        cruzamento(pop, npop ,pop_intermediaria, vencedor1, vencedor2, dimensao, precisao)


def selecao_roleta(pop, npop, fit, pop_intermediaria, roleta):
    fitaux = []
    roleta = []
    cont = 0
    while(len(pop_intermediaria) < npop):
        pop_intermediaria.append([])
        for i in fit:
            fitaux.append(1/i)

        sumfit = sum(fitaux)

        for i in fitaux:
            roleta.append(i/sumfit)

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

        # print(vencedor1)
        # print(vencedor2)
        #print('Soma: {}'.format(sum(roleta)))

        cruzamento(cont, pop, npop, pop_intermediaria, vencedor1, vencedor2, dimensao, precisao)
        cont += 1

def cruzamento(cont, pop, npop, pop_intermediaria, vencedor1, vencedor2, dimensao, precisao):
    for i in range(dimensao):
        print(vencedor1, cont)
        d = abs(pop[vencedor1][i] - pop[vencedor2][i])
        
        f1 = uniform(min(pop[vencedor1][i], pop[vencedor2][i]) - alfa * d, max(pop[vencedor1][i], pop[vencedor2][i]) + alfa * d)
        pop_intermediaria[cont].append(f1)

    #mutacao(pop_intermediaria, npop, pm, dimensao, precisao)
    

def mutacao(pop_intermediaria, npop, pm, dimensao, precisao):
    for i in range(0, len(pop_intermediaria)):
        for j in range(0, precisao*dimensao-1):
            mutacao = random.random()
            if mutacao <= pm:
                pop_intermediaria[i][j] == uniform(-2, 2):



def elitismo(pop, npop, pop_intermediaria, fit, dimensao, precisao):
    fit_min = min(fit)
    thebest.append(fit_min)(somatorio_roleta < sortp2):
                somatorio_roleta += i
                vencedor2 = roleta.index(i)icao][:]


x_min = -2
x_max = 2
dimensao = 3
precisao = 1

npop = 50 #tamanho da população
nger = 4 #numero de gerações
nelite = 2
pop = []
pop_intermediaria = []

fit = []
thebest = []
roleta = []

pc = 1 #probabilidade de cruzamento
pm = 0.1 #probabilidade de mutação
alfa = 0.5
cria_populacao_inicial(npop, pop, dimensao, precisao)

for i in pop:
    print(i)

for i in pop:
    avaliacao(i)

print('-----------------------------------------------------------------')

for i in fit:
    print(i)

print('-----------------------------------------------------------------')

selecao_roleta(pop, npop, fit, pop_intermediaria, roleta)

for i in pop_intermediaria:
    print(i)



# g=0
# while g < nger:
#     for i in pop:
#         avaliacao(i)
#    # torneio(npop, fit)
#     selecao_roleta(pop, npop, fit, pop_intermediaria, roleta)
#     elitismo(pop, npop, pop_intermediaria, fit, dimensao, precisao)
#     pop = pop_intermediaria
#     pop_intermediaria = []
#     fit = []
#     g += 1
#     for i in pop:
#         print(i)
#     print('------------------------------------')

# x = np.arange(1, nger+1,1)
# plt.plot(x, thebest, 'k--')
# plt.plot(x, thebest, 'go')
# plt.show()