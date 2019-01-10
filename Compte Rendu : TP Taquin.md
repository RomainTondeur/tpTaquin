# Fondements de l'intelligence artificielle

*Ronan LAMPE, Romain TONDEUR et Amine MESSAOUDI*



## Compte rendu : TP Taquin

L’objectif consiste à déterminer le nombre minimal de déplacements, nécessaire pour passer d’un taquin quelconque vers un taquin solution. L’objectif final sera de proposer l’étude des taquins 4 × 4.

Vous prendrez soin de la structure de données utilisée et des aspects algorithmiques. Nous vous rappelons que les coûts de calcul deviennent vite prohibitifs, et notamment pour des recherches dites aveugles (Cf. cours).

Nous proposons une étude en 4 étapes, lesquelles seront présentées successivement :



### Etape 1

Le travail demandé est de programmer A∗ et l’algorithme de recherche en coût uniforme. On utilise les heuristiques suivantes :
— $h_0$ : la valeur associée à chaque état est égale à 0
— $h_1$ : pièces mal positionnées
— $h_2$ : distance de Manhattan



### Etape 2

Proposer une adaptation de votre algorithme $A∗$ pour des taquins 4 × 4. Vous développerez également l’algorithme $IDA∗$. Pensez à expliquer son mécanisme dans votre compte-rendu.

Montrer que les heuristiques précédentes ne permettent pas de résoudre certains taquins.

Le choix de l’heuristique est très important pour accélérer la recherche dans l’espace d’états. Plusieurs nouvelles heuristiques ont été proposées dans la littérature. Rechercher dans la littérature une autre heuristique et préciser le défaut habituellement rencontré (montrer que le problème est le temps de calcul des heuristiques).

L’idée est alors de proposer un pré-traitement où les valeurs des taquins sont déjà calculées. Après avoir évalué le nombre de taquins afin de montrer l’impossibilité de mémoriser tous les taquins dans une liste (un tableau ou une base de données). Il suffit alors d’enregistrer un ensemble de taquins partiellement
spécifiés. On parle alors de motifs (des patterns).



### Etape 3

Avant de résoudre les taquins 4 × 4, on s’intéresse ainsi aux taquins partiellement spécifiés. Les cases numérotées et la case vide sont spécifiées (la case représentée par un ’x’ est non spécifiée). Ce taquin est appelé frange (frontière ou encore fringe).

Le travail demandé est le coût réel nécessaire, en utilisant $A∗$ et $IDA∗$ :
— pour passer d’une permutation quelconque d’un taquin frange (un taquin 4 × 4 ordinaire) vers le taquin frange donné
— pour passer d’une permutation quelconque d’un taquin frange (un taquin 4 × 4 ordinaire) vers un autre taquin donné.



### Etape 4

Résolution des taquins – On utilisera les heuristiques $h_0$, $h_1$ et $h_2$ définies précédemment. Pour chaque solution, il est demandé de fournir le nombre de déplacements obtenus dans le cas de taquins non résolus. Nous utiliserons l’exemple donné pour illustrer vos algorithmes.