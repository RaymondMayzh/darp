from solver.darp import Darp

BIG = -1
TOTAL_HORIZON=1000

def main_darp():

    """
        route = [1, 2 , 1*, 2*]
    route ids   = [1, 2 , 3 , 4 ]

        arr.:              150         175          475          500
    route: [0]---150--->[1]---25--->[2]---400--->[1*]---25--->[2*]
        tw:           [0  ,180)   [20 ,200)    [300,600)    [320,620)
    e. arr.:              150         100          450          400

    """
    
    dist_matrix = {
        "0":  {"0": BIG, "1": 150, "2": 100, "1*": BIG, "2*": BIG, "0*": 0},
        "1":  {"0": BIG, "1": BIG, "2": 25,  "1*": 150, "2*": 100, "0*": BIG},
        "2":  {"0": BIG, "1": 150, "2": BIG, "1*": 400, "2*": 300, "0*": BIG},
        "1*": {"0": BIG, "1": 300, "2": 100, "1*": BIG, "2*": 25,  "0*": 0},
        "2*": {"0": BIG, "1": 150, "2": 100, "1*": 150, "2*": BIG, "0*": 0},
        "0*": {"0": BIG, "1": BIG, "2": BIG, "1*": BIG, "2*": BIG, "0*": BIG},
        # "1": {"1": 0, "1*": 300, "2": 25},
        # "2": {"2": 0, "1*": 400, "2*": 300},
        # "2*": {"2*": 0, "1*": 300, "2*": 300},
        # "1*": {"2": 300, "2*": 25},
    }

    import networkx as nx
    import matplotlib.pyplot as plt
    G = nx.DiGraph()
    
    options = {
    "font_size": 36,
    "node_size": 3000,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 5,
    "width": 5,
}
    
    G.add_weighted_edges_from(
        (o,d,1)
        for o in dist_matrix
        for d in dist_matrix[o]
        if dist_matrix[o][d] != BIG
    )
    print("Drawing graph")
    print(G)
    fig, ax = plt.subplots()
    nx.draw_networkx(G, arrows=True, ax=ax, **options)
    plt.show()
    
    
    model = Darp(
        N=["0", "1", "2", "1*", "2*", "0*"],
        #N=["0", "1", "1*", "0*"],
        P=["1", "2"],
        D=["1*", "2*"],
        #P=["1"],
        #D=["1*"],
        # Example 1: Vehicle 1 pools requests 1 and 2
        K=["V1"],
        Q={"V1": 6},
        
        # Example 2: Vehicles 1 and 2 (of smaller capacity) have to be used to pickup 1 and 2
        #K=["V1", "V2"],
        #Q={"V1": 4, "V2": 4},
        L={"1": 600, "2": 600},
        el={
            "0": (0, TOTAL_HORIZON),
            "1": (0, 180),
            "2": (20, 200),
            "1*": (150, 600), # earliest at 1 (0) + travel time 1 -> 1* (150) 
            "2*": (320, 620),
            "0*": (0, TOTAL_HORIZON),
        },
        d={
            "0": 0,
            "1": 0,
            "2": 0,
            "1*": 0,
            "2*": 0,
            "0*": 0,
        },
        q={
            "0": 0,
            "1": 4,
            "2": 2,
            "1*": -4,
            "2*": -2,
            "0*": 0,
        },
        dist_matrix=dist_matrix,
    )

    model.stats()
    # model = Darp(N=[0,1,2,3,4], P=[1,2], D=[3,4], K=1, Q=1, L=600, el=[(0, math.inf), (0, 180), (20, 200), (300, 600), (320, 620)], dist_matrix=)

if __name__ == "__main__":
    main_darp()