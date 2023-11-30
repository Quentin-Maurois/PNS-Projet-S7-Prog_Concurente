import numpy as np
import matplotlib.pyplot as plt
import argparse
import threading
import time
import sys

# Création d'un analyseur d'arguments
parser = argparse.ArgumentParser(
    description="diffusion de la chaleur ponderer avec des pourcentages."
)

# Ajout d'arguments
parser.add_argument(
    "--caseValue",
    type=int,
    help="Affiche dans chaque case de la map (0) la temperature - (1) les pourcentages - (-1) rien",
)
parser.add_argument(
    "--demo",
    type=int,
    help="vous pouvez entrer 0,1,2,3 ou 4 afin d'obtenir une demontration préfaite",
)
parser.add_argument(
    "--iterations",
    type=int,
    help="choisissez le nombre d'iteration maximale a effectue",
)

# Analyse des arguments de ligne de commande
args = parser.parse_args()

printNumbers = -1

# Nombre d'itérations de simulation
maxIterations = 100
maxloop = 1  # nombre maximum changement de valeur dans chaque cellule par iteration

# Garder l'affichage à la fin
keepAtTheEnd = False

# Interruption des threads
Simulate = True

# Taille de la grille
n_rows, n_cols = 9, 5

# Créez la grille et initialisez les températures initiales
grid = np.zeros((n_rows, n_cols))

# zones infinies
material_grid = np.ones(grid.shape)

# ici la moitie superieur est beaucoup moins sensible a la propagation de chaleur
grid[4, :] = 100  # Zone chaude
material_grid[
    :4, :
] = 0.1  # la partie superieur de la map est moins affecte par la diffusion de chaleur
material_grid[:, :] = 0.1
material_grid[4, :] = 0  # Zone chaude
# Utilisation des arguments
if args.caseValue is not None:
    print("caseValue :", args.caseValue)
    if -2 < args.caseValue and args.caseValue < 2:
        printNumbers = args.caseValue
    else:
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
    maxIterations = args.iterations


# ici on peut voir que comme les cases froide sont dans un materiau plus sensible a la diffusion de chaleur, leur changement de temperature sera plus marqué que les cases chaude qui sont dans un materiaux moins sensible a la diffusion de chaleur
# grid[:, :1] = 100     # Zone chaude
# grid[:, -1] = -100    # Zone froide
# material_grid[:,0] = 0.1
# material_grid[:,-1] = 0.5

threads_grid = [[0 for y in range(n_cols)] for i in range(n_rows)]
new_grid = np.copy(grid)


# Matrice de propagation pour tout les matériau
propagation_matrix = np.array(
    [
        # [1, 4, 16, 4, 1],
        # [4, 16, 64, 16, 4],
        # [16, 64, 256, 64, 16],
        # [4, 16, 64, 16, 4],
        # [1, 4, 16, 4, 1]
        [1, 4, 1],
        [4, 16, 4],
        [1, 4, 1],
    ]
).astype(float)
propagation_matrix /= np.sum(propagation_matrix)
propagation_size = propagation_matrix.shape


def generate_neighboor_indice(i, j):
    sizeX = propagation_size[0] // 2
    sizeY = propagation_size[1] // 2
    start_row = max(0, i - sizeX)
    start_col = max(0, j - sizeY)
    end_row = min(n_rows, i + 1 + sizeX)
    end_col = min(n_cols, j + 1 + sizeY)
    return start_row, end_row, start_col, end_col


def update_value(i, j, value):
    if np.isnan(value):
        return
    percent = material_grid[i, j]
    current = grid[i, j]
    new_grid[i, j] = current + ((value - current) * percent)


