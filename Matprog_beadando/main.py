from collections import defaultdict
from os.path import split
from typing import List, Dict
from SzoFilterezes import *

# Ez az osztály egyetlen visszajelzést reprezentál a Szózatjátékból, azaz egy adott betű helyét és színét (visszajelzését) tárolja egy próbálkozásban.
class Valasz:
  # Konstruktor, ami egy "<index>:<szin>" formátumú stringből hozza létre az objektumot. Tehát például a "1:f" válaszrészletből index=0 (0-alapú), szin='f' (fekete) lesz.
  def __init__(self, index: int, szin: str, betu:str):
    self._index = index
    self._szin = szin
    self._betu = betu

  def __init__(self, repr: str):
    split = repr.split(':')
    self._index = int(split[0].strip())-1 # Indexet 0-tól fogjuk számolni, de a bemenet 1-től megy, ezért ki kell egyet vonni.
    self._szin = split[1].strip() # "z", "s" vagy "f" lehet.

# Visszaadja a betű helyét a szóban (0-tól indul)
  @property
  def index(self):
    return self._index

 # Visszaadja a visszajelzés színét ('z', 's' vagy 'f')
  @property
  def szin(self):
    return self._szin

# Visszaadja a betűt, amelyhez a visszajelzés tartozik (utólag beállítható a megadBetu által).
  @property
  def betu(self):
    return self._betu

# Beállítja a betűt az objektumban (pl. a tippelt szó adott betűjét)
  def megadBetu(self, betu: str):
    self._betu = betu

# Visszaadja, hogy a visszajelzés zöld-e
  def zold(self) -> bool:
    return self._szin == 'z'

# Visszaadja, hogy a visszajelzés sárga-e
  def sarga(self) -> bool:
    return self._szin == 's'

# Visszaadja, hogy a visszajelzés fekete-e
  def fekete(self) -> bool:
    return self._szin == 'f'

# <index>:<szín>:<betű> formában kíírja a visszajelzés alapján, amit tudunk.
  def __repr__(self):
    return f'{self._index}:{self._szin}:{self._betu}'

# A játékban használt szavak hossza.
karakterLimit = 5

# A bemenetként kapott visszajelzés stringet ("1:f, 2:s, ...") átalakítja egy Valasz objektumokat tartalmazó listává, amelyek tartalmazzák az indexet, a visszajelzés színét és a tippelt szó megfelelő betűjét.
def bemenetKonvertalas(tipp: List[str], bemenet: str) -> List[Valasz]:
  # tipp: jelenleg tippelt szó betűinek listája.
  # bemenet: általunk adott visszajelzés.
  split = bemenet.split(',')
  valaszok = list()
  for s in split:
    valasz = Valasz(s) # Létrehozzuk a Valasz objektumot az adott részletből
    betu = tipp[valasz.index] # Kikeressük a tippelt szó megfelelő betűjét
    valasz.megadBetu(betu) # Beállítjuk a Valasz objektumban a betűt
    valaszok.append(valasz) # Hozzáadjuk a válaszok listájához
  return valaszok
# Visszakapunk: Valasz objektumok listája, melyek tartalmazzák a pozíciót, színt és betűt.

# Egy adott karakter előfordulási gyakoriságát tárolja, az épp aktuális szólistára nézve.
class KarakterGyakorisag:
  def __init__(self, karakter: str, aboszolutGyakorisag: int, populacio: int):
    self._karakter = karakter
    self._abszolutGyakorisag = aboszolutGyakorisag
    self._populacio = populacio
    
  # Visszaad egy stringet, ami a karaktert és annak relatív gyakoriságát mutatja
  def __repr__(self):
    return f'{self._karakter}:{self.relativGyakorisag()}'

  # Kiszámolja és visszaadja a karakter relatív gyakorliságát a populációhoz képest
  @property
  def relativGyakorisag(self):
    return self._abszolutGyakorisag / self._populacio

  # Visszaadja a karaktert
  @property
  def karakter(self):
    return self._karakter

class Megoldo:

