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

### Sur une machine sans serveur graphique X

Pour une machine qui n'utilise pas de base un serveur X, la solution la plus simple pour éviter tout problème de compatibilité est d'utiliser une machine virtuelle. Cela a été testé sur une machine ubuntu 22.04 () avec une installation minimale.

Il est nécessaire d'installer docker

> 'sudo apt install docker'

Vous pouvez maintenant suivre les instructions pour une machine avec un serveur X

### Sur une machine avec serveur graphique X

Assurez vous d'avoir docker installé sur votre machine (tout dépends de votre OS et/ou package manager)

Le dossier contient des scripts shell. Autorisez l'execution de ces fichiers :

> 'chmod +x '\*.sh'

Le fichier dockerBuild.sh crée les images docker. La construction de l'une des images a été commentée car le programme semble avoir une fuite de mémoire problématique. Les images sont sous le nom "heat_diffusion" avec le tag :3 pour l'image qui présente le problème de mémoire et le tag :3.1 pour l'image qui fonctionne.

> './dockerBuild.sh'

Il y a deux images donc deux scripts permettant de les lancer. Le script runNoGIL_old.sh lance l'image gourmande en RAM et il n'est pas recommandé de l'utiliser actuellement et le script runNoGIL.sh lance la bonne image.
Ces scripts ouvrent une connexion locale qui permet au container d'accéder au serveur X de la machine et donc d'avoir une sortie graphique. ATTENTION cela peut poser des problèmes de sécurité car d'autres utilisateurs de la machine en local ont également accès a cette connexion. Les scripts ouvrent cette connexion avant de lancer le container et la ferme à la fin de l'execution du container.

> 'runNoGIL.sh'

# Analyse des résultats

## Résultats de la premiere étape : séquencielle (temps d'exécution):

|        |                    |
| ------ | ------------------ |
| demo 0 | 6.421178817749023  |
| demo 1 | 6.402407884597778  |
| demo 2 | 6.776578903198242  |
| demo 3 | 8.27846622467041   |
| demo 4 | 13.312830209732056 |

## Résultats de la seconde étape : à grain fin (temps d'exécution):

### Avec GIL :

|        | Temps  | Facteur d’accélération | Efficacité   |
| ------ | ---------------------- | ------------ | ------ |
| Démo 0 | 7.3907976150512695     | 0,8688072861 | 10,86% |
| Démo 1 | 7.702845811843872      | 0,8311743531 | 10,39% |
| Démo 2 | 9.808361053466797      | 0,6908981905 | 8,64%  |
| Démo 3 | 20.48836588859558      | 0,4040569301 | 5,05%  |
| Démo 4 | 88.99322724342346      | 0,1495937458 | 1,87%  |

### Sans GIL :

|        | Temps  | Facteur d’accélération | Efficacité   |
| ------ | ---------------------- | ------------ | ----- |
| Démo 0 | 12.786301612854004     | 0,5021920343 | 6,28% |
| Démo 1 | 12.763670444488525     | 0,501611814  | 6,27% |
| Démo 2 | 13.362324714660645     | 0,5071407145 | 6,34% |
| Démo 3 | 17.85131049156189      | 0,4637455737 | 5,80% |
| Démo 4 | 41.5448956489563       | 0,3204444253 | 4,01% |

## Résultats de la troisième étape : à gros grain où le nombre de thread correspond au nombre de coeurs de la machine (temps d'exécution):

### Avec GIL :

|        | Temps | Facteur d’accélération | Efficacité   |
| ------ | ---------------------- | ------------ | ------ |
| Démo 0 | 6.60429310798645       | 0,9722734459 | 12,15% |
| Démo 1 | 6.7815327644348145     | 0,9440945148 | 11,80% |
| Démo 2 | 7.584274530410767      | 0,8935039042 | 11,17% |
| Démo 3 | 13.034704208374023     | 0,6351096344 | 7,94%  |
| Démo 4 | 39.479583978652954     | 0,3372079659 | 4,22%  |

### Sans GIL :

