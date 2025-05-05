import numpy as np
from typing import List


class Valasz:
  def __init__(self, index: int, szin: str, betu:str):
    self._index = index
    self._szin = szin
    self._betu = betu

  def __init__(self, repr: str):
    split = repr.split(':')
    self._index = int(split[0].strip())-1
    self._szin = split[1].strip()

  @property
  def index(self):
    return self._index

  @property
  def szin(self):
    return self._szin

  @property
  def betu(self):
    return self._betu

  def megadBetu(self, betu: str):
    self._betu = betu

  def zold(self) -> bool:
    return self._szin == 'z'

  def sarga(self) -> bool:
    return self._szin == 's'

  def fekete(self) -> bool:
    return self._szin == 'f'

  def __repr__(self):
    return f'{self._index}:{self._szin}:{self._betu}'


class Jatek:

  def __init__(self, szavak: List[List[str]]):
    index = np.random.randint(0, len(szavak))
    self._szo = szavak[index]
    self._tippSzamlalo = 0

  def __repr__(self):
    return f'szo:{self._szo}, tippek={self._tippSzamlalo}'

  @property
  def szo(self) -> str:
    return ''.join(self._szo)

  def kerdes(self, c1, c2, c3, c4, c5) -> List[Valasz]:
    valasz = list()
    valasz.append(Valasz(1, self._charKerdes(c1, 0)))
    valasz.append(Valasz(2, self._charKerdes(c2, 1)))
    valasz.append(Valasz(3, self._charKerdes(c3, 2)))
    valasz.append(Valasz(4, self._charKerdes(c4, 3)))
    valasz.append(Valasz(5, self._charKerdes(c5, 4)))
    self._tippSzamlalo += 1
    print(f'{self}, tipp: {[c1, c2, c3, c4, c5]}, valasz: {valasz}')
    return valasz

  def _charKerdes(self, char, idx):
    if char == self._szo[idx]:
      return 'z'
    elif char in self._szo:
      return 's'
    return 'f'
