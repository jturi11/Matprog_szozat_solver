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

  def __init__(self, szavak=List[List[str]]):
    self._lehetsegesSzavak = szavak
    self.feketek = list()
    self.sargak = list()
    self.zoldek = list()

  def szavakSzama(self) -> int:
    return len(self._lehetsegesSzavak)

  def indexbeliGyakoriság(self, szavak: List[List[str]], index: int) -> Dict[str, int]:
    dict = defaultdict(int)
    for szo in szavak:
      karakter = szo[index]
      dict[karakter] = dict[karakter] + 1
    return dict

  def legJobbSzo(self) -> {List[str], int}:
    indexBeliGyakorisagok = list()
    for i in range(0, 5):
      indexBeliGyakorisagok.append(self.indexbeliGyakoriság(self._lehetsegesSzavak, i))
      legjobbSzo = None
      legjobbSzoGyakorisag = 0

    for szo in self._lehetsegesSzavak:
      szoErtek = 0
      karakterIndex = 0
      while karakterIndex < karakterLimit:
        karakter = szo[karakterIndex]
        indexbeliGyakorisag = indexBeliGyakorisagok[karakterIndex]
        abszolutGyakorisag = indexbeliGyakorisag[karakter]
        szoErtek += abszolutGyakorisag

        if legjobbSzoGyakorisag < szoErtek:
          legjobbSzo = szo
          legjobbSzoGyakorisag = szoErtek
        karakterIndex += 1

    return legjobbSzo, legjobbSzoGyakorisag

  def valaszFeldolgozas(self, valaszok: List[Valasz]):
    zoldek = list()
    sargak = list()
    feketek = list()

    for valasz in valaszok:
      if valasz.zold():
        zoldek.append(valasz)
      elif valasz.sarga():
        sargak.append(valasz)
      elif valasz.fekete():
        feketek.append(valasz)

    for zold in zoldek:
      index = 0
      while index < len(self._lehetsegesSzavak):
        vizsgaltSzo = self._lehetsegesSzavak[index]
        vizsgaltBetu = vizsgaltSzo[zold.index]
        if vizsgaltBetu == zold.betu:
          index += 1
        else:
          self._lehetsegesSzavak.pop(index)

    for sarga in sargak:
      index = 0
      # sárga helyen nem lehet az a betű
      betu = sarga.betu
      while index < len(self._lehetsegesSzavak):
        vizsgaltSzo = self._lehetsegesSzavak[index]
        vizsgaltBetu = vizsgaltSzo[sarga.index]
        if vizsgaltBetu == betu:
          self._lehetsegesSzavak.pop(index)
        else:
          index += 1
      # a sárgák + zöldek száma >= a betű előfordulása a szóban
      index = 0
      while index < len(self._lehetsegesSzavak):
        vizsgaltSzo = self._lehetsegesSzavak[index]
        countLimit = 0
        for zold in zoldek:
          if zold.betu == betu:
            countLimit += 1
        for sarga2 in sargak:
          if sarga2.betu == betu:
            countLimit += 1
        count = vizsgaltSzo.count(betu)
        if count < countLimit:
          self._lehetsegesSzavak.pop(index)
        else:
          index += 1

    for fekete in feketek:
      index = 0
      while index < len(self._lehetsegesSzavak):
        vizsgaltSzo = self._lehetsegesSzavak[index]
        countLimit = 0
        betu = fekete.betu
        for zold in zoldek:
          if zold.betu == betu:
            countLimit += 1
        for sarga in sargak:
          if sarga.betu == betu:
            countLimit += 1
        if vizsgaltSzo.count(betu) == countLimit:
          index += 1
        else:
          self._lehetsegesSzavak.pop(index)

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
