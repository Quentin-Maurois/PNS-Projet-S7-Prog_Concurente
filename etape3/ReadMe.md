Quentin Maurois

Marco Laclavere



## Description du projet

Le projet a pour but de simuler une propagation de chaleur entre différentes cases et à travers différents matériaux.
Il est séparé en trois parties : une partie séquencielle, une partie avec parallélisme à grain fin et une dernière partie avec parallélisme correspondant aux coeurs disponnibles sur la machine.

# Utilisation

Tout d'abord, bien qu'il soit possible de lancer les programmes sur tout système d'exploitation, il est nécessaire pour lancer les programmes avec docker (les programmes qui ne sont pas restreints par le GIL) il est nécessaire de posséder un serveur graphique X. 


## Avec GIL, environnement python "classique"

pour lancer cette partie du projet, il faut ecrire:
> `./BarriereDiffusion.py`


vous pouvez consulté les arguments disponibles avec:
> `./BarriereDiffusion.py --help`
Les arguments disponibles sont:
  > - `--caseValue` : permet de determiner quels valeurs afficher dans les cases de la simulation : soit la temperature (`--caseValue 0`) soit le *pourcentage de sensibilite a son environement\** (`-- caseValue 1`)

  > - `--demo` : permet de determiner quel demo sera utiliser pour la simulation : il en existe 4 (`--demo` avec comme valeur`0`,`1`,`2`,`3` ou `4`)
  > - `--iteration` : permet de definir le nombre d'iteration qui sont a realiser *(par defaut 100)*

## Docker, les programmes sans GIL
#### Sur une machine sans serveur graphique X
Pour une machine qui n'utilise pas de base un serveur X, la solution la plus simple pour éviter tout problème de compatibilité est d'utiliser une machine virtuelle. Cela a été testé sur une machine ubuntu 22.04 () avec une installation minimale.

Il est nécessaire d'installer docker
> 'sudo apt install docker'

Vous pouvez maintenant suivre les instructions pour une machine avec un serveur X


#### Sur une machine avec serveur graphique X
Assurez vous d'avoir docker installé sur votre machine (tout dépends de votre OS et/ou package manager)

Le dossier contient des scripts shell. Autorisez l'execution de ces fichiers :

> 'chmod +x '*.sh'

Le fichier dockerBuild.sh crée les images docker. La construction de l'une des images a été commentée car le programme semble avoir une fuite de mémoire problématique. Les images sont sous le nom "heat_diffusion" avec le tag :3 pour l'image qui présente le problème de mémoire et le tag :3.1 pour l'image qui fonctionne.

> './dockerBuild.sh'

Il y a deux images donc deux scripts permettant de les lancer. Le script  runNoGIL_old.sh lance l'image gourmande en RAM et il n'est pas recommandé de l'utiliser actuellement et le script runNoGIL.sh lance la bonne image.
Ces scripts ouvrent une connexion locale qui permet au container d'accéder au serveur X de la machine et donc d'avoir une sortie graphique. ATTENTION cela peut poser des problèmes de sécurité car d'autres utilisateurs de la machine en local ont également accès a cette connexion. Les scripts ouvrent cette connexion avant de lancer le container et la ferme à la fin de l'execution du container.

> 'runNoGIL.sh'


# Analyse des résultats