|        | Temps  | Facteur d’accélération | Efficacité   |
| ------ | ---------------------- | ------------ | ----- |
| Démo 0 | 12.529444694519043     | 0,5124871033 | 6,41% |
| Démo 1 | 12.853105783462524     | 0,4981214652 | 6,23% |
| Démo 2 | 12.957010746002197     | 0,5230048069 | 6,54% |
| Démo 3 | 16.135576963424683     | 0,513056722  | 6,41% |
| Démo 4 | 31.427582025527954     | 0,4236033876 | 5,30% |

Nous pouvons remarquer que la méthode séquencielle est toujours la plus rapide peu importe la taille de grille des démos ou de l'utilisation de GIL ou non.

Nous pouvons remarquer que lorsque l'on utilise pas le GIL sur des grilles de petite taille le code est est quasiment deux fois plus lent qu'avec GIL.
La tendence s'inverse d'autant plus que la grille est grande.

Il est possible que le fait que la méthode séquencielle soit plus rapide s'explique par le fait que l'opération effectuée dans les threads de mettre à jour la cellule soit en réalité une action très rapide et efficace en elle même. Le fait de créer et organiser des threads autour ne fait que ralentir la méthode. Comme nous l'avons vu en cours, plus une méthode est rapide et moins un tread y étant affecté est efficace.

Dans la partie multithreadée maintenant : l'utilisation ou non de GIL dépends de la taille de la grille car plus la grille est petite et plus GIL ralentis le processus. Cela est sûrement dû à la façon dont GIL est implémenté qui permet de gérer efficacement ce genre de problèmes (création de threads et affection de la fonction). En revance on voit bien que désactiver GIL sur des grandes grilles permet une nette amélioration bien que ce soit plus lent qu'en séquenciel comme vu plus haut.

Encore dans la partie multithreadée : le fait de limiter et gérer en fonction les threads au coeurs effectifs de la machine permet avec et sans GIL d'améliorer la vitesse d'execution sur toutes les démos effectuées. Encore une fois GIL est plus rapide avec des petites grilles et plus lent sur les grandes grilles.

## Explication de code

Voici une vision simplifiée de nos codes avec du pseudo code. La partie de mise à jour des cellules n'est pas décomposée car il n'est pas nécessaire de le faire. En effet elle est toujours la même au travers de tous les codes et c'est seulement la façon de l'appeler qui est différentes entre les codes.

Pour chacun de nos programes nous avons 2 grilles: une qui est la dernieres grille affichée, et l'autre qui est celle que nous allons afficher a lors de l'iteration en cours. Ainsi pour mettre a jour une case nous recuperons les valeurs de la precedente grille avant de mettre la nouvelle valeur dans la nouvelle grille.

### Etape 2

Pour cette etape nous parcourons l'entierete des cases et nous les mettons a jour avant de rafraichir l'affichage de la simulation

```
Main
-  pour chaque iteration
-  pour chaque case de notre tableau:
-  -  mettre a jour la case
-    afficher le tableau
-  Fin
```

### Etape 3

Ici nous avons deux codes qui vont sections de codes qui vont s'executer en parallele, un pour le thread principal et l'autre pour chacun des threads. Pour cette etape à grains fin chacune des cases de notre simultation aura un thread associe.
La barriere a pour but d'attendre que tout les threads ont mis a jour leurs cases. Une fois que cela est fait, alors le thread principal va mettre a jour l'affichage avant d'attendre de nouveau que les cases soient mises a jours etc. Ici la barriere est importante car elle permet de s'assurer que tout les threads mettent a jour une et une unique fois la valeurs de leurs cases. Si les cases se mettent a jour plusieurs fois cela ne faussera pas le resultat cependant enleve cette barriere va empecher que chaque cases est mise a jour entre deux iteration: faussant alors les resultats.

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

Ici nous avons creer un pool de threads (egaux au nombre de coeur de la machine) et separe les cases a mettre a jour en autant de liste de taille les plus egales possible. Ainsi a chaque iteration chaque thread va devoir mettre a jour les cases de la liste qui lui est attribue. Une fois que tout les threads ont traité les cases qui lui a ete assigne (donc que toutes les cases ont ete mises a jour) alors on rafraichis l'affichage de la simulation avant de recommencer.

```
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
