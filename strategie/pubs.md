# CNSNN — les versions pub de la vidéo « cerveau »

Dossier : `promo-concepts/cerveau-pub/` (sources dans `work/`, rendu : `CUT=15 node render.mjs frames 15 0 450`, son : `python3 make_ad_audio.py 15`).

| Fichier | Durée | Format | Où l'utiliser |
|---|---|---|---|
| `cnsnn-pub-cerveau-6s-9x16.mp4` | 6 s | 9:16 | Snapchat (pubs de 3 à 10 s), Stories, YouTube bumper |
| `cnsnn-pub-cerveau-15s-9x16.mp4` | 15 s | 9:16 | Meta Reels et Stories, TikTok, YouTube Shorts |
| `cnsnn-pub-cerveau-25s-9x16.mp4` | 25 s | 9:16 | TikTok (plus long, plus d'histoire), Reels |
| `cnsnn-pub-cerveau-6s-4x5.mp4` | 6 s | 4:5 | Fil Facebook et Instagram |
| `cnsnn-pub-cerveau-15s-4x5.mp4` | 15 s | 4:5 | Fil Facebook et Instagram |
| `cnsnn-pub-cerveau-25s-4x5.mp4` | 25 s | 4:5 | Fil Facebook et Instagram |

**Écran de fin pub :** CONSONNE, « Le mot du jour. Sans ses voyelles. », icône, badge « Télécharger dans l'App Store »,
« Cherche CNSNN », « GRATUIT · SANS PUB ». Tout reste dans la zone sûre des plateformes (rien à moins de 140 px du bord droit,
où TikTok met ses boutons, ni sous 1 440 px, où sont la légende et le bouton « Installer »), si bien que la même vidéo se
recadre en 4:5 (bande 200–1 550 px).

**Avant de lancer :**
- remplacer `work/badge.svg` (reproduction) par le **badge officiel** « Télécharger dans l'App Store » (noir, fr-FR) à télécharger sur
  https://tools.applemarketingtools.com, puis relancer le rendu (1 minute par version) ;
- vérifier que « Gratuit · sans pub » reste vrai ;
- cibler **iOS uniquement** tant que l'appli n'est pas sur Google Play ;
- texte de la pub : « Tu arrives à lire ça ? 🧠 Un mot sans voyelles chaque jour. Gratuit, sans pub. » ; bouton : « Installer ».
