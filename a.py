# coding: utf-8
import math
import random
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

def reseta_formigas(formigas, M_len):
    for i in range(M_len):
        for j in range(M_len):
            if j != 0:
                formigas[i][j] = -1 

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

def atualiza_feromonio(M_fer, formigas, M_dist, dist_formiga):
    p = 0.5
    q = 100

    for i in range(len(formigas)):
        somatorio = 0
        for j in range(len(formigas) - 1):
            somatorio += M_dist[formigas[i][j]][formigas[i][j + 1]]
            if j == len(formigas) - 2:
                j = len(formigas) - 1
                somatorio += M_dist[formigas[i][j]][formigas[i][0]]
        dist_formiga.append(somatorio)
    somatorio = 0

    for i in range(len(formigas)):
        for j in range(len(formigas) - 1):
            M_fer[i][j] = M_fer[i][j] * p

    for i in range(len(formigas)):
        for j in range(len(formigas) - 1):
            somatorio = 100/dist_formiga[i] + M_fer[formigas[i][j]][formigas[i][j + 1]]
            M_fer[formigas[i][j]][formigas[i][j + 1]] = somatorio


def programa(nger, iteracao, w):
    formigas = []
    distancia = []
    dist_formiga = []
    roleta = []
    alpha = 4
    beta = 1

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

    g=0
    while g < nger:
        for f in formigas:
            probabilidade(f, M_len, M_fer, M_dist_inversa, alpha, beta)

        atualiza_feromonio(M_fer, formigas, M_dist, dist_formiga)
        w.writerow([iteracao, nger, alpha, beta, min(dist_formiga)]) 
        reseta_formigas(formigas, M_len)
        g += 1

def start():
    nger = 100
    iteracao = 0

    file = open('data.csv', 'a', newline='')
    
    w = csv.writer(file)

    if Path('data.csv').stat().st_size == 0:
        w.writerow(["iteracao", "nger", "alpha", "beta", "dist_formiga"])

    for i in range(10):
        programa(nger, iteracao, w)
        iteracao += 1


start()