# Megadja még melyik szavak lehetséges emgoldások.
  def __init__(self, szavak=List[List[str]]):
    self._lehetsegesSzavak = szavak # Megadja melyik szavak potenciális megoldások. (Ez egy lista, amelyben minden szó listaként van tárolva.)
    self.feketek = list()
    self.sargak = list()
    self.zoldek = list()
# Megadja a még lehetséges szavak számát.
  def szavakSzama(self) -> int:
    return len(self._lehetsegesSzavak)

# Megszámolja, hogy az adott indexű pozícióban milyen gyakran fordulnak elő az egyes karaktereka megadott szavak listájában
  def indexbeliGyakoriság(self, szavak: List[List[str]], index: int) -> Dict[str, int]:
    dict = defaultdict(int) # Szótárban tároljuk el az adott betűk adott helyen vett gyakoriságát
    for szo in szavak: # Végigmegyünk a szólistán.
      karakter = szo[index] # Megnézzük a rögzített indexen milyen karakter van a szóban.
      dict[karakter] = dict[karakter] + 1 # A talált karakter előfordulásainak számát eggyel növeljük.
    return dict
  
# Kiválasztja a legjobb szót a jelenlegi lehetséges szavak közül. A kiválasztás alapja, hogy minden szó esetén kiszámolja az egyes betűk helyi előfordulási gyakoriságát, majd ezek összegét veszi "gyakorisági számként". A legmagasabb összegű szó lesz a legjobb tipp.
  def legJobbSzo(self) -> {List[str], int}:
   # Létrehozunk egy listát, amely minden pozícióra (0-4) tartalmazza az adott pozícióban előforduló betűk gyakoriságát a jelenlegi lehetséges szavak között.
    indexBeliGyakorisagok = list()
    # Meghívjuk az indexbeliGyakoriság metódust, amely visszaad egy szótárt, hogy az i-edik pozícióban milyen betűk és milyen gyakorisággal fordulnak elő.
    for i in range(0, 5):
      indexBeliGyakorisagok.append(self.indexbeliGyakoriság(self._lehetsegesSzavak, i))
      legjobbSzo = None #Legjobb szó betűlistaként.
      legjobbSzoGyakorisag = 0 #A legjobb szóhoz tartozó gyakorisági érték.

# Végigiterálunk az összes jelenleg lehetséges szón, hogy kiválasszuk azt, amelyik a legmagasabb "gyakorisági értékkel" rendelkezik.
    for szo in self._lehetsegesSzavak:
      szoErtek = 0 # A szó értékét itt számoljuk ki, azaz az összes betű helyi gyakoriságának összegét.
      karakterIndex = 0
      while karakterIndex < karakterLimit:
        karakter = szo[karakterIndex] # Az aktuális betű a szóban
        indexbeliGyakorisag = indexBeliGyakorisagok[karakterIndex] # Az adott pozíció betűgyakoriságai
        abszolutGyakorisag = indexbeliGyakorisag[karakter] # Az adott betű előfordulási száma az adott pozícióban
        szoErtek += abszolutGyakorisag # Hozzáadjuk a szó értékéhez

 # Ha a jelenlegi szó értéke nagyobb, mint a korábbi legjobb szó értéke, akkor frissítjük a legjobb szót és annak értékét.
        if legjobbSzoGyakorisag < szoErtek:
          legjobbSzo = szo
          legjobbSzoGyakorisag = szoErtek
        karakterIndex += 1