def heat_simulation_on(
    i, j, startBarrier: threading.Barrier, endBarrier: threading.Barrier
):
    loop = 0
    s_row, e_row, s_col, e_col = generate_neighboor_indice(i, j)

    try:
        while Simulate:
            neighborhood = grid[s_row:e_row, s_col:e_col]
            while maxloop < loop:
                startBarrier.wait()
                loop = 0
                endBarrier.wait()
            loop += 1
            if neighborhood.shape == (
                propagation_size[0],
                propagation_size[1],
            ):  # si non près d'un bord
                update_value(i, j, np.sum(neighborhood * propagation_matrix))
            else:
                # thisPropagationMatrix match la forme de neighborhood avec le centre de cette matrice à l'emplacement des coordonnées i,j dans la matrice neighborhood

                start_row = max(0, i - (propagation_size[0] // 2))
                start_col = max(0, j - (propagation_size[1] // 2))

                thisPropagationMatrix = np.zeros(neighborhood.shape)

                # attribution des coefficients à la matrice :
                for k in range(neighborhood.shape[0]):
                    for l in range(neighborhood.shape[1]):
                        thisPropagationMatrix[
                            i - start_row - 1 + k, j - start_col - 1 + l
                        ] = 1 / (
                            thisPropagationMatrix.shape[0]
                            * thisPropagationMatrix.shape[1]
                        )  # INFO : pour une matrice de 1 / nb d'éléments
                        #         thisPropagationMatrix[i - start_row - 1 + k, j - start_col - 1 + l] = propagation_matrix[center_i - 1 + k, center_j - 1 + l]

                new_value = np.sum(neighborhood * thisPropagationMatrix)
                update_value(i, j, new_value)
                time.sleep(
                    0.002
                )  # libere la place pour que d'autres threads s'executent
    finally:
        while Simulate:
            startBarrier.wait()
            endBarrier.wait()
    startBarrier.wait()
    endBarrier.wait()
    return


# Fonction de simulation de diffusion de chaleur
def simulate_heat_diffusion(maxIteration: int, barrier: threading.Barrier):
    for i in range(maxIteration):
        startBarrier.wait()
        grid = np.copy(
            new_grid
        )  # Mettez à jour la grille d'origine avec les nouvelles valeurs
        yield grid, i + 1  # renvoie une version mise à jour de la grille à chaque étape du for
        endBarrier.wait()


nbThreads = 0

for x in range(n_rows):
    for y in range(n_cols):
        if x > n_rows or y > n_cols:
            continue
        if material_grid[x, y] != 0:
            nbThreads += 1
startBarrier = threading.Barrier(nbThreads + 1)
endBarrier = threading.Barrier(nbThreads + 1)

TIMESTART = time.time()
for stage in range(2):
    for x in range(n_rows):
        for y in range(n_cols):
            if x > n_rows or y > n_cols:
                continue
            if (
                material_grid[x, y] != 0
            ):  # if is allowed to be replaced# Création d'un objet Thread
                if stage == 0:
                    threads_grid[x][y] = threading.Thread(
                        target=heat_simulation_on, args=(x, y, startBarrier, endBarrier)
                    )
                else:
                    # Démarrage du thread
                    threads_grid[x][y].start()

cmap = plt.get_cmap("coolwarm")
min_temperature = np.min(grid)  # Température minimale
max_temperature = np.max(grid)  # Température maximale
try:
    # Affichez la grille avec une carte de couleur à chaque itération
    for grid, iteration in simulate_heat_diffusion(maxIterations, startBarrier):
        plt.imshow(grid[0:n_rows, 0:n_cols], cmap=cmap, interpolation="nearest", vmin=min_temperature, vmax=max_temperature)
        plt.colorbar()
        plt.text(
            0.05,
            0.05,
            f"Iteration: {iteration}",
            transform=plt.gca().transAxes,
            color="white",
        )
        if printNumbers != -1:
            for i in range(0, n_rows):
                for j in range(0, n_cols):
                    if printNumbers == 0:
                        plt.text(
                            j,
                            i,
                            f"{int(grid[i, j])}°C",
                            color="black",
                            fontsize=8,
                            ha="center",
                            va="center",
                        )
                    elif printNumbers == 1:
                        plt.text(
                            j,
                            i,
                            f"{material_grid[i, j]}",
                            color="black",
                            fontsize=8,
                            ha="center",
                            va="center",
                        )

        plt.pause(
            0.01
        )  # Ajoutez une pause entre les itérations (ajustez selon vos besoins)
        # input("Appuyez sur Entrée pour continuer...") # attends la validation de l'utilisateur
        plt.clf()  # Effacez le graphique précédent pour la mise à jour
        # Affichage de la fenêtre
finally:
    print(time.time() - TIMESTART)
    Simulate = False
    startBarrier.wait()
    endBarrier.wait()  # Débloquer tous les threads pour terminer leur exécution
    for x in range(n_rows):
        for y in range(n_cols):
            if x > n_rows or y > n_cols:
                continue
            if material_grid[x, y] != 0:  # if is allowed to be replaced
                threads_grid[x][y].join()  # Attendre que chaque thread se termine
    if keepAtTheEnd:
        plt.plot()
        input("Apuyer sur une touche pour fermer le programme.")
    sys.exit(0)  # Terminer proprement le programme après l'interruption
