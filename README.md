# grp-orange repository for the UV LARM

https://ceri-num.gitbook.io/uv-larm/

Ce projet à pour but de detecter des bouteilles dans un environnement à l'aide d'une caméra

Pour lancer notre projet, il suffit de lancer le launch 
> roslaunch grp-orange challenge2.launch

Pour traiter les données, nous avons décidé d'utiliser la méthode HSV.

(A toi d'expliquer comment t'a fait la méthode et les params de detection)

Une fois les coordonnées de l'objet trouvé, on vérifie que ce n'est pas un objet que l'on connait déjà en comparant leur distance. Si c'est un nouvel objet, on l'ajoute dans la liste. Sinon, on modifie ses coordonnée pour les ajuster. Afin d'éviter les fausse detection, on publie un marker dans /bottle uniquement si l'objet a été vus au moins 10 fois.

L'ajustement se passe grâce à ce code :

    



