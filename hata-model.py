from enum import Enum
import math

import matplotlib.pyplot as plt
import numpy as np

plt.style.use('_mpl-gallery')

class BUILDING_TYPE(Enum):
    BIG_CITY = 0
    MEDIUM_CITY = 1
    SUBURBAN_AREAS = 2
    RURAL_AND_OPEN_AREAS = 3

def test_hata():
  print(hata(900, 1, 70, 1.5, BUILDING_TYPE.BIG_CITY))
  print(hata(150, 1, 70, 1.5, BUILDING_TYPE.BIG_CITY))
  print(hata(300, 1, 70, 1.5, BUILDING_TYPE.BIG_CITY))

  print(hata(900, 1, 70, 1.5, BUILDING_TYPE.MEDIUM_CITY))
  print(hata(150, 1, 70, 1.5, BUILDING_TYPE.MEDIUM_CITY))
  print(hata(300, 1, 70, 1.5, BUILDING_TYPE.MEDIUM_CITY))

  print(hata(900, 1, 70, 1.5, BUILDING_TYPE.SUBURBAN_AREAS))
  print(hata(150, 1, 70, 1.5, BUILDING_TYPE.SUBURBAN_AREAS))
  print(hata(300, 1, 70, 1.5, BUILDING_TYPE.SUBURBAN_AREAS))

  print(hata(900, 1, 70, 1.5, BUILDING_TYPE.RURAL_AND_OPEN_AREAS))
  print(hata(150, 1, 70, 1.5, BUILDING_TYPE.RURAL_AND_OPEN_AREAS))
  print(hata(300, 1, 70, 1.5, BUILDING_TYPE.RURAL_AND_OPEN_AREAS))

def example_data_hata():
  # f <- [150;1500] MHz - 
  # ht <- [30;200] m - 
  # hr <- [1;10] m - 
  # d <- [1;20] km - 
  # type 0 - big city | 1 - medium city | 2 - suburban areas | 3 - rural and open areas

  # make data 1:
  x = np.linspace(2, 5, 31)
  print(x)
  y_bigcity = []
  y_mediumcity = []
  y_subarea = []
  y_openarea = []

  for value in x:
    y_bigcity.append(hata(900, value, 50, 1.5, BUILDING_TYPE.BIG_CITY))
    y_mediumcity.append(hata(900, value, 50, 1.5, BUILDING_TYPE.MEDIUM_CITY))
    y_subarea.append(hata(900, value, 50, 1.5, BUILDING_TYPE.SUBURBAN_AREAS))
    y_openarea.append(hata(900, value, 50, 1.5, BUILDING_TYPE.RURAL_AND_OPEN_AREAS))

  # plot
  _, ax = plt.subplots(4,1,layout='constrained', figsize=(10,10))

  ax[0].plot(x, y_bigcity, linewidth=2.0)
  ax[0].set(xlim=(2, 5), xticks=np.arange(2, 5, 0.1),
        ylim=(130, 150), yticks=np.arange(130, 150, 5))
  ax[0].set_title('Big City')
  ax[0].set_xlabel('D[km]')
  ax[0].set_ylabel('L[dB]')

  ax[1].plot(x, y_mediumcity, linewidth=2.0)
  ax[1].set(xlim=(2, 5), xticks=np.arange(2, 5, 0.1),
        ylim=(130, 150), yticks=np.arange(130, 150, 5))
  ax[1].set_title('Medium City')
  ax[1].set_xlabel('D[km]')
  ax[1].set_ylabel('L[dB]')

  ax[2].plot(x, y_subarea, linewidth=2.0)
  ax[2].set(xlim=(2, 5), xticks=np.arange(2, 5, 0.1),
        ylim=(120, 140), yticks=np.arange(120, 140, 5))
  ax[2].set_title('Suburban Areas')
  ax[2].set_xlabel('D[km]')
  ax[2].set_ylabel('L[dB]')

  ax[3].plot(x, y_openarea, linewidth=2.0)
  ax[3].set(xlim=(2, 5), xticks=np.arange(2, 5, 0.1),
        ylim=(100, 120), yticks=np.arange(100, 120, 5))
  ax[3].set_title('Rural and Open Areas')
  ax[3].set_xlabel('D[km]')
  ax[3].set_ylabel('L[dB]')

  plt.show()
  
def input_hata():
  f0 = get_input('Enter f0[MHz][150;1500]: ', 150, 1500)
  ht = get_input('Enter ht[m][30;200]: ', 30, 200)
  hr = get_input('Enter hr[m][1;10]: ', 1, 10)
  d = get_input('Enter d[km][1;20]: ', 1, 20)
  building_type = BUILDING_TYPE(get_input('Enter building type: 0 - big city | 1 - medium city | 2 - suburban areas | 3 - rural and open areas', 0, 3))
  hata_with_display(f0, d, ht, hr, building_type)


def get_input(prompt, min_value, max_value):
  while True:
    print(prompt)
    value = float(input())
    if min_value <= value <= max_value:
      return value
    else:
      print(f'Please enter a value between {min_value} and {max_value}.')

def hata_with_display(f0, d, ht, hr, building_type):
  
  l = hata(f0, d, ht, hr, building_type)
  print('--- Hata model for data: ---')
  print(f'f0: {f0} MHz')
  print(f'ht: {ht} m')
  print(f'hr: {hr} m')
  print(f'd: {d} km')
  print(f'building type: {building_type.name}')
  print(f'Answer: {l} dB')

def hata(f0, d, ht, hr, building_type):
  
  a = correction_factor(f0, hr, building_type)

  # big city medium city
  l = 69.55 + 26.16 * math.log10(f0) - 13.82 * math.log10(ht) - a + ((44.9 - 6.55 * math.log10(ht)) * math.log10(d))

  if building_type.value == 2:
    # suburban areas
    l = l - 2 * pow(math.log10(f0/28), 2) - 5.4
  if building_type.value == 3:
    l = l - 4.78 * pow(math.log10(f0), 2) + 18.33 * math.log10(f0) - 40.94
  
  return l

def correction_factor(f0, hr, building_type):
  if building_type.value == 0:
    # big_city
    if f0 >= 400:
      a = (3.2 * pow(math.log10(11.75 * hr),2)) - 4.97
    elif f0 <= 200:
      a = (8.29 * pow(math.log10(1.54 * hr),2)) - 1.1
    else:
      a_high = (3.2 * pow(math.log10(11.75 * hr),2)) - 4.97
      a_low = (8.29 * pow(math.log10(1.54 * hr),2)) - 1.1
      weight_high = 1 / abs(f0 - 400)
      weight_low = 1 / abs(f0 - 200)
      a = (a_high * weight_high + a_low * weight_low) / (weight_high + weight_low)
  elif building_type.value in [1, 2, 3]:
    # medium city
    a = ((1.1 * math.log10(f0) - 0.7) * hr) - (1.56 * math.log10(f0) - 0.8)
  else:
    print("Wrong building_type in correction_factor")
    return None
  return a

def main():
  choice = 0
  while True:
    print('-- Hata Model --')
    print('1. Example data')
    print('2. Input data')
    print('3. Exit')

    choice = input()

    if choice == '1':
      example_data_hata()
    elif choice == '2':
      input_hata()
    elif choice == '3':
      break
    elif choice == 'test':
      test_hata()
    else: 
      print('Wrong input. Try again.')



main()