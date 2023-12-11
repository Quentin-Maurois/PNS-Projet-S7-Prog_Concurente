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

Lors de cette etape nous avons remplacer la creation d'un thread par case par un pool de x threads (x etant le nombre de coeur de la machine). Auquels nous donneront des taches a réaliser.

Lors de la réalisation de cette etape nous avons eu de meilleurs resultats que lors de l'etape precedente. Cela s'explique par le fait que on a limité le nombre de thread crée au nombre de coeur de notre machine. Ainsi en creant moins de threads nous gagnons du temps. Cependant par rapport a la premiere version sequentiel du projet nos resultats sont toujours moins bons. Nous pensons que cela est a cause non seulement du coup de creation des threads mais aussi que donner une tache a un thread est plus couteux que ce qu'elle nous fais gagner en temps.

### speedup

- demo 0
  > 0,5124871033
- demo 1
  > 0,4981214652
- demo 2
  > 0,5230048069
- demo 3
  > 0,513056722
- demo 4
  > 0,4236033876

### Efficacité

- demo 0
  > 6,41%
- demo 1
  > 6,23%
- demo 2
  > 6,54%
- demo 3
  > 6,41%
- demo 4
  > 5,30%

Nous pouvons clairement voir ici que le parallelisme a entrainé une baisse des performances. Notre efficacite a augmenté comparé au precedents resultats. Neanmoins ils montrent bien que le parralelisme ne nous fais perdre en performance dans notre cas.

## Pseudo code des differentes etapes

### Etape 2

```
Main
-  pour chaque iteration
-  -  pour chaque case de notre tableau:
-  -  -  mettre a jour la case
-  -  afficher le tableau
-  Fin
```

### Etape 3

```
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

### Etape 4

```
Main
-  creer une liste
-  pour chaque case du tableau :
-  -  Ajouter la case a la liste
-  decoupe la liste en partie le plus egale en fonction du nombre de coeur
-  creer le pool de thread
-  pour chaque iteration:
-  -  donner les taches au pool de thread
-  -  attendre que les taches ont toutes ete traité
-    afficher le tableau
-  Fin

PseudoCodeThread
-  pour chaque element de la liste:
-  -  mettre a jour la case associé
-  Fin
```
