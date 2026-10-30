# CNSNN — planning TikTok sur 30 jours (28 octobre → 26 novembre 2026)

Compte : **@jeucnsnn**. Chaque vidéo est aussi publiée en **Reels** (Instagram) et en **Shorts** (YouTube), même fichier.

## Le quota Metricool gratuit (règle : zéro euro)

- **20 publications par mois**, et une vidéo envoyée sur 3 réseaux en compte 3. Le compteur repart à zéro le 1er du mois.
- Répartition : **TikTok en priorité** (une vidéo tous les 2 jours environ), **Instagram seulement pour les meilleures** (3 à 5 par mois), **Facebook jamais via Metricool**. Les Reels Instagram sont repartagés sur la Page Facebook par le réglage gratuit d'Instagram (« Partager aussi sur Facebook »).
- Novembre : 7 TikTok + 3 Instagram du 1er au 7, soit 10 ; il reste 10 publications pour le 8 au 30 (8 TikTok + 2 Instagram).

## Les règles du jeu

- **Une vidéo par jour, à heure fixe.** La régularité compte plus que la perfection : l'algorithme et les abonnés prennent l'habitude.
- **Heures de publication de départ : 12 h 15 en semaine, 18 h 30 le week-end** (les joueurs de jeux de mots jouent à la pause déjeuner et le soir ; le rappel de l'appli tombe à 12 h). À ajuster après 2 semaines avec les statistiques TikTok (onglet « Audience »).
- **Jamais le vrai Mot du jour** : tous les mots ci-dessous viennent des cartes Classique (`Shared/cards.tsv`), que le workflow Firebase garantit différentes des mots du jour secrets.
- **Toujours 3 secondes et une question** : la vidéo s'arrête sur une question qui fait commenter (« Ton temps ? », « T'as trouvé ? »). Épingler un commentaire qui donne la réponse… 1 h après la publication.
- **Répondre aux commentaires en vidéo** au moins 2 fois par semaine (fonction « répondre avec une vidéo ») : c'est ce qui fait monter un compte.
- **Légende type :** une phrase d'accroche, « Tape CNSNN sur l'App Store (gratuit) », 4 ou 5 hashtags.
  Hashtags de base : `#jeudemots #motdujour #quiz #cerveau #cnsnn` (+ un hashtag du thème : `#football`, `#cinema`, `#geographie`, `#animaux`).
- **Lien App Store dans la bio** de TikTok et d'Instagram : https://apps.apple.com/app/id6823569042

## Les formats

| Code | Format | Durée | Modèle déjà prêt |
|---|---|---|---|
| **A** | **« 3 secondes pour trouver »** : un mot sans voyelles, son indice, un chrono de 3 s, la réponse | 8–12 s | `brag-output-quiz` (un seul mot) |
| **B** | **« Tu arrives à lire ça ? »** : une phrase sans voyelles, puis un mot expert | 15–25 s | `promo-concepts/cerveau` |
| **C** | **« Seuls les vrais fans »** : 3 mots d'une catégorie, facile → difficile | 20–25 s | `promo-concepts/foot` |
| **D** | **Duel** : deux joueurs, même mot, qui gagne ? « Tag ton adversaire » | 20 s | `promo-concepts/duel` |
| **E** | **Coulisses** : « Je développe seul un jeu de mots », une nouveauté de l'appli, un chiffre | 20–40 s, face caméra ou écran | à filmer par toi |
| **F** | **Pub rediffusée** : une des vidéos déjà faites | — | voir la colonne « Fichier » |

## Le calendrier