# Visszaadjuk a legjobb szót és annak gyakorisági értékét.
    return legjobbSzo, legjobbSzoGyakorisag
    
  # A következő függvénnyel a kapott válasz alapján kizárjuk a már nem lehetséges szavakat.
  def valaszFeldolgozas(self, valaszok: List[Valasz]):
    zoldek = list()
    sargak = list()
    feketek = list()
    # Az új válaszban szereplő betűket színük alapján 3 listába szedjük.
    for valasz in valaszok:
      if valasz.zold():
        zoldek.append(valasz)
      elif valasz.sarga():
        sargak.append(valasz)
      elif valasz.fekete():
        feketek.append(valasz)
        
    # Kizárunk minden olyan szót a lehetséges szavak listájából, ahol egy kapott zöld betű helyén nem az a betű szerepel.
    for zold in zoldek:
      index = 0
      while index < len(self._lehetsegesSzavak):
        vizsgaltSzo = self._lehetsegesSzavak[index]
        vizsgaltBetu = vizsgaltSzo[zold.index]
        if vizsgaltBetu == zold.betu:
          index += 1 # a megmaradt szólistában is egymást követik így az indexek
        else:
          self._lehetsegesSzavak.pop(index)

    for sarga in sargak:
      index = 0
      # A sárga helyen nem lehet az a betű, kizárjuk azokat a szavakat, ahol ott van.
      betu = sarga.betu
      while index < len(self._lehetsegesSzavak):
        vizsgaltSzo = self._lehetsegesSzavak[index]
        vizsgaltBetu = vizsgaltSzo[sarga.index]
        if vizsgaltBetu == betu:
          self._lehetsegesSzavak.pop(index)
        else:
          index += 1
          
      # a sárgák + zöldek száma >= a betű előfordulása a szóban, kizárjuk a szavakat ahol ez nem teljesül
      # tehát kizárjuk ahol nincs a sárga betű vagy kevesebbszer fordul elő, mint kén
      index = 0
      while index < len(self._lehetsegesSzavak):
        vizsgaltSzo = self._lehetsegesSzavak[index]
        countLimit = 0  # adott sárga betű eddigi ismert előfordulását számoljuk
        for zold in zoldek:
          if zold.betu == betu:
            countLimit += 1 # ez a betű zöld-e egy másik helyen
        for sarga2 in sargak:
          if sarga2.betu == betu:
            countLimit += 1 # ez a betű sárga-e egy másik helyen is
        count = vizsgaltSzo.count(betu)
        if count < countLimit:
          self._lehetsegesSzavak.pop(index)
        else:
          index += 1

    # Ha egy betű fekete, akkor pontosan annyiszor szerepelhet ahányszor eddig sárgaként vagy zöldként szerepel
    # Kizárjuk azokat a szavakat ahol nem ennyiszer szerepel a fekete betű
    for fekete in feketek:
      index = 0
      while index < len(self._lehetsegesSzavak):
        vizsgaltSzo = self._lehetsegesSzavak[index]
        countLimit = 0
        betu = fekete.betu
        for zold in zoldek:
          if zold.betu == betu:
            countLimit += 1 # ez a betű zöld-e egy másik helyen
        for sarga in sargak:
          if sarga.betu == betu:
            countLimit += 1 # ez a betű sárga-e egy másik helyen
        if vizsgaltSzo.count(betu) == countLimit:
          index += 1
        else:
          self._lehetsegesSzavak.pop(index)

  #van-e egynél több lehetséges megoldás (ha nincs, kitaláltuk a szót)
  def csakEgyTipp(self) -> bool:
    return len(self._lehetsegesSzavak) == 1


szavak = szoBetoltes()

# wordl = Wordl(szavak)
# wordl.kerdes('a', 'b', 'c', 'd', 'e')

megoldo = Megoldo(szavak)
for i in range(1, 9):
  tipp = megoldo.legJobbSzo()
  valaszString = input(
    f"Kérlek add meg a válaszodat a tippemre={tipp[0]}, tipp szám={i}, lehetséges szavak száma={megoldo.szavakSzama()}.\n"
    f"Kérlek használd a következő formát "
    f"<index>:<szín> ahol a szín 'f' : fekete, 's' sárga vagy 'z' zöld lehet vesszővel elválasztva. "
    f"Például: 1:f, 2:s, 3:f, 4:z, 5:f\n")

  valaszok = bemenetKonvertalas(tipp[0], valaszString)
  megoldo.valaszFeldolgozas(valaszok)
  if megoldo.csakEgyTipp():
    print(f"A megoldás szerintem={megoldo.legJobbSzo()}")
    exit()
