import csv
import os

def zpracuj_objednavky(cesta):
    if not os.path.exists(cesta):
        print(f"Soubor {cesta} nebyl nalezen.")
        return

    data_objednavek = {}

    with open(cesta, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for radek in reader:
            try:
                id_obj = radek['cislo_objednavky']
                zakaznik = radek['zakaznik']
                zaplaceno = radek['zaplaceno']
                polozka = radek['nazev_polozky']
                mn = float(radek['mnozstvi'])
                cena = float(radek['cena_za_kus'])

                
                if mn <= 0 or cena <= 0 or not polozka.strip():
                    continue

                
                if id_obj in data_objednavek:
                    stary = data_objednavek[id_obj]
                    if stary['zakaznik'] != zakaznik or stary['zaplaceno'] != zaplaceno:
                        stary['nekonzistentni'] = True
                        continue
                else:
                    data_objednavek[id_obj] = {
                        'id': id_obj, 'zakaznik': zakaznik, 'zaplaceno': zaplaceno,
                        'celkem': 0, 'pocet_polozek': 0, 'nekonzistentni': False
                    }

                
                data_objednavek[id_obj]['celkem'] += mn * cena
                data_objednavek[id_obj]['pocet_polozek'] += mn

            except (ValueError, KeyError):
                continue 

    vysledek = [v for v in data_objednavek.values() if not v['nekonzistentni']]
    
    vysledek.sort(key=lambda x: (-x['celkem'], -x['pocet_polozek'], x['id']))

    print(f"{'ID':<6} | {'ZÁKAZNÍK':<15} | {'CELKEM':<10} | {'POLOŽEK'}")
    print("-" * 50)
    for o in vysledek:
        print(f"{o['id']:<6} | {o['zakaznik']:<15} | {o['celkem']:<10.2f} | {o['pocet_polozek']}")

zpracuj_objednavky('objednavky.csv')
