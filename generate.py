import random

def level_3D(rows, columns, z, density =100):
    grid = []
    for r in range(rows):
        row = []
        for c in range(columns):
            z_dim = []
            for zz in range(z):
                z_dim.append(random.randint(1, 100) <= density)
            row.append(z_dim)
        grid.append(row)
    
    return grid

def level_2D(rows, columns, density =100):
    grid = []
    for r in range(rows):
        row = []
        for c in range(columns):
            row.append(random.randint(1, 100) <= density)
        grid.append(row)
    
    return grid
