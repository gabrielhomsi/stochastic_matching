from itertools import product

import click as click
import gurobipy
import numpy as np


# model from Kong and Schaefer (2016)
def solve(nodes: int, scenarios: int) -> float:
    V = range(nodes)
    W = range(nodes)
    S = range(scenarios)

    c = {}
    d = {}

    for (i, j) in product(V, W):
        c[i, j] = np.random.randint(100)

    for (s, i, j) in product(S, V, W):
        d[s, i, j] = np.random.randint(100)

    p = [1 / scenarios for s in S]

    # build model
    m = gurobipy.Model("kong")
    m.setParam("Threads", 1)

    # create vars
    x = {}  # first-stage match vars
    y = {}  # second-stage match vars

    for (i, j) in product(V, W):
        x[i, j] = m.addVar(vtype=gurobipy.GRB.BINARY, name=f"x({i},{j})")

    for (s, i, j) in product(S, V, W):
        y[s, i, j] = m.addVar(vtype=gurobipy.GRB.BINARY, name=f"y({s},{i},{j})")

    # create obj
    objX = sum(c[i, j] * x[i, j] for (i, j) in product(V, W))
    objY = sum(p[s] * d[s, i, j] * y[s, i, j] for (s, i, j) in product(S, V, W))

    m.setObjective(objX + objY, gurobipy.GRB.MAXIMIZE)

    # create cons
    for (s, i) in product(S, V):
        m.addConstr(sum([x[i, j] + y[s, i, j] for j in W]) <= 1)

    for (s, j) in product(S, W):
        m.addConstr(sum([x[i, j] + y[s, i, j] for i in V]) <= 1)

    m.optimize()

    return m.objVal


@click.command()
@click.option('--nodes', default=20)
@click.option('--scenarios', default=10)
@click.option('--seed', default=1)
def main(nodes: int, scenarios: int, seed: int):
    np.random.seed(seed)

    solve(nodes, scenarios)


if __name__ == '__main__':
    main()
