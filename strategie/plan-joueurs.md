# CNSNN — plan d'action pour trouver des joueurs (sans dépenser)

Point de départ (14 novembre 2026) : environ 5 téléchargements depuis le 29 octobre, les vidéos font entre 20 et 350 vues, Android sort dans environ 2 semaines.
Idée directrice : **les vidéos donnent de la visibilité, mais ce sont le jeu, la fiche App Store et le bouche-à-oreille qui amènent et gardent les joueurs.**

## 0. Mesurer chaque piste (10 minutes, à faire en premier)

Un lien de campagne App Store par piste, pour savoir laquelle amène des téléchargements (App Store Connect → Analytics → Sources → Campagnes) :

```
https://apps.apple.com/app/apple-store/id6823569042?pt=129627766&ct=SOURCE&mt=8
```

Remplacer `SOURCE` par : `reddit`, `facebook-groupes`, `discord`, `amis`, `presse`, `tiktok`, `instagram`.
Chaque lundi, noter dans un tableau : téléchargements de la semaine, et part « Recherche App Store » / « Référent web » / « Campagnes ».

## 1. La fiche App Store (1 heure, sans code)

C'est là que se décident la plupart des téléchargements : les gens qui cherchent « jeu de mots » doivent te trouver et avoir envie d'installer.

- **Mots-clés** (`Store/app-store-fr.json`, 100 caractères maximum, sans espaces après les virgules). Apple indexe déjà le nom et le sous-titre : inutile de répéter « jeu », « mots », « jour », « défi », « voyelles ». Proposition :
  `consonne,devinette,énigme,mot mystère,lettres,mots fléchés,mots mêlés,vocabulaire,cerveau,quiz,orthographe`
  Ne jamais mettre de marque (Wordle, Motus, Sutom…) : Apple refuse.
- **Première capture d'écran = le hook**, pas un écran de menu : « Tu arrives à lire ça ? » avec une phrase sans voyelles en très gros, puis la réponse sur la 2e capture. Les gens ne voient souvent que les 2 premières dans les résultats de recherche.
- **Texte promotionnel** (modifiable sans mise à jour) : le changer à chaque nouveauté, par exemple « Nouveau : défie tes amis par lien. Le mot du jour, le même pour tous. Gratuit, sans pub. »
- **Événement in-app** (App Store Connect → Événements in-app, gratuit) : il apparaît dans les recherches et sur la fiche. Premier événement possible : « CNSNN arrive sur Android » ou « Semaine spéciale cinéma ».
- **Avis** : la demande d'avis existe déjà dans l'appli. Demander aux premiers joueurs fidèles (amis, testeurs) de laisser une note : sous 5 avis, la fiche paraît vide.

## 2. Le partage dans l'appli (le vrai moteur, à faire dans le code de l'appli)

Le Wordle a grandi presque uniquement grâce au partage des résultats. CNSNN a déjà le partage : il faut qu'il convertisse.

1. **Le lien partagé doit mener à l'App Store, pas au site.** Aujourd'hui le texte se termine par « Jouez aussi : https://cnsnn-9ctosy.web.app » (`App/Views/HomeView.swift`, `invitation`). Mettre une page `/app` qui redirige vers l'App Store (et Google Play une fois Android sorti), et écrire « Jouez aussi à CNSNN (gratuit) : … ». Détails dans `evolutions-app.md`, point 2.
2. **Pousser au partage au bon moment** : juste après avoir trouvé le mot du jour, un bouton bien visible « Défier un ami sur ce mot ».
3. **Parrainage** (plus tard) : un lien d'invitation qui ajoute automatiquement l'ami au classement « Amis ». Détails dans `evolutions-app.md`, point 6.

## 3. Les communautés (30 minutes par semaine, par toi)

Toujours **se présenter comme le créateur**, demander des avis plutôt que « téléchargez », et **lire le règlement** de chaque groupe avant de poster (beaucoup interdisent l'autopromotion hors d'un fil dédié).

- **Groupes Facebook** de jeux de lettres : mots fléchés, mots croisés, mots mêlés, Scrabble, et les joueurs de jeux de mots quotidiens. C'est exactement le public : des gens qui jouent tous les jours.
  Message type : « J'ai créé seul un petit jeu de mots gratuit : chaque jour un mot à retrouver à partir de ses consonnes. Je cherche des joueurs pour me dire ce qu'ils en pensent. Le mot d'aujourd'hui donne ça : CHCRT 😉 »
- **Reddit** : les communautés francophones qui acceptent les projets perso, en général dans un fil dédié. Un post sincère du genre « J'ai développé un jeu de mots quotidien, vos retours ? ».
- **Discord** : serveurs francophones de jeux de mots, d'énigmes ou de culture générale, dans le salon « projets » ou « autopromo ».
- **Forums** : jeuxvideo.com (Blabla), forums de jeux de lettres.

Un lien de campagne différent par communauté (voir le point 0).

## 4. L'entourage (1 fois, puis ça tourne tout seul)

- Créer un **groupe WhatsApp « CNSNN du jour »** avec 10 à 15 amis, famille, collègues : chacun poste son résultat chaque jour (le texte de partage de l'appli est fait pour ça).
- Le **classement « Amis »** de l'appli fait le reste : on revient pour ne pas être dernier.
- Ce sont aussi les **12 testeurs Android** dont Google a besoin.

## 5. La presse et les blogs (gratuit, 1 heure)

Un petit jeu français, gratuit, sans pub, fait par une seule personne : c'est un sujet.

- **Blogs et sites iPhone francophones** (rubriques « applis » ou « bons plans ») : un e-mail court avec le lien, 2 captures, et l'histoire en 3 phrases.
- **Presse locale** de ta ville ou ta région : « un jeune développeur crée un jeu de mots » est un sujet classique.
- Le jour de la sortie Android, renvoyer le même e-mail aux blogs Android.

## 6. Les vidéos (en entretien, pas en moteur)

- **@jeucnsnn** : 2 à 3 vidéos par semaine, publiées à la main, jamais deux fois le même format d'affilée. Commenter chaque jour sous les grosses vidéos d'énigmes et de jeux de mots (de vrais commentaires, pas de pub).
- **Facebook Reels** : republier chaque vidéo (c'est le réseau qui a donné les vues les plus régulières, 220 à 290 sans abonnés).
- **Noah** : lancé le lendemain de la sortie Android, un épisode tous les 2 jours. Tester l'épisode 1 avant, pour vérifier que les gens le regardent jusqu'au bout.

## Le calendrier

| Semaine | À faire |
|---|---|
| **16–22 nov.** | Liens de campagne · fiche App Store (mots-clés, captures, texte promo) · groupe WhatsApp · recruter les 12 testeurs Android · 2 vidéos (L'escalade, Combien de mots) |
| **23–29 nov.** | 3 groupes Facebook + 1 post Reddit ou Discord · lien de partage vers l'App Store dans l'appli · e-mails aux blogs iPhone · test de l'épisode 1 de Noah |
| **Sortie Android** | Vidéo « CNSNN arrive sur Android » · événement in-app · e-mails aux blogs Android · lendemain : Noah épisode 1 |
| **Semaine suivante** | Noah tous les 2 jours · bilan des liens de campagne : on double la piste qui marche, on arrête celle qui ne donne rien |

## Le bon signe à surveiller

Pas les vues : **le nombre de joueurs du mot du jour** (le classement « Aujourd'hui » de l'appli) et **les joueurs qui reviennent le lendemain**. 30 joueurs fidèles qui partagent leur résultat valent plus que 10 000 vues.
