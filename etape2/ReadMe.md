# Etape 2 - Diffusion de chaleur

Quentin Maurois

Marco Laclavere

## Avancement du projet

Nous avons implementer un affichage afin de pouvoir observer l'evolution des temperatures sur une grille.

Nous sommes en train d'explorer 2 approches afin de prendre en compte les different materiaux qui devront etre representé:

- En utilisant des matrices: cette approche conciste a ne plus utiliser qu'une seule matrice mais une pour chaque type de materiaux que nous representons. Cela a pour avantage de facilement calibrer pour chaque materiaux la diffusion de chaleur qui l'influera ainsi que a quel point.
- En utilisant des pourcentages: Ici nous n'utilisons qu'une seule matrice pour diffuser la chaleur mais celle ci sera ponderer par un pourcentage. Lors de la diffusion de la chaleur nous allons calculer la difference de temperature entre avant et apres la diffusion de chaleur et multiplier cette difference par un pourcentage afin de savoir enquel proportion nous devons prendre en compte la nouvelle valeur

  > valeur_apres_diffusion = (valeur_calculer_avec_la_matrice - valeur_avant_diffusion) \* pourcentage

  Cela a comme avantage que nous pouvons facilement representer un grand nombre de materiaux
  Cependant cela se fait au detriment de la qualité de notre modele etant donnée que nous simplifions fortement une grande quantité de parametre (densité du materiaux, sa composition, etc).

## Utilisation

### Modele à multiples matrices

Afin de le lancer :

> `python .\heatDiffusion_PercentagePath.py`

Nous n'avons pas encore creer d'argument ou d'options afin de personnaliser ce modele

### Modele à pourcentage

Afin de le lancer :

> `python .\heatDiffusion_PercentagePath.py`

Pour ce modele nous avons creer 3 arguments possible:

- `caseValue <int>` : permet de definir quelle valeur nous voulons afficher dans chaque cases de notre figure (sur les grands tableaux cela devient illisible)
  - 0 permet d'afficher les temperatures
  - 1 permet d'afficher le pourcentage d'absorption de la chaleur de la case
- `iterations <int>` : permet de fefinir le nombre maximale d'iteration a faire
- `demo <int>` : permet d'afficher differente d'autres figures que celle sans arguments:

  - sans cette option : une ligne au centre de 100°C fixe

    la partie inferieur du tableau est tres sensible au changement de temperature.

    la partie superieur est peu sensible au changement de temperatures

  - 0 : les bords gauche bas et droit de la figure ne peuvent pas changer de temperature (100°C)
    le centre de la figure a une temperature initiale de -100°C
  - 1 : le bord haut et bas de la figure ne peuvent pas changer de temperature ils sont respectivement a -100 et 100°C
    la zone au centre de la figure change difficilement de temperature (1%) alors que les autres cases changent normalement (100%)

## Perspective

Nous sommes en train de développer un outil qui permettra de "peindre" des types de materiaux sur une toile qui sera ensuite utilise par notre programme de diffusion de la chaleur afin de faciliter la creation de simulation.
Nous comptons aussi changer l'affichage de nos figures afin de mettre en evidence a la fois la temperature de l'element mais aussi sa composition. Car pour le moment nous ne pouvons que afficher les temperatures.
