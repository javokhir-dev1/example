import argparse
import random
import string
import itertools

# ==================== LEET SPEAK (KENGAYTIRILGAN) ====================
LEET = {
    'a': ['@', '4', '^', 'а'],
    'b': ['8', '6', '|3'],
    'c': ['(', '{', '<', 'к'],
    'd': ['|)', 'cl'],
    'e': ['3', '€', '£'],
    'f': ['ph', '|='],
    'g': ['9', '6', 'q'],
    'h': ['#', '|-|', '}{'],
    'i': ['1', '!', '|', 'и'],
    'j': ['_|', ';'],
    'k': ['|<', '|{'],
    'l': ['1', '|', '£'],
    'm': ['/\\/\\', '|\\/|'],
    'n': ['/\\/', '|\\|'],
    'o': ['0', '()', 'о'],
    'p': ['|*', '|>'],
    'q': ['9', '0_'],
    'r': ['|2', '®'],
    's': ['$', '5', 'z'],
    't': ['7', '+', '†'],
    'u': ['|_|', 'v'],
    'v': ['\\/', '√'],
    'w': ['\\/\\/', 'vv'],
    'x': ['><', '%', '×'],
    'y': ['¥', '`/'],
    'z': ['2', 'z', '≥'],
}

BELGILAR = ['!', '@', '#', '$', '%', '&', '*', '_', '-', '.', '?', '+', '=', '~', '^']
AJRATGICHLAR = ['_', '-', '.', '', '@', '#', '!', '*', '+', '~', '__', '--', '..']

# ==================== PREFIKSLAR VA SUFFIKSLAR ====================
PREFIKSLAR = [
    'The', 'Mr', 'My', 'Im', 'x_', 'X_', 'its', 'real', 'official',
    'pro', 'king', 'dark', 'super', 'mega', 'ultra', 'boss', 'don',
    'el', 'big', 'lil', 'old', 'new', 'top', 'best', 'true',
]

SUFFIKSLAR = [
    '_official', '_real', '_pro', '_king', '_boss', '_01', '_xx',
    'YT', 'TV', 'UZ', 'tm', 'dev', 'hack', 'sec', 'admin',
    'root', 'god', 'lord', 'fire', 'ice', 'wolf', 'lion', 'eagle',
]

# ==================== KEYBOARD PATTERNLAR ====================
KEYBOARD_PATTERNS = [
    'qwerty', 'qwert', 'asdf', 'zxcv', 'qazwsx', 'qweasd',
    '1qaz2wsx', 'zaq1', '!QAZ2wsx', 'qwerty123', 'asdf1234',
    '1q2w3e4r', '1q2w3e', 'zxcvbnm', 'poiuyt', 'mnbvcxz',
    'q1w2e3r4', 'asdfjkl', '1234qwer', 'qwer1234',
]

# ==================== O'ZBEK SO'ZLARI ====================
UZBEK_SOZLAR = [
    'parol', 'maxfiy', 'salom', 'xayr', 'sevgi', 'hayot',
    'oltin', 'kumush', 'sherzod', 'sardor', 'botir', 'jasur',
    'aziz', 'bahodir', 'dilshod', 'farhod', 'nodir', 'temur',
    'ulugbek', 'mirzo', 'anvar', 'baxtiyor', 'davlat', 'erkin',
    'toshkent', 'samarqand', 'buxoro', 'andijon', 'namangan',
    'fergana', 'nukus', 'jizzax', 'qarshi', 'termiz',
    'uzbek', 'ozbekiston', 'vatan', 'mustaqil',
]

# ==================== KO'P ISHLATILADIGAN RAQAM PATTERNLAR ====================
RAQAM_PATTERNS = [
    '123', '1234', '12345', '123456', '111', '222', '333', '444',
    '555', '666', '777', '888', '999', '000', '007', '001',
    '321', '4321', '54321', '112', '911', '404', '500',
    '69', '77', '99', '13', '07', '01', '11', '21', '31',
    '100', '200', '300', '1000', '2000', '3000',
]

# ==================== YILLAR ====================
YILLAR = [str(y) for y in range(1990, 2027)] + \
         [str(y)[2:] for y in range(1990, 2027)] + \
         ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']


# ==================== FUNKSIYALAR ====================
def leet_almashtirish(soz, intensivlik=0.3):
    """So'zdagi harflarni tasodifiy leet belgilariga almashtiradi"""
    natija = []
    for harf in soz:
        if harf.lower() in LEET and random.random() < intensivlik:
            natija.append(random.choice(LEET[harf.lower()]))
        else:
            natija.append(harf)
    return ''.join(natija)


