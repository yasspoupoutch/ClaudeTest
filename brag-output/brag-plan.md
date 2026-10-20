# CNSNN — plan de la vidéo /brag

**Format :** vertical TikTok 1080×1920, 30 i/s, 21 s.
**Ton :** premium et joueur. Le design de l'appli (nuit, verre, or), avec du rythme et un petit jeu pour le spectateur.

## L'appli en une phrase
CNSNN est un jeu de mots iPhone/Android : on voit un mot privé de ses voyelles et on doit le retrouver le plus vite possible.
Pour qui : les amateurs de jeux de mots du quotidien (Wordle, Le Mot) qui veulent se mesurer à leurs amis.

## Angle
Le spectateur joue avant de comprendre. On ouvre sur « SRR » et une question. Il cherche, puis la vidéo
lui donne la réponse avec l'animation emblématique de l'appli : les voyelles dorées qui glissent entre les consonnes.
La chute reprend le même geste sur le nom : CNSNN devient CONSONNE.

- **Accroche :** « SRR » en très grand. « Trouverez-vous les voyelles ? » (le texte de l'image de partage de l'appli)
- **Points forts :** 1) une vraie partie du Mot du jour, 2) le même mot pour tous, avec un classement, 3) les modes Sprint, Survie et Double sens.
- **Chute :** CNSNN devient CONSONNE, puis « Retrouvez le mot. Sans ses voyelles. »
- **Légende de partage :** voir `share-copy.txt`.

## Identité visuelle (reprise du code : App/DesignSystem/Theme.swift, Firebase/hosting/style.css)
- Fond #06070C → #121426, halos violet (#593EC7) et bleu-vert (#007D86) qui dérivent lentement.
- Or des voyelles #FFC65A (dégradé #FFD673 → #F6B84D), menthe #5AE6C6, rouge #FF8785.
- Polices : Instrument Serif (consonnes, indices en italique), Fraunces Black (logo), Inter (à la place de la police système iOS).
- Cartes en verre : dégradé blanc 14 % → 5 %, bordure 16 %, reflet en haut.
- Clavier AZERTY avec voyelles dorées, révélation des voyelles avec rebond et halo doré.

## Storyboard
| # | Temps | Scène |
|---|---|---|
| 1 | 0,0–2,8 s | **Accroche.** « SRR » géant en Instrument Serif. En dessous, en italique doré : « Trouverez-vous les voyelles ? » |
| 2 | 2,8–6,9 s | **La partie.** « SRR » rejoint sa place sur le plateau du Mot du jour (barre du haut, chrono qui tourne, clavier AZERTY). Appui sur « Indice » : « On le voit sur mon visage. » Saisie S-O-U-R-I-R-E (voyelles en or), puis « Valider ». |
| 3 | 6,9–9,8 s | **Résultat.** La feuille de résultat monte. « Trouvé en 0:12. » Les voyelles glissent dans SRR → SOURIRE avec le halo doré. Cases temps / indice / série, puis « Top 5 % · 3e sur 120 aujourd'hui ». |
| 4 | 9,8–12,8 s | **Le même mot pour tous.** Titre « Un mot par jour. Le même pour tous. » Le classement du jour apparaît ligne par ligne, « Vous » mis en avant. |
| 5 | 12,8–17,0 s | **Les modes**, trois cartes rapides : Sprint (90 s, combo ×5), Survie (3 vies), Double sens (FRN → FARINE ou FREIN ?). |
| 6 | 17,0–21,0 s | **Chute.** « CNSNN » en Fraunces Black, les voyelles tombent en or → CONSONNE. « Retrouvez le mot. Sans ses voyelles. » · « Gratuit, sans publicité. » |

## Son
Une piste synthétisée pour cette vidéo, en la mineur à 120 BPM (Am–F–C–G). L'accroche ne garde qu'une nappe et un arpège,
le rythme démarre avec la partie. Les touches du clavier sont de légers clics, les voyelles révélées sont des notes de cloche
dans la gamme du morceau (la, do, ré, mi), et le logo final se termine sur un accord qui résonne.

## Données
Mot, indice et exemple de classement (« 3e sur 120 ») viennent du site et du README. Les prénoms du classement
(Léa, Malik) sont fictifs. Aucune donnée réelle de joueur, aucune clé ni configuration Firebase n'est utilisée.
Le dépôt CNSNN a seulement été lu : rien n'y a été modifié.
