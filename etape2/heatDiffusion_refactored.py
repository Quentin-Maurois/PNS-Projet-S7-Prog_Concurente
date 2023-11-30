import numpy as np
import matplotlib.pyplot as plt
import materialSelectionFunction

printNumbers = False
np.set_printoptions(precision=2, suppress=True)


# Taille de la grille
# n_rows, n_cols = 100, 100


# Nombre d'itérations de simulation
# iterations = 10000      # max iterations



#fonction des threads
def updateGrid(i, j, inputGrid, outputGrid, matrices, staticGrid, materialGrid, n_rows, n_cols, propagation_size):
    if (staticGrid[i, j]):  # if is allowed to be replaced
        neighborhood = inputGrid[max(0, i - 1):min(n_rows, i + 2),
                       max(0, j - 1):min(n_cols, j + 2)]  # neighborhood de taille variable : min (2,2) et max (3,3)
        propagation_matrix = matrices[materialGrid[i, j]]
        if (neighborhood.shape == (3, 3)):  # si non près d'un bord
            outputGrid[i, j] = np.sum(neighborhood * propagation_matrix)
        else:
            # thisPropagationMatrix match la forme de neighborhood avec le centre de cette matrice à l'emplacement des coordonnées i,j dans la matrice neighborhood

            start_row = max(0, i - (propagation_size // 2))
            start_col = max(0, j - (propagation_size // 2))

            thisPropagationMatrix = np.zeros(neighborhood.shape)
            center_i, center_j = neighborhood.shape[0] // 2, neighborhood.shape[1] // 2

            # attribution des coefficients à la matrice :
            for k in range(neighborhood.shape[0]):
                for l in range(neighborhood.shape[1]):
                    thisPropagationMatrix[i - start_row - 1 + k, j - start_col - 1 + l] = 1 / (
                                thisPropagationMatrix.shape[0] * thisPropagationMatrix.shape[1])  # INFO : pour une matrice de 1 / nb d'éléments
                    #         thisPropagationMatrix[i - start_row - 1 + k, j - start_col - 1 + l] = propagation_matrix[center_i - 1 + k, center_j - 1 + l]

            new_value = np.sum(neighborhood * thisPropagationMatrix)

            # print("---------------------------")
            # print("position : ", i, " ", j, "\nneighborhood :\n", neighborhood, "\nthisPropagationMatrix :\n", thisPropagationMatrix)
            # print("start row :", start_row, "start column : ", start_col)
            # print("\nvaleur : ", new_value)

            outputGrid[i, j] = new_value if not np.isnan(new_value) else 0  # Remplacer NaN par 0 si nécessaire




# Fonction de simulation de diffusion de chaleur
def simulate_heat_diffusion(grid, matrices, iterations, n_rows, n_cols, staticGrid, materialGrid, propagation_size):
    for iteration in range(iterations):
        new_grid = np.copy(grid)
        for i in range(n_rows):
            for j in range(n_cols):
                updateGrid(i, j, grid, new_grid, matrices, staticGrid, materialGrid, n_rows, n_cols, propagation_size)


        grid = np.copy(new_grid)  # Mettez à jour la grille d'origine avec les nouvelles valeurs
        yield grid, iteration   # renvoie une version mise à jour de la grille à chaque étape du for
    return


def HDPlot(n_rows, n_cols, iterations, keepAtTheEnd):
    # Créez la grille et initialisez les températures initiales
    grid = np.full((n_rows, n_cols), 20, dtype=float)
    materialGrid = np.zeros((n_rows, n_cols), dtype=int)
    staticGrid = np.full((n_rows, n_cols), True, dtype=bool)  # grid that stores the static cells (the ones that you do not want to be modified)

    ### Manual selection ###

    ### gauche droite 1 colone###
    grid[:, :1] = -20  # Zone chaude
    staticGrid[:, :1] = False
    # grid[:, -1] = -50  # Zone froide
    # staticGrid[:, -1] = False
    materialGrid[:, n_cols // 2] = 1
    materialGrid[:, n_cols // 2 -1] = 1
    materialGrid[:, n_cols // 4] = 2
    materialGrid[:, n_cols // 2 + n_cols // 4] = 2

    ### gauche droite ###
    # grid[:, :n_cols // 2] = 100
    # grid[:, n_cols // 2:] = -100

    ### centre ###
    # grid[15:17, 15:17] = 100
    # staticGrid[15:17, 15:17] = False

    ## coins ###
    # grid[0,0] = 100
    # staticGrid[0,0] = False
    # grid[-1,-1] = -100
    # staticGrid[-1,-1] = False
    ### --------------- ###

    ### Declaration of the different types of matrices ###
    matrices = []  # contains the matrices for all materials
    matrices.append(np.array([[1 / 9, 1 / 9, 1 / 9],  # propagation matrix in the air
                              [1 / 9, 1 / 9, 1 / 9],
                              [1 / 9, 1 / 9, 1 / 9]]))
    matrices.append(np.array([[1 / 42, 2 / 42, 1 / 42],  # propagation matrix in concrete
                              [2 / 42, 30 / 42, 2 / 42],
                              [1 / 42, 2 / 42, 1 / 42]]))
    matrices.append(np.array([[1 / 36, 4 / 36, 1 / 36],  # propagation matrix in wood
                              [4 / 36, 16 / 36, 4 / 36],
                              [1 / 36, 4 / 36, 1 / 36]]))

    propagation_size = matrices[0].shape[0]





    cmap = plt.get_cmap('coolwarm')
    min_temperature = np.min(grid)  # Température minimale
    max_temperature = np.max(grid)  # Température maximale

    materialColors = plt.cm.viridis(np.linspace(0, 1, np.max(materialGrid)))

    # Affichez la grille avec une carte de couleur à chaque itération
    for grid, iteration in simulate_heat_diffusion(grid, matrices, iterations, n_rows, n_cols, staticGrid, materialGrid, propagation_size):
        plt.imshow(grid[0:n_rows, 0:n_cols - 0], cmap=cmap, interpolation='nearest', vmin=min_temperature, vmax=max_temperature)
        plt.colorbar()
        plt.text(0.05, 0.05, f'Iteration: {iteration}', transform=plt.gca().transAxes, color='white')

        if(printNumbers or np.max(materialGrid)>0 or np.min(staticGrid)==False):
            for i in range(0, n_rows ):
                for j in range(0, n_cols ):
                    if (printNumbers):
                        plt.text(j , i , f'{int(grid[i, j])}°C', color='black', fontsize=8, ha='center', va='center')
                    if (materialGrid[i][j] > 0):
                        plt.text(j, i, f'{int(materialGrid[i, j])}', color=materialColors[materialGrid[i][j]-1], fontsize=8, ha='right', va='bottom')
                    if (staticGrid[i][j] == False):
                        plt.text(j, i, f'x', color='red', fontsize=8, ha='left', va='top')
        plt.pause(0.001)  # Ajoutez une pause entre les itérations (ajustez selon vos besoins)
        # input("Appuyez sur Entrée pour continuer...") # attends la validation de l'utilisateur
        plt.clf()  # Effacez le graphique précédent pour la mise à jour

    if(keepAtTheEnd):
        # Affichage de la fenêtre
        plt.imshow(grid[0:n_rows, 0:n_cols], cmap=cmap, interpolation='nearest', vmin=min_temperature, vmax=max_temperature)
        plt.colorbar()
        plt.text(0.05, 0.05, f'Iteration: {iterations}', transform=plt.gca().transAxes, color='white')
        if (printNumbers or np.max(materialGrid) > 0 or np.min(staticGrid) == False):
            for i in range(0, n_rows):
                for j in range(0, n_cols):
                    if (printNumbers):
                        plt.text(j, i, f'{int(grid[i, j])}°C', color='black', fontsize=8, ha='center', va='center')
                    if (materialGrid[i][j] > 0):
                        plt.text(j, i, f'{int(materialGrid[i, j])}', color=materialColors[materialGrid[i][j] - 1],
                                 fontsize=8, ha='right', va='bottom')
                    if (staticGrid[i][j] == False):
                        plt.text(j, i, f'x', color='red', fontsize=8, ha='left', va='top')
        plt.pause(-1)
        plt.plot()


# HDPlot(100, 100, 500)