def katta_kichik_aralashtirish(soz):
    """Harflarni tasodifiy katta/kichik qiladi"""
    return ''.join(
        h.upper() if random.random() < 0.4 else h.lower()
        for h in soz
    )


def birinchi_harf_katta(soz):
    """Faqat birinchi harfni katta qiladi"""
    return soz[0].upper() + soz[1:].lower() if soz else soz


def camel_case(sozlar):
    """camelCase: adminTashkent"""
    return sozlar[0].lower() + ''.join(s.capitalize() for s in sozlar[1:])


def takrorlash(soz):
    """So'zni takrorlaydi: adminadmin"""
    usul = random.choice(['full', 'double_char', 'partial'])
    if usul == 'full':
        return soz + soz
    elif usul == 'double_char':
        return ''.join(h * 2 for h in soz[:4])
    else:
        return soz + soz[::-1]


def qisqartirish(sozlar):
    """So'zlarning birinchi harflarini oladi"""
    return ''.join(s[0] for s in sozlar if s)


def telefon_pattern(telefon):
    """Telefon raqamidan turli kombinatsiyalar"""
    raqam = telefon.replace('+', '').replace('-', '').replace(' ', '')
    patterns = []
    if len(raqam) >= 4:
        patterns.append(raqam[-4:])           # oxirgi 4
        patterns.append(raqam[-7:])           # oxirgi 7
        patterns.append(raqam[-4:][::-1])     # teskari 4
    if len(raqam) >= 9:
        patterns.append(raqam[-9:])           # oxirgi 9
    patterns.append(raqam)                     # to'liq
    return patterns


