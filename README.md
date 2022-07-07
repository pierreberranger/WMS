# Documentation utilisateur  

 

## Premier lancement de l’interface 

Aller dans le terminal et le fichier wms 

Installer tous les outils nécessaires : `Pip3 install –r requirements.txt`

Initialiser la database : `Python3 initialize.py` (crée une database vide) 

Lancer l’interface : `Python3 interface.py`

## Modèle 

- **Package** : paquets dont on peut suivre l’avancement (palettes, …) 

- **Shipment** : ensemble de paquets ayant tous la même destination commandée par Jersey 

- **Dropoff** : ensemble de paquets dans le même camion, caractérisé par une date d’arrivée dans l’entrepôt 

- **Groupage** : ensemble de shipments qui sont livrés au même freight forwarder (transporteur) 

- **Trip** : ensemble de groupages ordonnés dans des conteneurs qui vont faire partie du même voyage en bâteau 

- **Conteneur** : de deux types (les standards et les plus larges) 

## Utilisation en pratique 

  - Vous recevez une commande de différents shipment par un client et/ou freight forwarder 

  - Vous ouvrez l’interface, shipment>declare : tous les paquets sont alors ajoutés à la base de données au statut inbound 

  - Vous apprenez quelles vont être les livraisons et quand des différents paquets vont arriver : vous ajoutez les dropoffs (camions d’arrivage), dropoff>declare 

  - Si on a oublié des paquets on peut toujours modifier les caractéristiques du dropoff, dropoff>update 

  - Pour prévoir l’arrivée des dropoffs vous pouvez visualiser leurs arrivées dans l’ordre chronologique avec view>pdf>incoming 

  - Une fois que le dropoff est arrivé, on le met à jour, dropoff>update>actual_arrival (le statut du dropoff et des paquets est modifié, attention pas du shipment car les paquets d’un même shipment peuvent arriver à l’entrepôt par des camions différents) 

  - Changer le statut du shipment quand tous les paquets sont arrivés, shipment>update>status 

  - Ensuite faire des groupages avec les shipments, groupages>declare 

  - Puis déclarer le voyage voulu avec les groupages, trip>declare 

  - Mettre à jour la base des containers pour en ajouter si besoin, container>add 

  - Demander un plan de chargement du voyage puis confirmer à partir des images, trip>plan_loading 

  - Quand le chargement sur le bâteau est effectué, indiquez-le, trip>load pour mettre à jour les shipments et les packages dans leur status 

  - Vous pouvez obtenir le cargomanifest en allant dans view>pdf>cargomanifest 

  - Quand les colis sont arrivés, vous pouvez changer les status des shipments 

## Fonctionnalités 

En arrivant sur l’interface, on peut choisir si l’on veut rentrer, changer un objet ou si l’on veut visualiser les données. 

**Quit** permet de sauvegarder et de fermer le programme. 

**Ctrl+C** quitte aussi le programme. 

Remarques générales :  

  - Après être rentré dans un des intitulés 

  - **Ctrl+C** permettra de revenir à cette page d’accueil 

  - Les propositions d’entrées sont entre parenthèse, entre crochet est le choix par défaut si on fait Entrer 

  - A chaque création d’objet, l’interface vous renvoie l’id 

 

## Package (add, del, status) 

### Add (One by One, By Reference) 

#### One by One 

On entre les informations demandées, le nombre de paquets qu’on veut ajouter et ses caractéristiques et on valide.  

Description of the package : chaine de caractères 

Length, Width et Height : flottant en cm 

Weight : flottant en kg 

Status, Package Type : à choisir parmi ceux proposés 

#### By Reference 

Donner le nombre de référence, détailler les caractéristiques du paquet (voir Package>Add>OnebyOne) de la référence donnée et indiquer le nombre de paquet à créer avec ces informations. Ou donner l’id d’un paquet sur lequel recueillir les informations et indiquer le nombre de paquets à créer avec ces informations. 

### Del 

Indiquer l’Id du paquet (si on rentre un id qui n’existe pas, l’interface nous donne la liste des id possibles) pui confirmer. 

### Status 

Indiquer l’Id du paquet dont il faut changer le statut, écrire un des statuts possibles donné entre parenthèses et confirmer. 

 

## Shipment (declare, update, del) 

### Declare 

Rentrer les informations demandées sur le shipment  

