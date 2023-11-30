import numpy as np
import matplotlib.pyplot as plt
import argparse
import time

# Création d'un analyseur d'arguments
parser = argparse.ArgumentParser(description='diffusion de la chaleur ponderer avec des pourcentages.')

# Ajout d'arguments
parser.add_argument('--caseValue', type=int, help='Affiche dans chaque case de la map (0) la temperature - (1) les pourcentages - (-1) rien')
parser.add_argument('--demo', type=int, help='proposition de demo (0) ')
parser.add_argument('--iterations', type=int, help='choisissez le nombre d\'iteration maximale a effectue')

# Analyse des arguments de ligne de commande
args = parser.parse_args()

printNumbers = -1

# Nombre d'itérations de simulation
iterations = 100

# Taille de la grille
n_rows, n_cols = 50, 50

# Créez la grille et initialisez les températures initiales
grid = np.zeros((n_rows, n_cols))

#zones infinies
material_grid = np.ones(grid.shape)

# ici la moitie superieur est beaucoup moins sensible a la propagation de chaleur
grid[4, :50] = 100     # Zone chaude
material_grid[4, :50] = 0     # Zone chaude
material_grid[:4,:] = 0.1 # la partie superieur de la map est moins affecte par la diffusion de chaleur

# Utilisation des arguments
if args.caseValue is not None:
    print("caseValue :", args.caseValue)
    if -2 < args.caseValue and args.caseValue < 2:
        printNumbers = args.caseValue
    else :
        print("valeur non valide")


if args.demo is not None:
    print("demo :", args.demo)
    if args.demo == 0:
        # Taille de la grille
        n_rows, n_cols = 5, 5

        # Créez la grille et initialisez les températures initiales
        grid = np.zeros((n_rows, n_cols))

        # zones infinies
        material_grid = np.ones(grid.shape)

        # ici la moitie superieur est beaucoup moins sensible a la propagation de chaleur
        grid[0, :] = 100  # Zone chaude
        grid[-1, :] = -50  # Zone froide
        material_grid[:, :1] = 1  # colonne chaude facile
        material_grid[:, -2:] = 1  # colonne froide facile
        material_grid[0, :] = 0  # Zone chaude static
        material_grid[-1, :] = 0  # Zone froide static
        material_grid[1:-1, 2:-2] = 1  # No temperatures land
    elif args.demo == 1:
        # Taille de la grille
        n_rows, n_cols = 10, 10

        # Créez la grille et initialisez les températures initiales
        grid = np.zeros((n_rows, n_cols))

        # zones infinies
        material_grid = np.ones(grid.shape)

        # ici la moitie superieur est beaucoup moins sensible a la propagation de chaleur
        grid[:, :] = 100  # Zone chaude
        grid[1:-1, 1:-1] = 0  # Zone neutre
        grid[7:8, 7:8] = -100  # Zone froide
        material_grid[:, :] = 0  # Zone chaude static
        material_grid[:-1, 1:-1] = 1  # Zone froide static
    elif args.demo == 2:
        # Taille de la grille
        n_rows, n_cols = 25, 25

        # Créez la grille et initialisez les températures initiales
        grid = np.zeros((n_rows, n_cols))
        material_grid = np.ones(grid.shape)

        grid[12, :12] = 100  # Zone chaude

    elif args.demo == 3:
        # Taille de la grille
        n_rows, n_cols = 50, 50

        # Créez la grille et initialisez les températures initiales
        grid = np.zeros((n_rows, n_cols))
        material_grid = np.ones(grid.shape)

        grid[:, 24:26] = 100  # Zone chaude
        material_grid[:, 24:26] = 0

        grid[:25, -2:] = -100  # Zone chaude
        material_grid[:25, -2:] = 0

        grid[25:, :1] = -50
        material_grid[25:, :1] = 0

    elif args.demo == 4:
        # Taille de la grille
        n_rows, n_cols = 100, 100

        # Créez la grille et initialisez les températures initiales
        grid = np.zeros((n_rows, n_cols))
        material_grid = np.ones(grid.shape)

        grid[0, :75] = -100  # Zone chaude
        material_grid[0, :75] = 0

        grid[25, 25:] = 100  # Zone chaude
        material_grid[25, 25:] = 0.5

        grid[49:51, 50:] = 50  # Zone chaude
        grid[49:51, :50] = -50  # Zone froide

        grid[75, :75] = -100  # Zone chaude
        material_grid[75, :75] = 0.5

        grid[-1, 25:] = 100  # Zone chaude
        material_grid[-1, 25:] = 0

if args.iterations is not None and not np.nan(args.iterations):
        iterations = args.iterations
        

# ici on peut voir que comme les cases froide sont dans un materiau plus sensible a la diffusion de chaleur, leur changement de temperature sera plus marqué que les cases chaude qui sont dans un materiaux moins sensible a la diffusion de chaleur
# grid[:, :1] = 100     # Zone chaude
# grid[:, -1] = -100    # Zone froide
# material_grid[:,0] = 0.1
# material_grid[:,-1] = 0.5

