# Szózat solver algoritmus
A szózat nevű játékhoz készített megoldó algoritmus.

## Bevezetés

A projektünk célja az volt, hogy kitaláljunk és leprogramozzunk egy algoritmust a Szózat nevű szójátékhoz. A feladatunk az volt, hogy egy olyan programot készítsünk, amely képes hatékonyan játszani a Szózat játékot, azaz adott szabályok mentén új szavakat generálni, érvényes válaszokat adni.

A Szózat játék a népszerű Wordle-hez hasonló magyar változat, ahol a játékosnak egy meg nem nevezett célszót kell kitalálnia 6 próbálkozással. Minden tipp után a rendszer visszajelzést ad: megmutatja, hogy melyik betű van jó helyen (zöld), melyik betű szerepel a célszóban, de rossz helyen (sárga), illetve melyik betű nem szerepel benne egyáltalán (fekete). A játék célja, hogy a játékos minél kevesebb próbálkozásból kitalálja a helyes szót.

## Algoritmus
### 1.lépés:
Első lépésként a megadott magyar-szavak.txt fájlból kellett kigyűjtenünk a 5 betűs szavakat. Itt olyan problémákba ütköztünk, hogy meg kellett különböztetnünk a diftongusokat és a dzs betűt. Az 5 betűs szavak meghatározására szolgál a SzoFilterezes.py nevű program. Ezt csak le kell futtatni, hogy megkapjuk az otBetusSzavak listát, amit majd a main program megfog hívni.

### 2.lépés:
Második lépésként az algoritmusunknak ki kell találnia, hogy melyik szavat érdemes először tippelni. Ugye ez minden esetben ugyanaz.<br>

Hogyan határozzuk meg a tökéletes szót?<br>

Minden egyes helyiértékre (1,2,3,4,5) minden betűre meghatározzuk, hogy hányszor fordul elő egy betű az adott helyen, és a teljes szószám alapján vesszük a relatív gyakoriságot. Ezek alapján minden szónak kiszámoljuk a "relatívgyakorisági számát" úgy, hogy minden betűjének az adott helyen vett relatív gyakoriságát összeadjuk. A legmagasabb "relatívgyakorisági számú" szót választjuk. Az így kapott szót fogjuk első tippként megadni a Szózat játék során.

### 3. lépés:
A visszajelzés alapján kizárjuk a már nem megfelelő szavakat.
A kizárás során elsőként a zöld betűket, majd a sárgákat, és végül a fekete betűket fogjuk megvizsgálni. (Azért ebben a sorrendben vizsgáljuk meg, mert, ha a fekete alapján vizsgálnánk meg elsőként, akkor előfordulhatna, hogy ha egy olyan szót adtunk meg, amiben van 2 azonos betű, és az egyik zöld a másik fekete, akkor kizárjuk azokat a szavakat, amiben szerepel az a betű, ami nem lenne helyes.) <br>

Zöldek: <br>
- Kiszedjük a szólistából azokat a szavakat, ahol a zöld betű helyén nem a zöld betű van, és a betűt beletesszük a "zöld abc"-be <br>

Sárgák:<br>
- Ha egy betű sárga, de benne van a "zöld abc"-ben, vagy többször is előfordul sárgán (vagy mindkettő), akkor kiszedjük az összes olyan szót, ahol kevesebbszer fordul elő, mint eddig összesen sárgaként és zöldként.
- Ha nem volt zöld, akkor eltávolítjuk az összes olyan szót, ami nem tartalmaz sárga betűt
- Mindneképp eltávolítjuk az összes olyan szót, ahol a sárga betű helyén az a betű szerepel<br>

Fekete:<br>
- Ha egy betű fekete, de benne van a "zöld" vagy "sárga abc"-ben (vagy mindkettőben), akkor pontosan annyiszor kell előfordulnia ahányszor ebben a két "abc"-ben megjelenik. Így kizárjuk az összes olyan szót ahol a betű nem ennyiszer  szerepel.
- Ha a betűnk nem volt zöld/sárga, akkor kitöröljük az összes olyan szót, amiben van ilyen betű.<br>

Ezután megismételjük a 2.lépést a megmaradó szólistából.

## Játék a géppel
Első lépésként mindenféleképpen futassuk le a SzoFilterezes.py-t, hogy a main.py tudja, hogy melyik szavakkal játszon.
Ezután futassuk le a main.py programot, ez magadja nekünk az első tippet, amivel érdemes próbálkoznunk. Ezután a mi feladatunk visszajelzést adni a tippről. Ezt a következőképpen tehetjük meg:  <index>:<szín> formában adjuk meg a válaszünkat, ahol a szín 'f' : fekete, 's' sárga vagy 'z' zöld lehet vesszővel elválasztva. Például: 1:f, 2:s, 3:f, 4:z, 5:f.
Miután megkapta a program a visszajelzésünket, újból ad egy tippet, amire szintén hasonló módon visszajelzést kell adnunk. Ezt addig ismételi, amíg ki nem találja a szót.

## Példa
Több szóra is lefuttatuk az algoritmust, és eddig mindig kitalálta. Például a szöszke szóra is, vagy a játék névadójára, a szózat szóra is. Illetve kipróbáltuk a mai (05.08) szóra is, erre így nézett ki a játék: 
1. tipp: keres, visszajelzés: 1:z, 2:f, 3:f, 4:f, 5:f <br>
2. tipp: kicsal, visszajelzés: 1:z, 2:f, 3:f, 4:f, 5:z <br>
3. tipp: koszol, visszajelzés: 1:z, 2:z, 3:f, 4:f, 5:z <br>
4. tipp: komál, visszajelzés: 1:z, 2:z, 3:z, 4:z, 5:z <br>

Így az algoritmus helyesen kitalálta a "komál" szót is.

