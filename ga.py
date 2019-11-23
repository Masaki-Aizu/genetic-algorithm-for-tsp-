# coding:utf-8

import pandas as pd
import random as rnd
import math

    
def generate_route(x, population):

    position = {}
    for i in range(len(x)):
        position[i] = x[i]

    select_num = [i for i in range(len(x))]
    routes = [rnd.sample(select_num, len(x)) for _ in range(population)]

    return position, routes


def evaluate(position, routes, loop=0):

    evaluate_value = []
    for i in range(len(routes)):
        temp_distances = 0
        list_x = [position[routes[i][x]][0] for x in range(len(position))]
        list_y = [position[routes[i][y]][1] for y in range(len(position))]

        for j in range(len(position)):
            if j == len(position) - 1:
                distance = math.sqrt(pow((list_x[j] - list_x[0]), 2) 
                                       + pow((list_y[j] - list_y[0]), 2))
            else:
                distance = math.sqrt(pow((list_x[j] - list_x[j + 1]), 2) 
                                       + pow((list_y[j] - list_y[j + 1]), 2))

            temp_distances += distance

        evaluate_value.append(temp_distances)

    # print(evaluate_value)

    best_value = min(evaluate_value)
    
    print('最優秀固体 %d世代目 : %f' %(loop + 1, best_value) )
    
    return evaluate_value

def tournament_selection(routes, evaluate_value, tournament_num, tournament_size):

    select_pop = []
    elite = []

    while len(select_pop) <= len(routes) / 2:
        select = rnd.sample(evaluate_value, tournament_size)
        select.sort()

        for i in range(tournament_num):
            value = select[i]
            index = evaluate_value.index(value)
            select_pop.append(routes[index])

    return select_pop

def crossover(select_pop, cross_pro):

    tmp = rnd.sample(select_pop, 2)
    ind_1 = tmp[0]
    ind_2 = tmp[1]

    if rnd.randint(0, 100) <= cross_pro:

        new_ind_1 = []
        cut = rnd.randint(1, len(ind_1) - 2)
        new_ind_1.extend(ind_1[:cut])
        for i in range(len(ind_1)):
           if ind_2[i] not in new_ind_1:
               new_ind_1.append(ind_2[i])

        new_ind_2 = []
        new_ind_2.extend(ind_1[cut:])
        for i in range(len(ind_2)):
           if ind_2[i] not in new_ind_2:
               new_ind_2.append(ind_2[i])

        return new_ind_1, new_ind_2
    else:
        return ind_1, ind_2

def mutation(ind, mutation_pro):

    if rnd.randint(0, 100) <= mutation_pro:
        select_num = [i for i in range(len(ind))]
        select_index = rnd.sample(select_num, 2)

        a = ind[select_index[0]]
        b = ind[select_index[1]]
        ind[select_index[1]] = a
        ind[select_index[0]] = b

    return ind

population = 200  # 個体数
generation_num = 200  # 世代数

tournament_size = 10  # トーナメント選択のパラメータ
tournament_num = 2

cross_pro = 50  # 交叉の確率

mutation_pro = 3  # 突然変異の確率

# データ読み込み: 座標(x, y)
X = pd.read_table("sample.txt", sep = "\t")
x = X.values

# create initial solutions
position, routes = generate_route(x, population)
# print(position, routes)

# evaluate initial solutions
evaluate_value = evaluate(position, routes)

for loop in range(generation_num - 1):
    # tournament selection
    select_pop = tournament_selection(routes, evaluate_value, tournament_num,  tournament_size)

    next_routes = []
    while len(next_routes) <= population:
        # crossover
        ind_1, ind_2 = crossover(select_pop, cross_pro)

        # mutation
        ind_1 = mutation(ind_1, mutation_pro)
        ind_2 = mutation(ind_2, mutation_pro)
        next_routes.append(ind_1)
        next_routes.append(ind_2)
    
    # update
    routes = next_routes
    evaluate_value = evaluate(position, next_routes, loop + 1)

    