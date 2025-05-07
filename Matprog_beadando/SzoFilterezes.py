import os.path as path
from typing import List

#Diftongusok lehetséges kezdőbetűi
diftongusKezdo = ['c', 'd', 'g', 'l', 'n', 's', 't', 'z']
#Kétjegyű betűk
diftongusok = ['cs', 'dz', 'gy', 'ly', 'ny', 'sz', 'ty', 'zs']

def szoSzuro(karakterLimit=5):
  """
  Kiszűri a szólistából lévő szavakat úgy, hogy 5 betű hosszúak legyenek.
  Figyelembe veszi a dupla és tripla hosszú betűket.
  """
  with open('szurt-szavak.txt', 'w',encoding="utf-8") as szurtSzavak:
    with open('magyar-szavak.txt', 'r',encoding="utf-8") as magyarSzavak:
      # Beolvassuk a szavakat (sorokat) a szólistából
      for beolvasottSor in magyarSzavak:
        #eltávolítjuk a sortöréseket, ha van
        if beolvasottSor[len(beolvasottSor) - 1] == '\n':
          beolvasottSor = beolvasottSor[:-1]
        #Kisbetűssé alakítjuk a szót
        beolvasottSor = beolvasottSor.lower()
        szoHossz = len(beolvasottSor)
        if (szoHossz >= karakterLimit):  # ha nincs 5 betűs eldobhatjuk
          karakterSzamlalo = 0 #számolja a betűket, jól a diftongusokat beleszámítva
          index = 0 #index a szó karakterein belül (index=diftongusokat nem számítva)
          elfogadottKarakterek = '' #Elfogadott betű
          #Amíg nem értük el a szó végét vagy karakterlimitet
          while index < szoHossz and karakterSzamlalo < karakterLimit:
            karakter = beolvasottSor[index]
            #Ha a karakter diftongus kezdőbetűje, és még van követekzeő karakter
            if karakter in diftongusKezdo and index + 1 < szoHossz:
              diftongusJelolt = karakter + beolvasottSor[index + 1]
              #Ha két karakter együtt egy betű
              if diftongusJelolt in diftongusok:
                #Külön eset 'dzs' szűrése
                if diftongusJelolt == 'dz' and index + 2 < szoHossz:
                  haromBetus = ''.join([karakter, beolvasottSor[index + 1], beolvasottSor[index + 2]])
                  if haromBetus == 'dzs':
                    elfogadottKarakterek += haromBetus
                    index += 1 #Mivel 3 betűs, további egyet lépünk
                else:
                  #Kétbetűs diftongusok hozzáadása
                  elfogadottKarakterek += karakter + beolvasottSor[index + 1]
                index += 1 #Mivel két betűt olvasunk be indexet növeljük mégegyszer
              else:
                #Nem diftongus, csak sima karakter hozzáadása
                elfogadottKarakterek += karakter
            else:
              #Nem diftongus, csak sima karakter hozzáadása
              elfogadottKarakterek += karakter
            karakterSzamlalo += 1 #Karaktereket számoljuk, diftongusok 1-nek számítanak
            index += 1 #Következő karakterre lépés
          #Ha a ciklus után nem értünk a szó végére, vagy nem értük el az 5 karaktert, akkor nem fogadjuk el
          if index != szoHossz or karakterSzamlalo < karakterLimit:
            continue
          else:
            #Ha megfelel a feltételeknek, akkor kiírjuk egy szót egy kimeneti fájlba
            szurtSzavak.write(beolvasottSor + '\n')

def szoBetoltes() -> List[List[str]]:
  """
  Betölti a 'szurt-szavak.txt' fájlban lévő szavakat, és szavanként
  a diftongusokat egy elemként kezeli, így 1-1 szó egy listát ad vissza,
  ahol minden elem egy betű.
  """
  
  #Ha még nincs létrehozva szűrt szó fájl, akkor létrehozunk
  if not path.exists('szurt-szavak.txt'):
    szoSzuro()

  otBetusSzavak = list() #5 betűs szavakat itt raktározzuk
  with open('szurt-szavak.txt', 'r',encoding="utf-8") as file:
    #Minden szót/sort beolvasunk
    for beolvasottSor in file:
      #Eltávolítjuk a sortörést, ha van
      if beolvasottSor[len(beolvasottSor) - 1] == '\n':
        beolvasottSor = beolvasottSor[:-1]
      index = 0
      indexeltSzo = list() #Itt tároljuk a szavak betűit
      szoHossz = len(beolvasottSor)
      #Végigmegyünk a szó karakterein
      while index < szoHossz:
        karakter = beolvasottSor[index]
        #Ha a karakter diftongus és van következő karakter
        if karakter in diftongusKezdo and index + 1 < szoHossz:
          diftongusJelolt = karakter + beolvasottSor[index + 1]
          #Ha a két karakter együtt diftongus
          if diftongusJelolt in diftongusok:
            #Külön eset a 'dzs'
            if diftongusJelolt == 'dz' and index + 2 < szoHossz:
              haromBetus = ''.join([karakter, beolvasottSor[index + 1], beolvasottSor[index + 2]])
              if haromBetus == 'dzs':
                indexeltSzo.append(haromBetus)
                index += 1 #3 betű miatt további 1 lépés
              else:
                indexeltSzo.append(karakter + beolvasottSor[index + 1])
            else:
              indexeltSzo.append(karakter + beolvasottSor[index + 1])
            index += 1 #2 betűs diftongus miatt további lépés
          else:
            #Nem diftongus, sima karakter hozzáadása
            indexeltSzo.append(karakter)
        else:
          indexeltSzo.append(karakter) #nem diftongus kezdőbetű, sima karakter hozzáadása
        index += 1 #Következő karakterre lépés
      otBetusSzavak.append(indexeltSzo) #Feldolgozott szó (betűk listája) hozzáadása az eredményhez
  return otBetusSzavak