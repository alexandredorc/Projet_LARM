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

### main.py 

Afin de trouver les bouteilles à l'écran, nous avons décidé d'utiliser la méthode HSV.

Nous avons identifié un domaine de couleur HSV dans lequel ce trouve les couleurs presentent sur les bouteilles oranges, nous définissons une borne supérieur et infeurieur qui va créer un masque à partir duquel on pourra identifier des formes. 

```python
mask=cv2.inRange(image, lo_or, hi_or)
mask=cv2.erode(mask, None, iterations=6)
mask=cv2.dilate(mask, None, iterations=6)
elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
```

parmis toutes les formes nous allons conserver uniquement les formes qui on un certaine aire et à une distance compris entre 30cm et 1m50cm, la forme la plus grande nous donnera la position en pixel de notre bouteille. 

```python
if depth_bottle >= 150 and depth_bottle < 1500 and cv2.contourArea(e)>300:
```

Par la suite nous calculons via les coordonées de la bouteille sur l'image et la profondeur à la quelle le centre de la bouteille ce situe. 

```python
width=43.5*sc_x/640
angle=43.5*(x-640)/640
angle=angle*math.pi/180
return [math.cos(angle) * dist, math.sin( angle ) * dist-35]
```

grâce à cela nous pouvons obtenir la position de la bouteille relative à la caméra. on appliquera une transformer vers le repêre `/map`. 

```python
transfPose = tfListener.transformPose("map", createPose)
```

Une fois les coordonnées de l'objet trouvé, on vérifie que ce n'est pas un objet que l'on connait déjà en comparant leur distance. Si c'est un nouvel objet, on l'ajoute dans la liste. Sinon, on modifie ses coordonnées pour les ajuster. Afin d'éviter les fausses detections, on publie un marker dans `/bottle` uniquement si l'objet a été vu au moins 10 fois.



### marker_pub.py 

c'est un fichier qui contient des fonction nous permettant de manipuler les différents markeur dans rviz.





    