| Date | Format | Contenu | Consonnes → réponse | Indice (de la carte) |
|---|---|---|---|---|
| mer. 28 oct. | F | Halloween « Les voyelles s'échappent » | HLLWN → HALLOWEEN | `brag-output-halloween-fuite/brag.mp4` |
| jeu. 29 oct. | B | Ton cerveau sait lire sans voyelles | — | `promo-concepts/cerveau/cnsnn-cerveau.mp4` |
| ven. 30 oct. | F | Halloween quiz « 3 mots qui font peur » | RGN, BRLLRD, NSFRT | `brag-output-halloween/brag.mp4` |
| sam. 31 oct. | A | Spécial Halloween | LNTRN → LANTERNE | Une lampe d'autrefois qu'on porte à la main. |
| dim. 1 nov. | E | « J'ai codé seul un jeu de mots : voilà comment il marche » (écran de l'appli, tutoriel TR → TROU / AUTEUR) | — | — |
| lun. 2 nov. | A | Facile pour lancer la semaine | HMSTR → HAMSTER | Un petit rongeur qui court dans sa roue. |
| mar. 3 nov. | C | Seuls les vrais fans de foot | voir `promo-concepts/foot` | (rediffusion) |
| mer. 4 nov. | A | Moyen | TBGGN → TOBOGGAN | On glisse dessus au parc. |
| jeu. 5 nov. | D | Le duel | C_SS__L_T → CASSOULET | `promo-concepts/duel/cnsnn-duel.mp4` |
| ven. 6 nov. | A | Difficile | MRTN-PCHR → MARTIN-PÊCHEUR | Un petit oiseau bleu vif qui plonge pour attraper les poissons. |
| sam. 7 nov. | C | **Nouveau** : seuls les vrais cinéphiles | L CRND, FGHT CLB, MN VSN TTR | Le Corniaud · Fight Club · Mon voisin Totoro |
| dim. 8 nov. | E | « Le classement de la semaine : qui est n°1 ? » (capture du classement, sans pseudos privés) | — | — |
| lun. 9 nov. | B | **Nouvelle** phrase : « T S PS CRNT T LR » ? | T ES PAS CERTAIN DE LIRE ? (phrase libre) | puis mot expert |
| mar. 10 nov. | A | Facile | BBRN → BIBERON | Le bébé y boit son lait. |
| mer. 11 nov. | A | Moyen (11 novembre) | VRST → EVEREST | Le plus haut sommet du monde. |
| jeu. 12 nov. | C | **Nouveau** : seuls les vrais géographes | PRVNC, TLNTQ, BDPST | Provence · Atlantique · Budapest |
| ven. 13 nov. | A | Difficile | NTRCTQ → ANTARCTIQUE | Le continent glacé du pôle Sud. |
| sam. 14 nov. | F | Pub 3D « CHOUCROUTE » | CHCRT → CHOUCROUTE | `promo-3d/cnsnn-promo-3d.mp4` |
| dim. 15 nov. | E | Réponse en vidéo aux meilleurs commentaires de la semaine | — | — |
| lun. 16 nov. | A | Facile | RVL → RÉVEIL | Il sonne le matin. |
| mar. 17 nov. | A | Moyen | LMRN → LÉMURIEN | Un primate de Madagascar aux grands yeux. |
| mer. 18 nov. | C | **Nouveau** : seuls les vrais amis des bêtes | DNSR, PCRN, CT | Dinosaure · Puceron · Coyote |
| jeu. 19 nov. | A | Difficile | BBLTHCR → BIBLIOTHÉCAIRE | Il prête les livres et les range sur les rayons. |
| ven. 20 nov. | D | Duel « en vrai » : toi contre un ami, filmé à l'écran (format E + D) | — | — |
| sam. 21 nov. | A | Moyen | BRB  PP → BARBE À PAPA | Un nuage de sucre filé sur un bâton. |
| dim. 22 nov. | E | « 1 mois de CNSNN : ce que j'ai appris / les chiffres » | — | — |
| lun. 23 nov. | B | Phrase + mot expert | (phrase libre) → CSSLT CASSOULET | Des haricots blancs et des saucisses… |
| mar. 24 nov. | A | Facile | STL → STYLO | On écrit avec, à bille ou à plume. |
| mer. 25 nov. | C | Seuls les vrais fans de foot, épisode 2 | GRDNS, XPLSN, RTRN CRBTQ | Gradins · Expulsion · Retourné acrobatique |
| jeu. 26 nov. | A | Difficile | QBRN → QUIBERON | Une presqu'île bretonne à la côte sauvage. |

Pour les vidéos en pub payante, les épisodes « vrais fans » doivent éviter les noms de personnes réelles (Maradona, Lizarazu…) ; en organique c'est moins sensible, mais l'épisode 2 du foot ci-dessus n'en utilise déjà plus.

## Ce que je peux produire

Les formats **A, B, C et D** se fabriquent avec les modèles existants en **moins d'une minute de rendu chacun**. Il suffit de me dire « produis la semaine 1 » (ou les 4 semaines) : je génère toutes les vidéos de la période, nommées par date, avec leur légende. Les **E** sont à filmer par toi (c'est ce qui crée le lien avec les abonnés).

## Ce qu'il faut regarder chaque semaine

| Indicateur | Où | Bon signe |
|---|---|---|
| Durée de visionnage moyenne, % de vidéo regardée en entier | TikTok Studio | > 50 % regardée en entier sur les formats A |
| Commentaires et partages par vidéo | TikTok Studio | les formats qui font commenter → en faire plus |
| Visites de profil, clics sur le lien en bio | TikTok Studio | monte avec les abonnés |
| Téléchargements par jour, sources (« Référent web », « Recherche App Store ») | App Store Connect → Analytics | les pics suivent les vidéos qui marchent |
| Joueurs du jour (Mot du jour) | classement « Aujourd'hui » dans l'appli (« 3e sur 120 ») | le nombre de joueurs quotidiens qui monte |

## Leçons des premières semaines (à appliquer aux prochaines vidéos, sans refaire les anciennes)

- Les quiz simples faits par le créateur (un mot, consonnes énormes, indice, barre de temps) ont fait 271 à 944 vues sur TikTok ; les vidéos plus travaillées : Halloween 352, « cerveau » 20.
- Garder la police du jeu, mais : un seul mot lisible dès la vignette, consonnes très grandes, défi à l'écran dès la première image, fin courte « Tape CNSNN sur l'App Store ».
- Code de campagne App Store : `pt=129627766` (liens : `https://apps.apple.com/app/apple-store/id6823569042?pt=129627766&ct=<source>&mt=8`).
- Compte TikTok personnel : le passage en compte pro demande une entreprise vérifiée, donc pas de stats TikTok dans Metricool ni de lien cliquable avant 1 000 abonnés.
