# CNSNN — trois concepts de promo TikTok (hors Halloween)

| Vidéo | Fichier | Durée | Idée |
|---|---|---|---|
| Ton cerveau sait lire sans voyelles | `cerveau/cnsnn-cerveau.mp4` | 24 s | Hook « Tu arrives à lire ça ? » sur une phrase sans voyelles, puis niveau 2 et niveau expert (PISSENLIT, vraie carte) avec 3 s au chrono. |
| Seuls les vrais fans de foot | `foot/cnsnn-foot.mp4` | 24 s | Stade de nuit ; trois vraies cartes Football : CARTON JAUNE (facile), MARADONA (moyen), LIZARAZU (difficile). « T'en as trouvé combien ? » |
| Le duel | `duel/cnsnn-duel.mp4` | 23,5 s | Léa contre Malik sur le même mot (CASSOULET) : Malik se trompe, Léa trouve en 0:38, Malik en 0:41 ; classement et « Défier un ami ». |

Les trois finissent sur le même écran : CNSNN tapé dans la recherche App Store, l'appli en résultat, CNSNN devient
CONSONNE, « GRATUIT », @jeuCNSNN (common/kit.js).

**Technique :** HTML/CSS animé image par image (Playwright), musique synthétisée (synth.py), rendu en moins d'une minute
par vidéo. `common/` contient les éléments partagés : écran de jeu de l'appli, cases des voyelles, chrono circulaire,
écran de fin et ses sons. Chaque `*/work/` en a une copie, et `node render.mjs frames <durée>` le rend.

**Voix off :** chaque dossier a son `voix.txt` (texte ElevenLabs + placement) ; une fois la voix reçue, elle se cale
et la musique baisse dessous, comme pour la vidéo Halloween, sans refaire le rendu des images.
