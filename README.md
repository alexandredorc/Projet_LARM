# grp-orange repository for the UV LARM

https://ceri-num.gitbook.io/uv-larm/

Ce projet à pour but de detecter des bouteilles dans un environnement à l'aide d'une caméra

Pour lancer notre projet, il suffit de lancer le launch 
> roslaunch grp-orange challenge2.launch

Attention : Pour lancer le rosbag, il faut lancer aussi sa clock.    
    
    rosbag play --clock [nom du rosbag]

# Composition du package

> scripts : Nous utilisons 2 scripts, le principal *main* et un spécifiquement pour la création de message comme les markers

> rviz : contient la map paramatré de rviz

> launch : contient le launch lançant l'ensemble de notre projet

# Explication du code

Pour traiter les données, nous avons décidé d'utiliser la méthode HSV.

(A toi d'expliquer comment t'a fait la méthode et les params de detection)

Une fois les coordonnées de l'objet trouvé, on vérifie que ce n'est pas un objet que l'on connait déjà en comparant leur distance. Si c'est un nouvel objet, on l'ajoute dans la liste. Sinon, on modifie ses coordonnées pour les ajuster. Afin d'éviter les fausses detections, on publie un marker dans `/bottle` uniquement si l'objet a été vu au moins 10 fois.

    



