# OT_game_tower_defence

**Autor**: Ondrej Smolarik

**Vybraná téma**:
**Obsah**
---
1.Koncept

2.Grafika

3.Dizajn

4.Zvuk

5.Ovládanie

6.Používateľské Rozhranie (UI)

7.Technológie

---
**1. Koncept**
   
Tower Defense je strategická hra, kde hráč musí brániť svoju základňu pred vlnami nepriateľov pomocou staveb veží. Hráč strategicky umiestňuje rôzne typy veží na hraciu plochu, aby zničil prichádzajúcich nepriateľov predtým, než dosiahnu základňu. Cieľom je prežiť všetky vlny nepriateľov v každom leveli a postupovať do vyšších úrovní s rastúcou obtiažnosťou.

Hlavné Ciele:

Strategické plánovanie: Vybrať správne typy veží a ich umiestnenie.

Správa zdrojov: Získavať a efektívne využívať zlato na stavbu a vylepšovanie veží.

Adaptácia: Prispôsobiť sa meniacim sa vlnám nepriateľov a ich typom.

---
**2.Grafika**

2.1 Štýl
2D Grafika: Hra využíva dvojrozmerné grafické prvky, ktoré sú jednoduché a prehľadné.


2.2 Assety
Pozadia: Jemné a nepretržite sa opakujúce sa pozadie, ktoré neodvádza pozornosť od hlavnej akcie.

Cesty: Definované obdlžníky reprezentujúce cesty, po ktorých sa pohybujú nepriatelia.

Veže: Rôzne typy veží (základná, rýchla, sniper) s odlišným vzhľadom a vlastnosťami.

Nepriateľov: Viacero typov nepriateľov s unikátnymi vlastnosťami a animáciami.

Power-Upy: Graficky odlíšené power-upy, ktoré hráč môže zbierať a aktivovať.

**2.3 Implementácia**

Sprite Sheets: Použitie sprite sheets pre animácie nepriateľov.

---
**3.Dizajn**

**3.1 Level Design**

Úrovne: Hra obsahuje viacero levelov, z ktorých každý predstavuje zvýšenú obtiažnosť a nové výzvy.

Cesty: Rôzne cesty pre nepriateľov, ktoré vyžadujú rôzne stratégie na obranu.

Vlny Nepriateľov: Každý level má sériu vĺn nepriateľov s rastúcou obtiažnosťou.

**3.2 Postupovanie**

Level 1: Základné cesty a nepriatelia.

Level 2: Komplexnejšie cesty a zvýšená rýchlosť vĺn.

---

**4. Zvuk**

**4.1 Hudba**

Zvukové Efekty
Stavba Veže: Zvukový efekt pri stavbe veže, ktorý poskytuje audio spätnú väzbu.

Streľba a Zásahy: Zvuky streľby veží a zásahov nepriateľov, ktoré zvyšujú pocit akcie.

---

**5. Ovládanie**

Klávesnica a Myš

Stláčanie Veží:

Kliknutie na Slot veže v HUD: Vyberie typ veže na stavbu.

Stavba Veže:

Kliknutie na Hrací Povrch: Umiestni vybranú vežu na kliknutú pozíciu, ak je to možné.

Aktivácia Power-Upu:

Kliknutie na Slot Power-Upu v HUD: Aktivuje dostupný power-up, ak je k dispozícii.

Ukončenie Hry:

Stlačenie Klávesu ESC: Ukončí hru.

Kliknutie na Krížik Okna: Ukončí hru.

---

**6.Používateľské Rozhranie (UI)**

Heads-Up Display (HUD)

Sloty pre Veže:

Basic Tower Slot:

Pozícia: Ľavý slot.

Zobrazenie: Obrázok základnej veže, cena (50 zlata).

Interakcia: Kliknutie na vybrať a stavbu veže.

Fast Tower Slot:

Pozícia: Stredný slot.

Zobrazenie: Obrázok rýchlej veže, cena (75 zlata).

Interakcia: Kliknutie na vybrať a stavbu veže.

Sniper Tower Slot:

Pozícia: Pravý  slot.

Zobrazenie: Obrázok sniper veže, cena (100 zlata).

Interakcia: Kliknutie na vybrať a stavbu veže.

Power-Up Slot:

Pozícia: Vedľa sniper tower.

Zobrazenie: Počet dostupných power-upov, indikátor aktivity.

Interakcia: Kliknutie na aktiváciu power-upu.

Informácie o Zdrojov:

Gold: Zobrazuje aktuálne množstvo zlata hráča.

Lives: Zobrazuje aktuálny počet životov hráča.

Level a Wave: Zobrazuje aktuálny level a vlna nepriateľov.

**Správy a Notifikácie**

Výpis Správ: Zobrazuje dôležité správy, ako napríklad "Powerup aktivovaný!", "Nedostatok zlata!", "Vyhral si hru!".

Časovač Správ: Správy sú zobrazené na určitú dobu a následne sa automaticky odstránia.

**Vizualizácia Stavov**

Vybraná Veža: Vybraný slot veže je zvýraznený žltým rámčekom, čo indikuje aktuálny výber.

Aktívny Power-Up: Slot power-upu je zvýraznený zeleným rámčekom, keď je power-up aktívny.

---

**7.Technológie**

Programovací Jazyk: Python

Herná Knižnica: Pygame

Grafické Formáty: PNG pre obrázky a sprite sheets

Zvukové Formáty: MP3 pre zvukové efekty a hudbu

---
