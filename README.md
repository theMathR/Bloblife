# Bloblife
EN: A game made in Python with pygame about [blobs](https://en.wikipedia.org/wiki/Physarum_polycephalum).

FR: Un jeu fait en Python avec pygame sur les [blobs](https://en.wikipedia.org/wiki/Physarum_polycephalum).

## Rules
Bloblife is a strategy game for 2 players where two blobs fight each other.
To win, you have to be as big as possible.
The game ends when the blob of one of the players is dead or when there is no more food.

The game takes place on a grid:
- The yellow cells correspond to the blob of the first player
- The orange cells correspond to the second player's blob
- The green cells correspond to the bacteria that serve as food
- The blue cells correspond to the mushrooms that also serve as food
- The brighter a cell is, the more blob or food is on it. The maximum is 20.	To see exactly how many blob/food are on a square press Space.

During a turn, the player must plan the movements of his blob.
To do this, he must click on one of the cells from which he wants to move, then click on one of the destination cells in red as many times as the amount of blob he wants to move.
Be careful, moving has a cost of one "blob unit" per cell.
When he has finished, he must press Enter to validate his turn.
To eat food (or his opponent), he simply has to go on it.

Between turns, bacteria and fungi grow. If they are not already at their maximum, their quantity on their cell increases.
At a certain level (17 for bacteria, 20 for fungi) they reproduce:
- For the bacteria, they create other bacteria on the cells next to them if they are not occupied
- Fungi send their spores to 3 random cells. New mushrooms are formed if their cell is not occupied. Fungi reproduce only once.

## Règles
Bloblife est un jeu de stratégie à 2 joueurs où deux blobs se combattent.
Pour gagner, il faut être le plus gros possible.
Le jeu prend fin quand le blob d'un des joueurs est mort ou quand il n'y a plus de source de nourriture.

Le jeu se déroule sur une grille sur lequel:
- Les cases jaunes correspondent au blob du premier joueur
- Les cases oranges correspondent au blob du second joueur
- Les cases vertes correspondent aux bactéries qui servent de nourriture
- Les cases bleues correspondent aux champignons qui servent aussi de nourriture
- Plus une case est claire plus il y a de blob ou de nourriture dessus. Le maximum est de 20. Pour voir précisément la quantité de blob/nourriture sur une case appuyez sur Espace.

Lors d'un tour, le joueur doit planifier les déplacements de son blob.
Pour cela, il doit cliquer sur l'une des cases d'où il veut se déplacer, puis cliquer sur une des cases de destination en rouge autant de fois que la quantité de blob qu'il veut déplacer.
Attention, se déplacer a un coût d'une "unité de blob" par case.
Quand il a fini, il doit appuyer sur Entrée pour valider son tour.
Pour manger de la nourriture (ou son adversaire) il suffit simplement d'aller sur elle/lui.

Entre les tours, les bactéries et les champignons grandissent. S'ils ne sont pas déjà au maximum leur quantité sur leur case augmente.
À un certain niveau (17 pour les bactéries, 20 pour les champignons), ils se reproduisent:
- Pour les bactéries, elles créent d'autres bactéries sur les cases juste à coté si elles ne sont pas occupées
- Les champignons, eux, envoient leur spores sur 3 cases au hasard. De nouveaux champignons se forment si leurs cases n'est pas occupée. Les champignons ne se reproduisent qu'une fois.
