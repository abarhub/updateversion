# updateversion

Permet de mettre à jour la version du pom maven.
Pour l'utiliser, il faut lancer la commande en ettant dans le répertoire du pom.
S'il y a des sous modules, ils sont modifiés aussi avec la même version.

Le programme propose de monter la version de chaque composant. Par exemple, si la version du pom est 0.0.1-SNAPSHOT, 
le programme va proposer de mettre les version suivantes :
```shell
1) version=1.0.0-SNAPSHOT
2) version=0.2.0-SNAPSHOT
3) version=0.1.1-SNAPSHOT
4) autre
0) quitter
```
Le choix 4 permet de saisir la valeur que l'on souhaite. Le '-SNAPSHOT' est ajouté pour toutes les versions.

