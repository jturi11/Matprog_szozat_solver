# Szózat solver algoritmus
A szózat nevű játékhoz készített megoldó algoritmus.

## Bevezetés

A projektünk célja az volt, hogy kitaláljunk és leprogramozzunk egy algoritmust a Szózat nevű szójátékhoz. A feladatunk az volt, hogy egy olyan programot készítsünk, amely képes hatékonyan játszani a Szózat játékot, azaz adott szabályok mentén új szavakat generálni, érvényes válaszokat adni.

A Szózat játék a népszerű Wordle-hez hasonló magyar változat, ahol a játékosnak egy meg nem nevezett célszót kell kitalálnia 6 próbálkozással. Minden tipp után a rendszer visszajelzést ad: megmutatja, hogy melyik betű van jó helyen (zöld), melyik betű szerepel a célszóban, de rossz helyen (sárga), illetve melyik betű nem szerepel benne egyáltalán (szürke). A játék célja, hogy a játékos minél kevesebb próbálkozásból kitalálja a helyes szót.

## Algoritmus
### 1.lépés:
Első lépésként a megadott magyar-szavak.txt fájlból kellett kigyűjtenünk a 5 betűs szavakat. Itt olyan problémákba ütköztünk, hogy meg kellett különböztetnünk a diftongusokat és a dzs betűt. Az 5 betűs szavak meghatározására szolgál a SzoFilterezes.py nevű program. Ezt csak le kell futtatni, hogy megkapjuk az otBetusSzavak listát, amit majd a main program megfog hívni.

### 2.lépés:
Második lépésként az algoritmusunknak ki kell találnia, hogy melyik szavat érdemes először tippelni. Ugye ez minden esetben ugyanaz. 

Hogyan határozzuk meg a tökéletes szót?

Minden egyes helyiértékre (1,2,3,4,5) minden betűre meghatározzuk, hogy hányszor fordul elő egy betű az adott helyen. Ezek alapján minden szónak kiszámoljuk a "gyakorisági számát" úgy, hogy minden betűjének az adott helyen vett előfordulási számát összeadjuk. A legmagasabb "gyakorisági számú" szót választjuk. Az így kapott szót fogjuk első tippként megadni a Szózat játék során.

### 3. lépés:
A visszajelzés alapján kizárjuk már nem megfelelő szavakat.
A kizárás során elsőként a zöld betűket, majd a sárgákat, és végül a szürke betűket fogjuk megvizsgálni. (Azért ebben a sorrendben vizsgáljuk meg, mert, ha a szürke alapján vizsgálnánk me elsőként, akkor lehet, hogy egy olyan szót adtunk meg, amiben van 2 azonos betű, és az egyik zöld a másik fekete, akkor nem zárhatjuk ki azokat a szavakat, amiben szerepel az a betű.)
Zöldek:
-Kiszedjük a szólistából azokat a szavakat, ahol a zöld betű helyén nem a zöld betű van, és a batűt beletesszük a "zöld abc"-be
Sárgák:
- Ha a sárga, de a betűnk benne van a "zöld abc"-ben, akkor kiszedjük az összes olyat, ahol csak a zöld helyen áll a betű
- Ha nem volt zöld, akkor eltávolítjuk az összes olyan szót, ami nem tartalmaz sárga betűt
- .......
Fekete:
- ......
- Ha a betűnk nem volt zöld/sárga, akkor kitöröljük az összes olyan szót, amiben van ilyen betű.

## Játék a géppel
Első lépésként mindenféleképpen futassuk le a SzoFilterezes.py-t, hogy a main.py tudja, hogy melyik szavakkal játszon.
Ezután futassuk le a main.py programot, ez magadja nekünk az első tippet, amivel érdemes próbálkoznunk. Ezután a mi feladatunk visszajelzést adni a tippről. Ezt a következőképpen tehetjük meg: 
