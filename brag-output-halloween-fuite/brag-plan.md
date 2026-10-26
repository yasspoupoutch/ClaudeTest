# CNSNN — Halloween : « La nuit où les voyelles ont disparu »

**Format :** TikTok 1080×1920, 30 i/s, 30 s, avec voix off. **Ton :** conte d'Halloween, fun, néons orange sur nuit violette.

**Concept :** un seul mot du début à la fin. Hook : l'enseigne néon HALLOWEEN ; sur « Ahhh ! » ses voyelles
A, O, E, E sautent dehors et il reste HLLWN — la règle du jeu, montrée sans l'expliquer. Les voyelles s'enfuient
au loin, la caméra les poursuit sur une route pavée qui tourne à gauche puis à droite. Au bout, le téléphone affiche
HLLWN : chaque voyelle retourne dans sa case, HALLOWEEN. Fin : on tape « CNSNN » dans la recherche de l'App Store,
« c'est juste le mot consonne… sans ses voyelles », gratuit.

**Voix off :** Timothée (ElevenLabs) — prise 1 pour les cinq premières répliques, prise 2 pour la dernière
(meilleur « C. N. S. N. N. »). Calée par voice.py, sous-titrée à l'écran ; la musique baisse de 8 dB sous la voix.

**Technique :** vraie perspective (CSS 3D) : la caméra avance de 15 000 px dans la scène, suit les virages de la
route (lacet et roulis), le ciel glisse avec elle ; la route est faite de bandes orientées le long de la courbe.
Rendu en ~20 min.

| Temps | Scène | Voix |
|---|---|---|
| 0–2,4 s | Hook : HALLOWEEN s'allume ; A, O, E, E sautent dehors, l'enseigne grésille : HLLWN. | « Ahhh ! Les voyelles s'échappent ! » |
| 2,4–6,5 s | Elles tremblent puis filent au loin ; la caméra démarre. | « Chaque jour, un nouveau mot… sans ses voyelles. » |
| 6,5–9,5 s | Virage à gauche. « Suis-les… » · « ne les perds pas ! » Chauves-souris. | « Viens nous aider à les retrouver ! » |
| 9,5–12,5 s | Citrouilles géantes gravées FNTM, SRCR, CTRLL, BNBNS, MM. Anneau néon. | |
| 12,5–16,5 s | Virage à droite. « Un mot, » · « sans voyelles… » · « à toi de le trouver ! » | |
| 16,5–20,9 s | Le téléphone : HLLWN. A, O, E, E reprennent leur place : HALLOWEEN. | « Regarde ! Elles retrouvent leur place ! » · « Halloween ! » |
| 20,95–22,15 s | La caméra plonge dans le mot, éclair orange. | |
| 22,15–30 s | CNSNN sous la lune ; « CNSNN » se tape dans la recherche App Store, l'appli apparaît ; CNSNN devient CONSONNE ; « GRATUIT », Obtenir ; @jeuCNSNN. | « Pour jouer, tape C. N. S. N. N. sur l'App Store. C'est juste le mot consonne… sans ses voyelles ! Et c'est gratuit ! » |

**Son :** ré mineur 120 BPM, sous la voix ; boîte à musique au triton, tremblement puis petit rire et souffle pour chaque voyelle qui s'échappe,
rythme pendant la poursuite, souffles calés sur chaque texte et anneau traversé (times.json), un souffle par citrouille gravée,
une cloche par voyelle qui rentre dans le téléphone, tonnerre.

**Données :** l'écran du Mot du jour recréé à l'identique (couleurs, polices, clavier AZERTY aux voyelles dorées) avec HALLOWEEN ; mots d'Halloween gravés sur les citrouilles.
