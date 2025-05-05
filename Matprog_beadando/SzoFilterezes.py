import os.path as path
from typing import List

diftongusKezdo = ['c', 'd', 'g', 'l', 'n', 's', 't', 'z']
diftongusok = ['cs', 'dz', 'gy', 'ly', 'ny', 'sz', 'ty', 'zs']

def szoSzuro(karakterLimit=5):
  with open('szurt-szavak.txt', 'w') as szurtSzavak:
    with open('magyar-szavak.txt', 'r') as magyarSzavak:
      # with open('nastyWords.txt', 'r') as magyarSzavak:
      for beolvasottSor in magyarSzavak:
        if beolvasottSor[len(beolvasottSor) - 1] == '\n':
          beolvasottSor = beolvasottSor[:-1]
        beolvasottSor = beolvasottSor.lower()
        szoHossz = len(beolvasottSor)
        if (szoHossz >= karakterLimit):  # ha nincs 5 betűs eldobhatjuk
          karakterSzamlalo = 0
          index = 0
          elfogadottKarakterek = ''
          while index < szoHossz and karakterSzamlalo < karakterLimit:
            karakter = beolvasottSor[index]
            if karakter in diftongusKezdo and index + 1 < szoHossz:
              diftongusJelolt = karakter + beolvasottSor[index + 1]
              if diftongusJelolt in diftongusok:
                if diftongusJelolt == 'dz' and index + 2 < szoHossz:
                  haromBetus = ''.join([karakter, beolvasottSor[index + 1], beolvasottSor[index + 2]])
                  if haromBetus == 'dzs':
                    elfogadottKarakterek += haromBetus
                    index += 1
                else:
                  elfogadottKarakterek += karakter + beolvasottSor[index + 1]
                index += 1
              else:
                elfogadottKarakterek += karakter
            else:
              elfogadottKarakterek += karakter
            karakterSzamlalo += 1
            index += 1
            #print(f'{beolvasottSor}\t, karakterSzám={karakterSzamlalo}, \tszohossz={szoHossz},\tindex={index}\t{elfogadottKarakterek}')
          if index != szoHossz or karakterSzamlalo < karakterLimit:  # elértük az 5 betűt de nincs vége a szónak -> eldobhatjuk
            continue
          else:
            szurtSzavak.write(beolvasottSor + '\n')

def szoBetoltes() -> List[List[str]]:
  if not path.exists('szurt-szavak.txt'):
    szoSzuro()

  otBetusSzavak = list()
  with open('szurt-szavak.txt', 'r') as file:
    for beolvasottSor in file:
      if beolvasottSor[len(beolvasottSor) - 1] == '\n':
        beolvasottSor = beolvasottSor[:-1]
      index = 0
      indexeltSzo = list()
      szoHossz = len(beolvasottSor)
      while index < szoHossz:
        karakter = beolvasottSor[index]
        if karakter in diftongusKezdo and index + 1 < szoHossz:
          diftongusJelolt = karakter + beolvasottSor[index + 1]
          if diftongusJelolt in diftongusok:
            if diftongusJelolt == 'dz' and index + 2 < szoHossz:
              haromBetus = ''.join([karakter, beolvasottSor[index + 1], beolvasottSor[index + 2]])
              if haromBetus == 'dzs':
                indexeltSzo.append(haromBetus)
                index += 1
              else:
                indexeltSzo.append(karakter + beolvasottSor[index + 1])
            else:
              indexeltSzo.append(karakter + beolvasottSor[index + 1])
            index += 1
          else:
            indexeltSzo.append(karakter)
        else:
          indexeltSzo.append(karakter)
        index += 1
      otBetusSzavak.append(indexeltSzo)
  return otBetusSzavak