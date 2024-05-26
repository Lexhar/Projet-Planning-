# Proggrammation d'examens 
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
## Auteurs

Ce projet est réalisé par : 

- TALEB Imane
- EMESSIENE Rachel
- KHATIB Robin
- ABDELATIF Alexandre
- ABDELKRIM Nouha
- BOYELDIEU Matheo 

