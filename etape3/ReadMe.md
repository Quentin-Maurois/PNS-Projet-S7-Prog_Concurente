Quentin Maurois

Marco Laclavere

## Description du projet

Le projet a pour but de simuler une propagation de chaleur entre différentes cases et à travers différents matériaux.
Il est séparé en trois parties : une partie séquencielle, une partie avec parallélisme à grain fin et une dernière partie avec parallélisme correspondant aux coeurs disponnibles sur la machine.

# Utilisation

Tout d'abord, bien qu'il soit possible de lancer les programmes sur tout système d'exploitation, il est nécessaire pour lancer les programmes avec docker (les programmes qui ne sont pas restreints par le GIL) il est nécessaire de posséder un serveur graphique X.

## Avec GIL, environnement python "classique"

pour lancer cette partie du projet, il faut entrer:

> `./BarriereDiffusion.py`

vous pouvez consulté les arguments disponibles avec:

> `./BarriereDiffusion.py --help`

Les arguments disponibles sont:

- `--caseValue` : permet de determiner quels valeurs afficher dans les cases de la simulation : soit la temperature (`--caseValue 0`) soit le \*pourcentage de sensibilite a son environement\*\* (`-- caseValue 1`)

- `--demo` : permet de determiner quel demo sera utiliser pour la simulation : il en existe 4 de la plus petite grille jusqu'a la plus grande: (`--demo` avec comme valeur `0`, `1`, `2`, `3` ou `4`)
  > - demo0 : 5x5
  > - demo1 : 10x10
  > - demo2 : 25x25
  > - demo3 : 50x50
  > - demo4 : 100x100
- `--iteration` : permet de definir le nombre d'iteration qui sont a realiser _(par defaut 100)_

## Docker, les programmes sans GIL

#### Sur une machine sans serveur graphique X

Pour une machine qui n'utilise pas de base un serveur X, la solution la plus simple pour éviter tout problème de compatibilité est d'utiliser une machine virtuelle. Cela a été testé sur une machine ubuntu 22.04 () avec une installation minimale.

Il est nécessaire d'installer docker

> 'sudo apt install docker'

Vous pouvez maintenant suivre les instructions pour une machine avec un serveur X

#### Sur une machine avec serveur graphique X

Assurez vous d'avoir docker installé sur votre machine (tout dépends de votre OS et/ou package manager)

Le dossier contient des scripts shell. Autorisez l'execution de ces fichiers :

> 'chmod +x '\*.sh'

Le fichier dockerBuild.sh crée les images docker. La construction de l'une des images a été commentée car le programme semble avoir une fuite de mémoire problématique. Les images sont sous le nom "heat_diffusion" avec le tag :3 pour l'image qui présente le problème de mémoire et le tag :3.1 pour l'image qui fonctionne.

> './dockerBuild.sh'

Il y a deux images donc deux scripts permettant de les lancer. Le script runNoGIL_old.sh lance l'image gourmande en RAM et il n'est pas recommandé de l'utiliser actuellement et le script runNoGIL.sh lance la bonne image.
Ces scripts ouvrent une connexion locale qui permet au container d'accéder au serveur X de la machine et donc d'avoir une sortie graphique. ATTENTION cela peut poser des problèmes de sécurité car d'autres utilisateurs de la machine en local ont également accès a cette connexion. Les scripts ouvrent cette connexion avant de lancer le container et la ferme à la fin de l'execution du container.

> 'runNoGIL.sh'

# Analyse des résultats

### Resultat de la premiere etape (temps d'execution):

- demo 0
  > 7.258728504180908 sec
- demo 1
  > 7.686929941177368 sec
- demo 2
  > 10.299062252044678 sec
- demo 3
  > 20.986248016357422 sec
- demo 4
  > 97.18011999130249 sec

### Resultat de la seconde etape (temps d'execution):

- demo 0
  > 13.189159393310547 sec
- demo 1
  > 13.141157388687134 sec
- demo 2
  > 13.788105249404907 sec
- demo 3
  > 19.38200807571411 sec
- demo 4
  > 46.58527946472168 sec

Nous pouvons remarque que sur de petites grille tout faire sequentiellement est plus rapide que de creer un thread par cases de notre tableaux. Cela s'explique par le fait que créer un thread est plus cher que ce qu'il permet de gagner en temps.

Neanmoins nous pouvons voir que sur de plus grande grille, avoir multiplié le nombre de thread permet de gagner du temps malgrés leurs coup initial de creation.

### speedup

- demo 0
  > 0.550355659
- demo 1
  > 0.584950755
- demo 2
  > 0.746952686
- demo 3
  > 1.082769542
- demo 4
  > 2.086069271

### Efficacité

- demo 0
  > 0.550355659 / 25 = 0.022014226
- demo 1
  > 0.584950755 / 100 = 0.005849508
- demo 2
  > 0.746952686 / 625 = 0.001195124
- demo 3
  > 1.082769542 / 2500 = 0.000433108
- demo 4
  > 2.086069271 / 10000 = 0.000208607

Nous pouvons remarque que les resultats que nous avons obtenu sont tres bas et ne cesse de diminuer en augmentant la taille de la grille

Un si grand nombre de thread n'est pas efficace car il n'y a pas assez de coeur qui permettent de paralleliser le traitement
Cela explique pourquoi on observe une baisse d'efficacite de chacun de nos thread.

```
--- === Etape 2 === ---
Main
-  pour chaque iteration
-  pour chaque case de notre tableau:
-  -  mettre a jour la case
-    afficher le tableau
-  Fin
```

```
--- === Etape 3 === ---
Main
-  pour chaque case de notre tableau:
-  -  creer un thread associé a cette case
-
-  pour chaque iteration:
-  -  attendre a la barriere 1
-  -  afficher le tableau
-  -  attendre a la barriere 2
-  supprimer les threads
-  arreter la simulation
-  Fin

PseudoCodeThread
-  tant que on continue la simulation:
-  -  mettre a jour la case associé
-  -  attendre a la barriere 1
-  -  attendre a la barriere 2
-  Fin
```

```
--- === Etape 4 === ---
Main
-  creer une liste
-  pour chaque case du tableau :
-  -  Ajouter la case a la liste
-  creer le pool de thread
-  pour chaque iteration:
-  -  donner les taches au pool de thread
-  -  attendre que les taches ont toutes ete traité
-    afficher le tableau
-  Fin

PseudoCodeThread
-  mettre a jour la case associé
-  Fin
```
