import numpy as np
import matplotlib.pyplot as plt

printNumbers = False

# Taille de la grille
n_rows, n_cols = 32, 32

# Créez la grille et initialisez les températures initiales
grid = np.zeros((n_rows, n_cols))
boolean_grid = np.full((n_rows, n_cols), True, dtype=bool)



#zones infinies
# grid[:, :1] = 100     # Zone chaude
# boolean_grid[:, :1] = False
# grid[:, -1] = -50    # Zone froide
# boolean_grid[:, -1] = False
grid[15:17, 15:17] = 100
boolean_grid[15:17, 15:17] = False


# Matrice de propagation pour un matériau
propagation_matrix = np.array([[1/36, 4/36, 1/36],  # faible propagation
                               [4/36, 16/36, 4/36],
                               [1/36, 4/36, 1/36]])
propagation_matrix = np.array([[1/9, 1/9, 1/9],     # forte propagation
                               [1/9, 1/9, 1/9],
                               [1/9, 1/9, 1/9]])
propagation_size = propagation_matrix.shape[0]


# Fonction de simulation de diffusion de chaleur
def simulate_heat_diffusion(grid, propagation_matrix, iterations):
    for iteration in range(iterations):
        new_grid = np.copy(grid)
        for i in range(n_rows):
            for j in range(n_cols):
                if (boolean_grid[i,j]): # if is allowed to be replaced
                    neighborhood = grid[max(0, i - 1):min(n_rows, i + 2), max(0, j - 1):min(n_cols, j + 2)] # neighborhood de taille variable : min (2,2) et max (3,3)
                    if (neighborhood.shape == (3, 3)):  # si non près d'un bord
                        new_grid[i, j] = np.sum(neighborhood * propagation_matrix)
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

                        new_grid[i, j] = new_value if not np.isnan(new_value) else 0  # Remplacer NaN par 0 si nécessaire

        grid = np.copy(new_grid)  # Mettez à jour la grille d'origine avec les nouvelles valeurs
        yield grid, iteration   # renvoie une version mise à jour de la grille à chaque étape du for

# Nombre d'itérations de simulation
iterations = 10000

cmap = plt.get_cmap('coolwarm')

# Affichez la grille avec une carte de couleur à chaque itération
for grid, iteration in simulate_heat_diffusion(grid, propagation_matrix, iterations):
    # plt.imshow(grid[1:n_rows-1, 1:n_cols-1], cmap=cmap, interpolation='nearest')    # n'affiche pas les bords
    plt.imshow(grid[0:n_rows, 0:n_cols - 0], cmap=cmap, interpolation='nearest')    # affiche les bords
    plt.colorbar()
    plt.text(0.05, 0.05, f'Iteration: {iteration}', transform=plt.gca().transAxes, color='white')
    if(printNumbers):
        for i in range(0, n_rows ):
            for j in range(0, n_cols ):
                plt.text(j , i , f'{int(grid[i, j])}°C', color='black', fontsize=8, ha='center', va='center')
    plt.pause(0.001)  # Ajoutez une pause entre les itérations (ajustez selon vos besoins)
    # input("Appuyez sur Entrée pour continuer...") # attends la validation de l'utilisateur
    plt.clf()  # Effacez le graphique précédent pour la mise à jour

# Affichage de la fenêtre
plt.imshow(grid[0:n_rows, 0:n_cols], cmap=cmap, interpolation='nearest')
plt.colorbar()
plt.text(0.05, 0.05, f'Iteration: {iterations}', transform=plt.gca().transAxes, color='white')
if (printNumbers):
    for i in range(0, n_rows):
        for j in range(0, n_cols):
            plt.text(j, i, f'{int(grid[i, j])}°C', color='black', fontsize=8, ha='center', va='center')
plt.pause(-1)
plt.plot()