# ==================== PAROL GENERATORLAR ====================
def parol_yasash(kalit_sozlar, soni, tug_yil=None, telefon=None, daraja='orta'):
    """Kalit so'zlar asosida parollar to'plamini yaratadi"""
    parollar = set()
    urinishlar = 0
    max_urinish = soni * 100

    # Telefon raqam patternlari
    tel_patterns = telefon_pattern(telefon) if telefon else []

    # Barcha so'zlar (kalit + o'zbek)
    kengaytirilgan = kalit_sozlar.copy()

    # Daraja bo'yicha usullar soni
    if daraja == 'oson':
        max_usul = 10
    elif daraja == 'orta':
        max_usul = 18
    else:  # murakkab
        max_usul = 25
        kengaytirilgan += random.sample(UZBEK_SOZLAR, min(5, len(UZBEK_SOZLAR)))

    while len(parollar) < soni and urinishlar < max_urinish:
        urinishlar += 1
        usul = random.randint(1, max_usul)

        try:
            if usul == 1:
                # kalit1_kalit2 + raqamlar
                sozlar = random.sample(kalit_sozlar, min(random.randint(1, 3), len(kalit_sozlar)))
                ajratgich = random.choice(AJRATGICHLAR)
                parol = ajratgich.join(sozlar) + str(random.randint(0, 9999))

            elif usul == 2:
                # Leet speak + belgi
                soz = random.choice(kalit_sozlar)
                parol = leet_almashtirish(soz) + random.choice(BELGILAR) + str(random.randint(10, 999))

            elif usul == 3:
                # Katta-kichik aralash + raqam + belgi
                soz = random.choice(kalit_sozlar)
                parol = katta_kichik_aralashtirish(soz) + str(random.randint(1, 9999)) + random.choice(BELGILAR)

            elif usul == 4:
                # Teskari + raqam
                soz = random.choice(kalit_sozlar)
                parol = soz[::-1] + str(random.randint(100, 9999))

            elif usul == 5:
                # 2ta so'z + leet + belgi
                sozlar = random.sample(kalit_sozlar, min(2, len(kalit_sozlar)))
                parol = leet_almashtirish(sozlar[0]) + random.choice(BELGILAR) + katta_kichik_aralashtirish(sozlar[-1])

            elif usul == 6:
                # Birinchi harflar + raqamlar + belgilar
                bosh_harflar = ''.join([s[0].upper() for s in kalit_sozlar])
                parol = bosh_harflar + str(random.randint(100, 99999)) + random.choice(BELGILAR) * random.randint(1, 3)

            elif usul == 7:
                # So'z + yil + belgi
                soz = random.choice(kalit_sozlar)
                yil = random.choice(YILLAR)
                parol = katta_kichik_aralashtirish(soz) + yil + random.choice(BELGILAR)

            elif usul == 8:
                # Murakkab: leet + katta-kichik + raqam + belgi + ikkinchi so'z
                sozlar = random.sample(kalit_sozlar, min(2, len(kalit_sozlar)))
                qism1 = leet_almashtirish(katta_kichik_aralashtirish(sozlar[0]))
                qism2 = katta_kichik_aralashtirish(sozlar[-1])
                parol = qism1 + random.choice(BELGILAR) + str(random.randint(0, 99)) + qism2

            elif usul == 9:
                # Prefiks + so'z + raqam
                soz = random.choice(kalit_sozlar)
                prefiks = random.choice(PREFIKSLAR)
                parol = prefiks + birinchi_harf_katta(soz) + str(random.randint(1, 999))

            elif usul == 10:
                # So'z + suffiks + raqam
                soz = random.choice(kalit_sozlar)
                suffiks = random.choice(SUFFIKSLAR)
                parol = katta_kichik_aralashtirish(soz) + suffiks + str(random.randint(0, 99))

            # ===== O'RTA VA MURAKKAB =====

            elif usul == 11:
                # Keyboard pattern + so'z
                pattern = random.choice(KEYBOARD_PATTERNS)
                soz = random.choice(kalit_sozlar)
                parol = random.choice([
                    soz + pattern,
                    pattern + soz,
                    soz + random.choice(BELGILAR) + pattern,
                ])

            elif usul == 12:
                # Takrorlash: adminadmin, aaddmmiinn
                soz = random.choice(kalit_sozlar)
                parol = takrorlash(soz) + str(random.randint(0, 99))

            elif usul == 13:
                # CamelCase: adminTashkent2024
                sozlar = random.sample(kalit_sozlar, min(2, len(kalit_sozlar)))
                parol = camel_case(sozlar) + random.choice(YILLAR)

            elif usul == 14:
                # Tug'ilgan yil kombinatsiyasi
                if tug_yil:
                    soz = random.choice(kalit_sozlar)
                    parol = random.choice([
                        soz + tug_yil,
                        soz + tug_yil + random.choice(BELGILAR),
                        birinchi_harf_katta(soz) + tug_yil,
                        katta_kichik_aralashtirish(soz) + tug_yil + random.choice(BELGILAR),
                        soz + random.choice(BELGILAR) + tug_yil,
                        tug_yil + soz,
                        tug_yil + random.choice(BELGILAR) + soz,
                        leet_almashtirish(soz) + tug_yil,
                        soz[::-1] + tug_yil,
                    ])
                else:
                    continue

            elif usul == 15:
                # Telefon raqam kombinatsiyasi
                if tel_patterns:
                    soz = random.choice(kalit_sozlar)
                    tel = random.choice(tel_patterns)
                    parol = random.choice([
                        soz + tel,
                        soz + random.choice(BELGILAR) + tel,
                        birinchi_harf_katta(soz) + tel,
                        tel + soz,
                        tel + random.choice(BELGILAR) + soz,
                        leet_almashtirish(soz) + tel,
                    ])
                else:
                    continue

            elif usul == 16:
                # Raqam pattern + so'z + belgi
                soz = random.choice(kalit_sozlar)
                raqam = random.choice(RAQAM_PATTERNS)
                parol = random.choice([
                    soz + raqam,
                    soz + raqam + random.choice(BELGILAR),
                    birinchi_harf_katta(soz) + raqam,
                    raqam + soz,
                    katta_kichik_aralashtirish(soz) + raqam + random.choice(BELGILAR),
                ])

            elif usul == 17:
                # O'zbek so'z + kalit so'z
                uzb = random.choice(UZBEK_SOZLAR)
                soz = random.choice(kalit_sozlar)
                parol = random.choice([
                    uzb + soz + str(random.randint(1, 99)),
                    soz + uzb + str(random.randint(1, 999)),
                    birinchi_harf_katta(uzb) + birinchi_harf_katta(soz),
                    leet_almashtirish(uzb) + random.choice(BELGILAR) + soz,
                ])

            elif usul == 18:
                # Permutatsiya — barcha tartiblar
                sozlar = random.sample(kalit_sozlar, min(random.randint(2, 3), len(kalit_sozlar)))
                random.shuffle(sozlar)
                ajratgich = random.choice(AJRATGICHLAR)
                parol = ajratgich.join(sozlar) + random.choice(BELGILAR) + str(random.randint(0, 99))

            # ===== MURAKKAB =====

            elif usul == 19:
                # Intensiv leet speak (70%)
                soz = random.choice(kalit_sozlar)
                parol = leet_almashtirish(soz, 0.7) + str(random.randint(10, 9999))

            elif usul == 20:
                # Prefiks + leet + yil
                soz = random.choice(kalit_sozlar)
                parol = random.choice(PREFIKSLAR) + leet_almashtirish(soz) + random.choice(YILLAR)

            elif usul == 21:
                # Qisqartma + raqam + belgi + so'z
                qisqa = qisqartirish(kalit_sozlar).upper()
                soz = random.choice(kalit_sozlar)
                parol = qisqa + str(random.randint(100, 9999)) + random.choice(BELGILAR) + katta_kichik_aralashtirish(soz)

            elif usul == 22:
                # To'liq murakkab: prefiks + leet + telefon + belgi
                soz = random.choice(kalit_sozlar)
                qism1 = random.choice(PREFIKSLAR) if random.random() > 0.5 else ''
                qism2 = leet_almashtirish(katta_kichik_aralashtirish(soz), 0.5)
                qism3 = random.choice(tel_patterns) if tel_patterns else str(random.randint(100, 9999))
                parol = qism1 + qism2 + random.choice(BELGILAR) + qism3

            elif usul == 23:
                # Teskari + leet + yil + belgi
                soz = random.choice(kalit_sozlar)
                parol = leet_almashtirish(soz[::-1]) + random.choice(YILLAR) + random.choice(BELGILAR) * 2

            elif usul == 24:
                # 3 ta so'z + murakkab
                sozlar = random.sample(kengaytirilgan, min(3, len(kengaytirilgan)))
                parol = random.choice(BELGILAR).join([
                    leet_almashtirish(sozlar[0]),
                    katta_kichik_aralashtirish(sozlar[1]),
                    sozlar[2][::-1]
                ]) + str(random.randint(0, 99))

            elif usul == 25:
                # Ultra murakkab: random harflar + kalit so'z qismlari
                soz = random.choice(kalit_sozlar)
                rand_part = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
                parol = soz[:3] + random.choice(BELGILAR) + rand_part + random.choice(BELGILAR) + soz[-3:]

            else:
                continue

            parollar.add(parol)

        except (ValueError, IndexError):
            continue

    return list(parollar)[:soni]


