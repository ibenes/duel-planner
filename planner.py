#!/usr/bin/python3
import random
import argparse

hard_prefix = [
    (["Karel", "Lukas", "Martin", "Tomas"], "Ctyrka"),
    ]

hard_suffix = [
    (["Karel", "Lukas"], "Pochodne"),
    ]

all_duels = [
    (["Karel", "Lukas"], "Kopi"),
    (["Karel", "Lukas"], "Kordy"),
    (["Martin", "Karel"], "Stitky"),
    (["Martin", "Karel"], "Zapas"),
    (["Tomas", "Karel"], "Jedenapulky"),
    (["Tomas", "Lukas"], "Noze"),
    (["Tomas", "Lukas"], "Zapas"),
    (["Martin", "Lukas"], "Hole"),
    (["Martin", "Lukas"], "Stistky"),
    (["Martin", "Lukas"], "Zapas"),
    (["Martin", "Tomas"], "Sekery"),
    (["Martin", "Tomas"], "Tesaky"),
    ]

def genes2fenes(genotype):
    duels_left = list(all_duels)

    duels = list(hard_prefix)
    for i in genotype:
        duels.append(duels_left.pop(i))

    duels += hard_suffix

    return duels

def print_solution(sol):
    duels = genes2fenes(sol)
    for duel in duels:
        print(duel)

def seq_cost(seq_len):
    return seq_len ** 2 - 1

def fitness(sol):
    cost = 0
    seqs = {}

    duels = genes2fenes(sol)

    for duel in duels:
        for fighter in seqs:
            if fighter in duel[0]:
                seqs[fighter] += 1
            else:
                cost += seq_cost(seqs[fighter])
                seqs[fighter] = 0

        for fighter in duel[0]:
            if fighter not in seqs:
                seqs[fighter] = 1

    for fighter in seqs:
        cost += seq_cost(seqs[fighter])

    return -cost

def random_sol(n_duels):
    sol = []
    for ii in range(n_duels):
        sol.append(random.randint(0,n_duels-ii-1))
    return sol 

def crossover(a, b):
    if (len(a) != len(b)):
        raise ValueError("Can only crossover genomes of equal length")

    co_point = random.randint(1,len(a)-2)
    child_1 = a[:co_point] + b[co_point:]
    child_2 = b[:co_point] + a[co_point:]

    return child_1, child_2

def run_experiment():
    population_size = args.pop_size

    # generate initial population
    population = []
    for i in range(population_size):
        population.append(random_sol(len(all_duels)))

    nb_epochs = args.nb_epochs
    nb_mutations = args.nb_mutations
    selection_threshold = args.selection_thres
    always_kill = args.always_kill
    for epoch_n in range(nb_epochs):
        population.sort(key=fitness, reverse=True)
        population = population[:population_size]
        avg_fitness = sum([fitness(sol) for sol in population])/len(population)
        if args.verbose > 0:
            print("Average population fitness: " + str(avg_fitness))
    #    print([fitness(sol) for sol in population])
        threshold = avg_fitness * 1.0/selection_threshold
        if always_kill > 0:
            population = population[:-always_kill]
        population = [sol for sol in population 
                          if fitness(sol) >= threshold]
        killed = population_size - len(population)
        if args.verbose > 0:
            print("Epoch nb:" + str(epoch_n) + ", killed: " + str(killed))

        nb_children_needed = population_size - len(population)
        for intercourse in range(population_size): # range((nb_children_needed+1)//2):
            p1 = random.randint(0, len(population)-1)
            p2 = random.randint(0, len(population)-1)
            ch1, ch2 = crossover(population[p1], population[p2])
            population += [ch1, ch2]
        
        for i in range(nb_mutations):
            host = random.randint(0, len(population)-1)
            gene = random.randint(0, len(population[host])-1)
            new_val = random.randint(0, len(population[host])-gene-1)
            population[host][gene] = new_val

        # print([fitness(sol) for sol in population])

    nb_interesting = 3
    population.sort(key=fitness, reverse=True)
    for i in range(nb_interesting):
        print("\n" + "=" * 15 + " Cost: "+ str(-fitness(population[i])))
        print_solution(population[i])


def run_gui():
    print("HAve a gui")
    from gui import Gui
    gui = Gui()
    gui.master.title('Duel planner')
    gui.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pop-size", type=int, default=64)
    parser.add_argument("--nb-epochs", type=int, default=64)
    parser.add_argument("--nb-mutations", type=int, default=8)
    parser.add_argument("--selection-thres", type=float, default=0.75)
    parser.add_argument("--always-kill", type=int, default=8)
    parser.add_argument("--verbose", type=int, default=0)
    parser.add_argument("--gui", action='store_true')
    args = parser.parse_args()

    if args.gui:
        run_gui()

    run_experiment()
