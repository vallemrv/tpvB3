lista = [{"can": 20, "tipo": 50}, {"can": 10, "tipo": 10},
         {"can": 20, "tipo": 50}]


print lista
src = sorted(lista, key=lambda k: k["tipo"])
for sr in src:
    print sr
