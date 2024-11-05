#### Projet Data Scientest sur l'API Ecobalyse
##### Introduction
Ecobalyse est un calculateur permettant de calculer le coût environnemental de produits textiles, 
sur bases de divers paramètres tels que les matières premières, le pays de production, les étapes de fabrications, etc.
La méthode est détaillée dans la documentation d'Ecobalyse. 
Son API ouverte permet à n'importe quel utilisateur ou application de s'intégrer en utilisant des méthodes REST.  

La liste des types de produits (Pantalon, Veste, etc.) proposée par Ecobalyse couvre les principaux vêtements, mais de nombreux types de produits ne sont pas disponibles.

Le but de notre projet est d'étoffer cette liste, et de pouvoir calculer le coût environnemental d'une 
selection beaucoup plus large de produits.

##### Démarche

Etape 1 : Scrapper l'API pour récupérer les listes de paramètres (ou les seuils) acceptables par l'API Ecobalyse
Etape 2 : Envoyer plusieurs milliers de requêtes random à l'API pour constituer une bases de requêtes/réponses.
Etape 3 : A partir de ces données, entraîner un modèle de machine learning, pour déterminer l'influence des divers paramètres (étapes de fabrication, matières, etc.) sur les variables cibles, les variables cibles étant les différents impats environnementaux d'un produit.
Etape 4 : Utiliser l'IA générative pour générer une liste de produits non pris en charge par Ecobalyse, et fournir les étapes de fabrication associées.
Etape 5 : Utiliser le modèle de machine learning sur ces nouveaux produits pour déterminer les 17 impacts environnementaux, et les 2 scores pondérés. Enrichir ainsi la base de données.
Etape 6 : Déploiement du modèle (Docker, Airflow)
Etape 7 : Interface graphique
Etape 8 : Statistiques
