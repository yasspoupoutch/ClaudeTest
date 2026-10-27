# CNSNN — les évolutions de l'appli pour faire venir (et revenir) des joueurs

Analyse faite sur le dépôt `yasspoupoutch/cnsnn` à jour (version 1.2, commit `94c07ab`). Rien n'a été modifié dans ce dépôt :
ce document décrit les changements, avec les fichiers concernés, pour que tu les fasses (ou que tu me demandes de les préparer ailleurs).

## Ce qui est déjà en place (et qui aide beaucoup)

- Publiée sur l'App Store (`id6823569042`), tutoriel de démarrage, demande d'avis dans l'appli, rappel à 12 h, rattrapage classé des
  jours manqués de la semaine, classements jour / semaine / mois / amis, Top 25/50, widget, partage du résultat sans spoiler,
  défis par lien, site référencé sur Google avec le lien App Store et le TikTok.

## Les évolutions, par ordre d'impact

### 1. Mesurer : Firebase Analytics — **priorité 1**, effort : ½ journée

**Pourquoi :** aujourd'hui l'appli n'envoie aucune statistique. Sans mesure, impossible de savoir quelle vidéo ou quelle pub amène
des joueurs, ni s'ils reviennent. C'est le préalable à toute pub payante.

**Quoi :**
- iOS : ajouter le produit `FirebaseAnalytics` à la liste des paquets de `Scripts/generate_project.py` (ligne `for name in ['FirebaseCore','FirebaseAuth','FirebaseFirestore']`), puis régénérer le projet.
- Android : ajouter `firebase-analytics` à `Android/app/build.gradle.kts`.
- Désactiver la collection de l'IDFA (pas de publicité) : clé `GOOGLE_ANALYTICS_IDFA_COLLECTION_ENABLED = NO` dans `Info.plist`, et `GOOGLE_ANALYTICS_ADID_COLLECTION_ENABLED = false` dans le manifeste Android.
- Mettre à jour `App/Resources/PrivacyInfo.xcprivacy`, la fiche « Confidentialité » de l'App Store et `Firebase/hosting/confidentialite.html` (données d'utilisation, non liées à l'identité, sans suivi).
- **Consentement :** en France, la CNIL n'exempte de consentement que les mesures d'audience strictement limitées. À vérifier avant de lancer : soit un écran de consentement simple au premier lancement (avec le tutoriel), soit une configuration exemptée.

**Événements à suivre** (noms courts, sans donnée personnelle) :

| Événement | Quand | Paramètres |
|---|---|---|
| `tutorial_complete` | fin du tutoriel | — |
| `daily_start` / `daily_end` | début et fin du Mot du jour | `found`, `time_s`, `hint` |
| `daily_catchup` | partie de rattrapage | `day_offset` |
| `share_result` | partage du résultat | `mode` |
| `challenge_create` / `challenge_join` | défi créé / rejoint par un lien | — |
| `mode_start` | Classique, Sprint, Survie, Double sens | `mode` |
| `reminder_on` | rappel activé ou heure changée | `hour` |
| `friend_add` | ami ajouté par code | — |

**Ce qu'on regarde ensuite :** les joueurs revenus après 1 jour et après 7 jours, le pourcentage qui termine le tutoriel, qui partage, qui crée un défi.

### 2. Partager vers l'App Store, pas vers le site — effort : 1 heure

**Pourquoi :** le texte partagé dit « Jouez aussi : https://cnsnn-9ctosy.web.app ». Un ami qui clique arrive sur le site, puis doit
encore trouver le bouton App Store. Chaque étape en plus fait perdre des gens.

**Quoi :**
- Créer une page courte `Firebase/hosting/app.html` (servie à `/app`) qui redirige vers l'App Store sur iPhone, vers Google Play sur Android (quand l'appli y sera) et affiche les deux boutons sinon.
- Remplacer `Site.home` par cette adresse dans le texte de partage : `App/Views/HomeView.swift` (`static let invitation = "\nJouez aussi : " + Site.home…`) et `Android/app/src/main/java/com/poupoutch/cnsnn/share/Share.kt`.
- Garder « Jouez aussi » mais ajouter le nom : « Jouez aussi à CNSNN (gratuit) : … ».

### 3. Liens universels pour les défis — effort : ½ journée

**Pourquoi :** sur iPhone, un lien de défi (`/d/CODE`) ouvre la page web, puis il faut toucher « Ouvrir dans CNSNN » (schéma `cnsnn://`). Avec les liens universels, le lien ouvre directement l'appli si elle est installée, et la page web (avec le bouton App Store) sinon.