def main():
    parser = argparse.ArgumentParser(
        description='Kalit so\'zlar asosida kuchli parollar generatori v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Misollar:
  python parol_yasash.py -k ali admin tashkent -s 50
  python parol_yasash.py -k ali admin -s 100 -d 2006 -f parollar.txt
  python parol_yasash.py -k ali admin -s 500 -d 2006 -t 998901234567 --daraja murakkab
  python parol_yasash.py -k javohir dev -s 200 -d 2003 -t 998912345678 --daraja murakkab -f parollar.txt

Darajalar:
  oson     — 10 usul, oddiy kombinatsiyalar
  orta     — 18 usul, keyboard pattern, o'zbek so'zlar (standart)
  murakkab — 25 usul, barcha usullar, intensiv leet speak
        """
    )

    parser.add_argument('-k', '--kalit_sozlar', nargs='+', required=True,
                        help='Parol uchun kalit so\'zlar')
    parser.add_argument('-s', '--soni', type=int, default=10,
                        help='Nechta parol yasash (standart: 10)')
    parser.add_argument('-f', '--fayl', type=str, default=None,
                        help='Parollarni faylga saqlash')
    parser.add_argument('-d', '--tug_yil', type=str, default=None,
                        help='Tug\'ilgan yil (masalan: 2006)')
    parser.add_argument('-t', '--telefon', type=str, default=None,
                        help='Telefon raqam (masalan: 998901234567)')
    parser.add_argument('--daraja', type=str, default='orta',
                        choices=['oson', 'orta', 'murakkab'],
                        help='Murakkablik darajasi (standart: orta)')

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  PAROL GENERATORI v2.0")
    print(f"{'='*60}")
    print(f"  Kalit so'zlar : {', '.join(args.kalit_sozlar)}")
    print(f"  Soni          : {args.soni}")
    print(f"  Daraja        : {args.daraja}")
    print(f"  Tug'ilgan yil : {args.tug_yil or '—'}")
    print(f"  Telefon       : {args.telefon or '—'}")
    usullar = {'oson': 10, 'orta': 18, 'murakkab': 25}
    print(f"  Usullar soni  : {usullar[args.daraja]}")
    print(f"{'='*60}\n")

    parollar = parol_yasash(
        args.kalit_sozlar, args.soni,
        tug_yil=args.tug_yil,
        telefon=args.telefon,
        daraja=args.daraja
    )

    print(f"  {'#':>4} | {'Parol':<45} | Uzunlik")
    print(f"  {'-'*4}+{'-'*47}+{'-'*8}")

    for i, parol in enumerate(parollar, 1):
        print(f"  {i:>4} | {parol:<45} | {len(parol)}")

    print(f"\n  Jami: {len(parollar)} ta parol yaratildi.\n")

    if args.fayl:
        with open(args.fayl, 'w', encoding='utf-8') as f:
            for parol in parollar:
                f.write(parol + '\n')
        print(f"  Parollar '{args.fayl}' fayliga saqlandi!\n")


if __name__ == '__main__':
    main()
