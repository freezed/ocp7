-[_Parcours Open Classrooms_][oc]-
# [PyDev] Projet 7

## _Note_

_La dernière version à jour de ce document est désormais disponible sur [gitlab](https://gitlab.com/free_zed/ocp7/blob/master/README.md)._

---
## Créez GrandPy Bot, le papy-robot

### Cahier des charges

#### Fonctionnalités

*   Interactions en AJAX : question envoyée en appuyant sur entrée : la réponse s'affiche sans recharger la page.
*   Vous utiliserez l'[API de Google Maps][gmaps] et celle de [Media Wiki][mediawiki]
*   Rien n'est sauvegardé (page rechargée == historique perdu)
*   [option] Plusieurs réponses différentes peuvent être faites

#### Parcours utilisateur

L'utilisateur ouvre son navigateur et entre l'URL que vous lui avez fournie. Il arrive devant une page contenant les éléments suivants :

*   header : logo et phrase d'accroche
*   zone centrale : zone vide (qui servira à afficher le dialogue) et formulaire pour envoyer une question.

L'utilisateur tape dans le champ de formulaire puis appuie sur la touche `entrée` :

> "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"

Le message s'affiche dans la zone du dessus qui affiche tous les messages échangés. Une icône tourne pour indiquer que GrandPy est en train de réfléchir.

Puis un nouveau message apparaît :

>"Bien sûr mon poussin ! La voici : 7 cité Paradis, 75010 Paris."

En-dessous, une carte Google Maps apparaît également avec un marqueur indiquant l'adresse demandée.

GrandPy envoie un nouveau message :

> "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ? La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43 rue de Paradis, la deuxième au 57 rue d'Hauteville et la troisième en impasse. [[En savoir plus sur Wikipedia](https://fr.wikipedia.org/wiki/Cit%C3%A9_Paradis)]"


### Livrables

- [Document texte expliquant la démarche][approach]
    * difficultés rencontrées / solutions trouvées
    * lien _Github_
    * lien du _site déployé_ pour utiliser votre projet en production
    * format pdf n'éxcédant pas 2 pages A4
    * rédigé en anglais ou français
- Code source [dépôt sur _Github_][readme]
- Tableau agile [Project table sur github][kanban]

### Contraintes

* Interface responsive et consultable sur mobile
* Test Driven Development
* Code intégralement écrit en anglais : fonctions, variables et commentaires
* Utilisation d'AJAX pour l'envoi des questions et l'affichage des réponses
* Tests utilisant des mocks pour les API
* Mis en en ligne avec [Heroku][heroku]


[approach]: https://gitlab.com/free_zed/ocp7/blob/master/doc/approach.md
[gmaps]: https://cloud.google.com/maps-platform/?hl=fr "API Google Maps"
[heroku]: https://devcenter.heroku.com/articles/getting-started-with-python
[kanban]: https://github.com/freezed/ocp7/projects/1
[mediawiki]: https://www.mediawiki.org/wiki/API:Main_page/fr
[oc]: https://openclassrooms.com/fr/projects/creez-grandpy-bot-le-papy-robot "Créez GrandPy Bot, le papy-robot"
[readme]: https://gitlab.com/free_zed/ocp7/blob/master/README.md