Adressee : destination client, chaine de caractères 

Departure date from warehouse et delivery date : Année-Mois-Jour Heure:Minutes 

Description : chaine de caractères 

Ensuite, rentrer les paquets One by One comme précédemment ou By Reference. 

## Update (Actual Exit, Status, Add_packages, Del packages, Delivered) 

### Actual_Exit 

Indiquer l’id du shipment à modifier, donner sa date de départ. Les statuts du shipment et des paquets sont changés. 

### Status  

Indiquer l’id du shipment à modifier et le statut voulu. 

### Add_packages  

Indiquer le shipment et ajouter les paquets comme dans Package>Add 

### Del_packages  

Indiquer l’id du shipment et retirer les paquets par leur id 

### Delivered 

Indiquer l’id du shipment et donner la date, cela va changer le statuts des paquets et du shipment. 

### Del 

Donner le nombre de shipments à supprimer puis indiquer l’id du shiment à supprimer  

 

## Dropoff (declare, update, del) 

### Declare 

On entre les informations demandées pour décrire le dropoff, puis on ajoute par leur id les packages (déjà déclarés) et on valide. 

Sender : chaine de caractères 

Arrival date : datetime 

Description of the Dropoff : chaine de caractères 

### Update (arrival_date, add_packages, del_packages, actual_arrival) 

#### Arrival_date 

Si la date d’arrivée du dropoff est changée ou l’heure, on peut la modifiée en indiquant l’id du dropoff et la nouvelle date d’arrivée (ne modifie pas les statuts des objets) 

#### Add_packages 

Indiquer l’id du dropoff et ajouter le nombre de paquets souhaités par leur id. 

#### Del_packages 

Indiquer l’id du dropoff et donner le nombre de paquets à éliminier, puis indiquer leur id. 

#### Actual_arrival 

On entre l’id du dropoff, puis on renseigne la date d’arrivée effective du dropoff dans l’entrepôt. 

La date arrival_date est mise à jour, et les packages ont un statut qui est alors modifié ainsi que le dropoff. 

### Del 

On entre l’id du dropoff, puis le dropoff est supprimé de la datebase. 

 

## Groupage (declare, del) 

### Declare 

On déclare les informations pour décrire le groupage, puis on ajoute par leur id les shipments. 

Freight_forwarder : chaîne de caractères 

### Del 

Indiquer l’id du groupage à supprimer. 

 

## Trip (declare, plan loading, update, del, load) 

### Declare 

On déclare les informations pour décrire le trip, puis on ajoute par leur id les groupages. 

Ship Name : chaine de caractères 

Departure date : datetime 

### Plan loading 

Indiquer l’id du trip, puis le nombre de conteneurs à utilizer sachant ceux qui sont disponibles, les plots s’affichent si cela convient, fermer les plots et valider la proposition dans le terminal (un pdf du plan de chargement est créé dans le fichier output>trip>T…), sinon refuser la proposition dans le terminal après avoir fermé les plots et se diriger vers update. 

### Update 

#### Add_groupage 

Indiquer l’id du trip, le nombre de groupages à ajouter puis leur id. 

#### Del_groupage 

Indiquer l’id du trip, le nombre de groupages à enlever puis leur id. 

### Del 

Indiquer l’id du trip à supprimer. 

### Load 

Indiquer l’id du trip qui a été chargé dans le bateau, les statuts des shipments et packages sont alors changés. 

 

## Container (Add, Del) 

### Add 

Indiquer le nombre de conteneurs à ajouter et choisir pour chaque conteneur s’il s’agit d’un standard ou d’un palet wide. 

### Del 

Indiquer le nombre et les id des conteneurs à supprimer. 

 

## View (List, Details, Pdf) 

### List 

Choisir les objets dont on veut voir les caractéristiques dans la base de données (packages, shipments, groupages, trips, dropoffs) 

### Details 

Choisir l’objet que l’on veut, donner l’id et on a un aperçu en plus de ses informations, des objets qu’ils contiennent. (Shipment, groupages, trips, dropoffs) 

### Pdf 

#### Incoming 

Crée un pdf dans Output de la liste des arrivages dans l’ordre chronologique. 

#### Cargomanifest 

Indiquer le nom du trip, crée un pdf dans Output>Trips>T… 

 

 

 

 

 