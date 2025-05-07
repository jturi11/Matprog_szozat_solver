# Szózat solver algoritmus
A szózat nevű játékhoz készített megoldó algoritmus.

## Bevezetés

A projektünk célja az volt, hogy kitaláljunk és leprogramozzunk egy algoritmust a Szózat nevű szójátékhoz. A feladatunk az volt, hogy egy olyan programot készítsünk, amely képes hatékonyan játszani a Szózat játékot, azaz adott szabályok mentén új szavakat generálni, érvényes válaszokat adni.

A Szózat játék a népszerű Wordle-hez hasonló magyar változat, ahol a játékosnak egy meg nem nevezett célszót kell kitalálnia 6 próbálkozással. Minden tipp után a rendszer visszajelzést ad: megmutatja, hogy melyik betű van jó helyen (zöld), melyik betű szerepel a célszóban, de rossz helyen (sárga), illetve melyik betű nem szerepel benne egyáltalán (szürke). A játék célja, hogy a játékos minél kevesebb próbálkozásból kitalálja a helyes szót.

## Algoritmus
### 1.lépés:
Első lépésként a megadott magyar-szavak.txt fájlból kellett kigyűjtenünk a 5 betűs szavakat. Itt olyan problémákba ütköztünk, hogy meg kellett különböztetnünk a diftongusokat és a dzs betűt. Az 5 betűs szavak meghatározására szolgál a SzoFilterezes.py nevű program. Ezt csak le kell futtatni, hogy majd a solver algoritmusunk tudja, hogy melyek az elfogadott szavak.


