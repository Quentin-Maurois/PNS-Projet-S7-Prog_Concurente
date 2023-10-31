import tkinter as tk

def create_material_simulation(grid_width, grid_height, cell_size, material_names):
    # Matériau par défaut
    default_material = 0

    # Variables pour le suivi du clic de la souris
    mouse_pressed = False
    prev_row, prev_col = -1, -1

    # Créez un dictionnaire qui mappe les noms des matériaux à des valeurs numériques
    material_values = {material: i for i, material in enumerate(material_names)}

    def draw_material(event):
        nonlocal mouse_pressed, prev_row, prev_col

        x, y = event.x, event.y
        col = x // cell_size
        row = y // cell_size

        if mouse_pressed and (prev_row, prev_col) != (row, col):
            material_value = material_values.get(current_material.get(), default_material)
            material_color = material_colors.get(current_material.get(), "black")
            canvas.create_rectangle(col * cell_size, row * cell_size,
                                    (col + 1) * cell_size, (row + 1) * cell_size,
                                    fill=material_color, outline="gray")
            grid_data[row][col] = material_value
            prev_row, prev_col = row, col

    def mouse_pressed_event(event):
        nonlocal mouse_pressed, prev_row, prev_col

        mouse_pressed = True
        prev_row, prev_col = -1, -1
        draw_material(event)

    def mouse_released_event(event):
        nonlocal mouse_pressed

        mouse_pressed = False

    def next_step():
        root.quit()

    def finish():
        # Ferme la fenêtre actuelle
        root.destroy()

    # Créez une fenêtre Tkinter
    root = tk.Tk()
    root.title("Simulation de Propagation de Chaleur")

    # Créez un canevas pour dessiner
    canvas = tk.Canvas(root, width=grid_width * cell_size, height=grid_height * cell_size)
    canvas.pack()

    # Créez une liste de matériaux à partir du tableau de noms de matériaux
    materials = material_names
    current_material = tk.StringVar(value=materials[0])

    # Créez un dictionnaire associant les matériaux à des couleurs aléatoires
    material_colors = {
        material: f"#{(i * 100) % 256:02X}{(i * 50) % 256:02X}{(i * 25) % 256:02X}"
        for i, material in enumerate(materials)
    }

    # Créez des boutons radio pour choisir le matériau
    for material in materials:
        tk.Radiobutton(root, text=material, variable=current_material, value=material).pack()

    # Initialisez la grille avec la valeur par défaut
    grid_data = [[default_material for _ in range(grid_width)] for _ in range(grid_height)]

    # Remplissez le canevas avec la couleur du matériau par défaut
    canvas.create_rectangle(0, 0, grid_width * cell_size, grid_height * cell_size, fill=material_colors.get(materials[0], "white"))

    # Associez des fonctions d'événements à la souris
    canvas.bind("<Button-1>", mouse_pressed_event)
    canvas.bind("<B1-Motion>", draw_material)
    canvas.bind("<ButtonRelease-1>", mouse_released_event)

    # Ajoutez un rectangle pour chaque case de la grille avec la couleur par défaut
    for row in range(grid_height):
        for col in range(grid_width):
            x0 = col * cell_size
            y0 = row * cell_size
            x1 = (col + 1) * cell_size
            y1 = (row + 1) * cell_size
            canvas.create_rectangle(x0, y0, x1, y1, outline="black")

    # Ajoutez un bouton "Passer à la suite"
    next_button = tk.Button(root, text="Passer à la suite", command=next_step)
    next_button.pack()

    # Exécutez la fenêtre Tkinter
    root.mainloop()

    # Après que l'utilisateur ait fait ses sélections, la fonction retourne le tableau
    windows.append(root)
    return grid_data

# Créez une liste pour stocker les fenêtres
windows = []

# Utilisation de la fonction pour créer une simulation avec un tableau de noms de matériaux
# grid_data = create_material_simulation(10, 10, 40, ["Air", "Béton", "Bois"])   # sélection des matériaux
# print("[")
# for row in grid_data:
#     print(row)
# print("]")
#
# create_material_simulation(10, 10, 40, ["Modifiable", "Statique"])  # sélection des zones modifiables
# print("[")
# for row in grid_data:
#     print(row)
# print("]")

for window in windows:
    window.destroy()

