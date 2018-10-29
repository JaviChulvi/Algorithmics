def planificar( d: "List<int>", n: "int") -> "List<int>":
    paradas = [0]
    km = n
    for (i, dist) in enumerate(d):
        if dist >= km:
            paradas.append(i)
            km = n
        km -= dist
    if paradas[-1] != len(d):
        paradas.append(len(d))
    return paradas

if __name__ == "__main__":
    print(planificar([20, 10, 40, 20, 10], 50))
