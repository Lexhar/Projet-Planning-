# Programmation d'examens 
## Description

Ce projet vise à créer un système d'attribution d'examens qui minimise les conflits en utilisant la théorie des graphes et des algorithmes de coloration. Il comprend plusieurs scripts Python pour construire un graphe de conflits, colorier le graphe et assigner des salles aux examens.

Il prend en compte des contraintes dures telles que : 

- La capacité des salles
- Le fait qu'un élève ne puisse pas passer plusieurs examens en même temps
- Le respect d'une plage horaire donnée

## Structure des fichiers

- **utils.py** : Contient des fonctions utilitaires pour construire le graphe de conflits et appliquer l'algorithme de Welsh-Powell.
- **welsh_powell_coloring.py** : Implémente l'algorithme de Welsh-Powell pour la coloration des graphes.
- **assign_rooms.py** : Assigne des salles aux examens en fonction des capacités et des plages horaires disponibles.
- **build_conflict_graph.py** : Construit le graphe de conflits entre les examens.

- **graph_color.ipynb** : Fichier notebook permettant d'exécuter les algorithmes sur une base de données plus petite et de présenter les résultats de manière lisible et compréhensible pour un public.
## Dépendances


Ce projet utilise les bibliothèques suivantes :

- `networkx`
- `pandas`
- `pulp`

Assurez-vous de les installer avant d'exécuter les scripts :

```sh
 pip install networkx pandas pulp
```
## Lancer le projet

Vous pouvez lancer le projet de deux manières : en exécutant`utils.py` ou en utilisant le fichier Jupyter Notebook `graph_color.ipynb`.

### Exécution via `utils.py` 
1. Assurez vous que toutes les dépendances sont installées.
2. Exécutez le script `utils.py` depuis votre terminal :
```sh
python utils.py
```
### Utilisation du fichier Jupyter Notebook
1. Assurez-vous que Jupyter Notebook est installé. Si ce n'est pas le cas, installez-le avec la commande suivante :
```sh
pip install notebook
```
2.  Lancez Jupyter Notebook depuis votre terminal :
```sh
jupyter notebook
```
3. Ouvrez le fichier `graph_color.ipynb` dans Jupyter Notebook
4. Exécutez les cellules du notebook bloc par bloc pour voir les résultats étape par étape.

## Auteurs

Ce projet est réalisé par : 

- TALEB Imane
- EMESSIENE Rachel
- KHATIB Robin
- ABDELATIF Alexandre
- ABDELKRIM Nouha
- BOYELDIEU Matheo 

