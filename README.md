# Alphsistant Code 



### Travaux pour finir la démo fin novembre 

* Le lien modèle DL -> blender est à peu près fonctionnel mais il manque quelques éléments 
* Générer les faces sur le visage
    * À mon sens, le plus simple est de le faire à la main et d'enregistrer le résultat dans un fichier csv qu'on lira pour regénérer le maillage à chaque init 
    * Attention: la tesselation du modèle DL fait qu'on a des tri au lieu de quads. Mais no sweat, blender permet de convertir facilement les tris en quads (Alt + J en mode edit)
* Vérifier que les axes sont cohérents (je pense qu'il faut inverser y et z)
* Éventuellement réflechir à un offset ou un scaling factor pour que la démo soit sexy à travers la caméra 


### Blender folder: 

Scripts created in the path for proto 0. In dire need of comments ;) 


### Biblio

* https://lgg.epfl.ch/publications/2015/Sofien_Thesis/thesis.pdf