**Quoi :**
- Publier `Firebase/hosting/.well-known/apple-app-site-association` (sans extension, `Content-Type: application/json`) avec `applinks` → `TEAMID.com.poupoutch.cnsnn` et le chemin `/d/*` ; ajouter l'en-tête dans `Firebase/firebase.json`.
- Ajouter `applinks:cnsnn-9ctosy.web.app` dans `App/CNSNN.entitlements` (capacité « Associated Domains »).
- Dans `App/CNSNNApp.swift`, le `.onOpenURL` existant traite déjà `cnsnn://d/CODE` : lui faire aussi accepter `https://cnsnn-9ctosy.web.app/d/CODE`.
- Android a déjà ses App Links vérifiés.

### 4. Tenir la charge : Firebase Blaze avec une alerte de budget — effort : 15 minutes

**Pourquoi :** sur le plan gratuit Spark, Firestore s'arrête à environ 50 000 lectures et 20 000 écritures par jour (`Docs/PUBLICATION.md`). Une vidéo qui fait 100 000 vues peut amener assez de joueurs pour **bloquer l'appli toute la journée**, au pire moment.

**Quoi :** passer le projet `cnsnn-9ctosy` en Blaze (paiement à l'usage) et créer une **alerte de budget** (par exemple 5 €/mois) dans Google Cloud. À l'échelle actuelle, la facture reste à 0 € ou presque ; seuls les quotas gratuits sont dépassés en cas de pic. Les règles et le code ne changent pas.

### 5. Sortir la version Android — effort : déjà fait côté code, reste la publication

**Pourquoi :** environ un smartphone sur deux en France, et la grande majorité en Afrique francophone (Côte d'Ivoire, Sénégal, Cameroun…), où les jeux de mots en français ont très peu de concurrence.

**Quoi :** compte Google Play (25 $), test fermé de 14 jours avec 12 testeurs (les premiers abonnés TikTok peuvent l'être !), puis publication. Ajouter ensuite le bouton Google Play sur le site et dans la page `/app`.

### 6. Parrainage par le code ami — effort : 1 à 2 jours

**Pourquoi :** le système d'amis existe (code de 6 caractères) mais il faut le saisir à la main. Un lien d'invitation qui ajoute automatiquement l'ami transforme chaque joueur en recruteur, et le classement « Amis » donne une raison de revenir.

**Quoi :**
- Un lien `https://cnsnn-9ctosy.web.app/a/CODE` (même principe que `/d/CODE`, avec la page web, le lien universel et l'App Link Android).
- À l'ouverture : « Léa vous invite. L'ajouter en ami ? » → ajout dans les deux sens.
- Le bouton « Partager mon code » de `App/Views/LeaderboardView.swift` partage ce lien plutôt que le code seul.
- Récompense simple et sans pub : un badge « Ambassadeur » sur le profil, ou un rattrapage supplémentaire.

### 7. App Store : fiche et événements — effort : 1 à 2 heures, sans code

- **Mots-clés** (`Store/app-store-fr.json`) : garder les actuels et ajouter des recherches réelles, par exemple « mot mystère, devinette, lettres manquantes, jeu cerveau, mots cachés ». Ne pas utiliser de marques (Wordle, Motus…) : Apple les refuse.
- **Première capture d'écran = le hook** : « Tu arrives à lire ça ? » avec une phrase sans voyelles, c'est ce qui accroche dans les résultats de recherche.
- **Événements in-app** (App Store Connect) : gratuits, ils apparaissent dans la recherche et sur la fiche. Exemples : « Spécial Noël », « Semaine du cinéma », « Coupe de foot des mots ». Ils peuvent s'appuyer sur des cartes thématiques.
- **Texte promotionnel** (modifiable sans mise à jour) : le mettre à jour à chaque événement.

### 8. Pub payante, une fois le point 1 en place

- **Apple Search Ads** en premier : annonces sur les recherches « jeu de mots », « mot du jour », « mots fléchés ». L'attribution se fait côté Apple (rien à coder pour commencer ; pour aller plus loin, le framework `AdServices` donne un jeton d'attribution gratuit).
- **Meta (Facebook / Instagram)** puis **TikTok Ads** avec les versions pub de la vidéo « cerveau » (`promo-concepts/cerveau-pub/`, en 6 s, 15 s et 25 s, en 9:16 et en 4:5).
- Petit budget de test par vidéo pendant une semaine ; on garde celle qui a le meilleur coût par installation **et** le meilleur retour des joueurs à 7 jours (d'où le point 1).

## Dans quel ordre

1. Semaine 1 : **4** (Blaze, 15 min) et **2** (partage vers l'App Store), puis lancer le planning TikTok.
2. Semaine 2 : **1** (Analytics) et **7** (fiche App Store, premier événement in-app).
3. Semaines 3–4 : **3** (liens universels), **5** (Android), puis **6** (parrainage).
4. Ensuite : **8** (pub payante), avec les mesures du point 1.