new_grid = np.copy(grid)


# Matrice de propagation pour tout les matériau
propagation_matrix = np.array([[1/36, 4/36, 1/36],  # faible propagation
                               [4/36, 16/36, 4/36],
                               [1/36, 4/36, 1/36]])
propagation_size = propagation_matrix.shape[0]
            
def update_value(i, j, value):
    if np.isnan(value):
        return
    percent = material_grid[i,j]
    current = grid[i,j]
    new_grid[i,j] += (value-current)*percent
    
def heat_simulation_on(i, j):
    neighborhood = grid[max(0, i - 1):min(n_rows, i + 2), max(0, j - 1):min(n_cols, j + 2)] # neighborhood de taille variable : min (2,2) et max (3,3)
    if (neighborhood.shape == (3, 3)):  # si non près d'un bord
        
        update_value(i,j,np.sum(neighborhood * propagation_matrix))
    else:
        # thisPropagationMatrix match la forme de neighborhood avec le centre de cette matrice à l'emplacement des coordonnées i,j dans la matrice neighborhood

        start_row = max(0, i - (propagation_size // 2))
        start_col = max(0, j - (propagation_size // 2))

        thisPropagationMatrix = np.zeros(neighborhood.shape)
        center_i, center_j = neighborhood.shape[0] // 2, neighborhood.shape[1] // 2
        
        # attribution des coefficients à la matrice :
        for k in range(neighborhood.shape[0]):
            for l in range(neighborhood.shape[1]):
                thisPropagationMatrix[i - start_row - 1 + k, j - start_col - 1 + l] = 1 / (thisPropagationMatrix.shape[0] * thisPropagationMatrix.shape[1])     # INFO : pour une matrice de 1 / nb d'éléments
                #         thisPropagationMatrix[i - start_row - 1 + k, j - start_col - 1 + l] = propagation_matrix[center_i - 1 + k, center_j - 1 + l]

        new_value = np.sum(neighborhood * thisPropagationMatrix)

        # print("---------------------------")
        # print("position : ", i, " ", j, "\nneighborhood :\n", neighborhood, "\nthisPropagationMatrix :\n", thisPropagationMatrix)
        # print("start row :", start_row, "start column : ", start_col)
        # print("\nvaleur : ", new_value)
        update_value(i,j,new_value)

# Fonction de simulation de diffusion de chaleur
def simulate_heat_diffusion(propagation_matrix, iterations):
    # indexgrid = np.zeros((n_rows, n_cols)) # pour verifier si le tableaux est parcourus correctement
    num_loops_rows = (n_rows - propagation_matrix.shape[0]) // (propagation_matrix.shape[0] - 1) + 1
    num_loops_cols = (n_cols - propagation_matrix.shape[1]) // (propagation_matrix.shape[1] - 1) + 1
    for iteration in range(iterations):
        # index=0
        for i in range(propagation_matrix.shape[0]):
            for j in range(propagation_matrix.shape[1]):
                for I in range(num_loops_rows):
                    for J in range(num_loops_cols):
                        x = I*propagation_matrix.shape[0]+i
                        y = J*propagation_matrix.shape[1]+j
                        if x> n_rows-1 or y> n_cols-1:
                            continue
                        # index += 1
                        # indexgrid[x,y]=index
                        if (material_grid[x,y]!=0): # if is allowed to be replaced
                            heat_simulation_on(x,y) 
        # print(indexgrid)
        grid = np.copy(new_grid)  # Mettez à jour la grille d'origine avec les nouvelles valeurs
        yield grid, iteration   # renvoie une version mise à jour de la grille à chaque étape du for


cmap = plt.get_cmap('coolwarm')
STARTTIME= time.time()
# Affichez la grille avec une carte de couleur à chaque itération
for grid, iteration in simulate_heat_diffusion(propagation_matrix, iterations):
    plt.imshow(grid[0:n_rows, 0:n_cols], cmap=cmap, interpolation='nearest')
    plt.colorbar()
    plt.text(0.05, 0.05, f'Iteration: {iteration}', transform=plt.gca().transAxes, color='white')
    if printNumbers!=-1:
        for i in range(0, n_rows):
            for j in range(0, n_cols):
                if printNumbers==0:
                    plt.text(j, i, f'{int(grid[i, j])}°C', color='black', fontsize=8, ha='center', va='center')
                elif printNumbers==1:
                    plt.text(j, i, f'{int(material_grid[i, j]*100)}%', color='black', fontsize=8, ha='center', va='center')
    plt.pause(0.001)  # Ajoutez une pause entre les itérations (ajustez selon vos besoins)
    # input("Appuyez sur Entrée pour continuer...") # attends la validation de l'utilisateur
    plt.clf()  # Effacez le graphique précédent pour la mise à jour

# Affichage de la fenêtre
print(time.time() - STARTTIME)        
plt.plot()
