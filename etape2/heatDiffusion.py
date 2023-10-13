import numpy as np
import matplotlib.pyplot as plt

# Taille de la grille
n_rows, n_cols = 12, 12 # + 2 car les cellules de bordure ne sont pas mises à jour

# Créez la grille et initialisez les températures initiales
grid = np.zeros((n_rows, n_cols))
grid[:, :1] = 100     # Zone chaude
grid[:, -1] = -50    # Zone froide

np.set_printoptions(precision=2, suppress=True)
print(grid)

# Matrice de propagation pour un matériau
propagation_matrix = np.array([[1/36, 4/36, 1/36],
                               [4/36, 16/36, 4/36],
                               [1/36, 4/36, 1/36]])

# Fonction de simulation de diffusion de chaleur
def simulate_heat_diffusion(grid, propagation_matrix, iterations):
    for iteration in range(iterations):
        new_grid = np.copy(grid)
        for i in range(1, n_rows - 1):
            for j in range(1, n_cols - 1):
                neighborhood = grid[i - 1:i + 2, j - 1:j + 2]
                new_grid[i, j] = np.sum(neighborhood * propagation_matrix)
        grid = np.copy(new_grid)  # Mettez à jour la grille d'origine avec les nouvelles valeurs
        yield grid, iteration   # renvoie une version mise à jour de la grille à chaque étape du for

# Nombre d'itérations de simulation
iterations = 1000000

cmap = plt.get_cmap('coolwarm')

# Affichez la grille avec une carte de couleur à chaque itération
for grid, iteration in simulate_heat_diffusion(grid, propagation_matrix, iterations):
    # plt.imshow(grid[1:n_rows-1, 1:n_cols-1], cmap=cmap, interpolation='nearest')    # n'affiche pas les bords
    plt.imshow(grid[0:n_rows, 0:n_cols - 0], cmap=cmap, interpolation='nearest')    # affiche les bords
    plt.colorbar()
    plt.text(0.05, 0.05, f'Iteration: {iteration}', transform=plt.gca().transAxes, color='white')
    for i in range(0, n_rows ):
        for j in range(0, n_cols ):
            plt.text(j , i , f'{int(grid[i, j])}°C', color='black', fontsize=8, ha='center', va='center')
    plt.pause(0.001)  # Ajoutez une pause entre les itérations (ajustez selon vos besoins)
    plt.clf()  # Effacez le graphique précédent pour la mise à jour

# Affichage de la fenêtre
plt.imshow(grid[1:n_rows-1, 1:n_cols-1], cmap=cmap, interpolation='nearest')
plt.colorbar()
plt.text(0.05, 0.05, f'Iteration: {iterations}', transform=plt.gca().transAxes, color='white')
plt.pause(-1)
plt.plot()
