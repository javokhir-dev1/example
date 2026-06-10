# 🔐 Security Testing Toolkit

Ushbu loyiha **ieltstation.com** platformasida topilgan xavfsizlik zaifligini
aniqlash va tasdiqlash jarayonida ishlatilgan vositalarni o'z ichiga oladi.

---

## 📁 Fayllar tuzilishi

```
site_monitoring/
├── main.py              # Saytni monitoring qilish (webview)
├── parol_yasash.py      # Kalit so'zlar asosida parollar generatori
├── post_yuborish.py     # URL'ga parallel POST so'rovlar yuborish
├── otp_bruteforce.py    # OTP brute force (oddiy, threadli)
├── otp_stealth.py       # OTP brute force (stealth — fingerprint spoofing)
├── otp_turbo.py         # OTP brute force (async turbo — eng tez)
├── parollar.txt         # Generatsiya qilingan parollar ro'yxati
└── sorovlar_logi/       # Tarmoq so'rovlari loglari
```

---

## 1️⃣ main.py — Sayt Monitoring

Saytni `pywebview` oynasida ochib, barcha **fetch** va **XMLHttpRequest**
so'rovlarini (request + response) ushlab, JSON faylga saqlaydi.

```bash
python main.py
```

**Nima qiladi:**
- Saytni desktop oynada ochadi
- Barcha tarmoq so'rovlarini real-time ushlaydi
- Har bir so'rov `sorovlar_logi/` papkasiga JSON sifatida saqlanadi
- Sahifada refresh tugmasi mavjud (pastki o'ng burchak)

**Natija:** Saytning API endpointlari, request/response formati va
cookie tuzilishini o'rganish imkonini berdi.

---

## 2️⃣ parol_yasash.py — Parol Generatori

Berilgan kalit so'zlar asosida turli xil parollar kombinatsiyasini yaratadi.

```bash
# 20 ta parol yasash
python parol_yasash.py -k admin test kalit -s 20

# 100 ta parol yasab faylga saqlash
python parol_yasash.py -k admin test kalit -s 100 -f parollar.txt
```

| Argument | Tavsif | Standart |
|----------|--------|----------|
| `-k` | Kalit so'zlar (bir nechta) | *majburiy* |
| `-s` | Parollar soni | 10 |
| `-f` | Faylga saqlash | — |

**Generatsiya usullari:**
- Leet speak: `admin` → `@dm!n`
- Katta-kichik aralash: `admin` → `AdMiN`
- Teskari: `admin` → `nimda`
- So'zlarni birlashtirish: `admin_test2547`
- Yil qo'shish: `aDmIN2025!`
- Murakkab kombinatsiya: `4dM!n$12tEsT`

---

## 3️⃣ post_yuborish.py — Parallel POST So'rov

URL'ga parollar ro'yxatidan foydalanib parallel POST so'rovlar yuboradi.
To'g'ri parol topilganda jarayonni to'xtatadi.

```bash
# Oddiy ishlatish
python post_yuborish.py -u https://sayt.com/login -n admin -p parollar.txt -x "Invalid"

# 20 ta thread bilan
python post_yuborish.py -u https://sayt.com/login -n admin -p parollar.txt -x "Invalid" -t 20
```

| Argument | Tavsif | Standart |
|----------|--------|----------|
| `-u` | POST yuboriladigan URL | *majburiy* |
| `-n` | Username | *majburiy* |
| `-p` | Parollar .txt fayli | *majburiy* |
| `-x` | Noto'g'ri parolda chiqadigan so'z | — |
| `-t` | Threadlar soni | 10 |

**Parol aniqlash logikasi:**
- `-x "Invalid"` berilgan → javobda "Invalid" yo'q = ✅ parol to'g'ri
- `-x` berilmagan → status 302 (redirect) = ✅ parol to'g'ri
- Status 400+ → ❌ har doim noto'g'ri

---

## 4️⃣ otp_bruteforce.py — OTP Brute Force (Oddiy)

OTP kodlarni 0001-9999 orasida threadlar bilan parallel sinab ko'radi.

```bash
python otp_bruteforce.py -e user@gmail.com -t 10
```

| Argument | Tavsif | Standart |
|----------|--------|----------|
| `-e` | Email manzil | *majburiy* |
| `-u` | API URL | otaboyev-prep.uz |
| `-b` | Boshlang'ich kod | 1 |
| `-g` | Oxirgi kod | 10000 |
| `-t` | Threadlar soni | 10 |

**Muammo:** Serverdan 429 (Rate Limit) javob keladi.

---

## 5️⃣ otp_stealth.py — Stealth Mode

Har bir so'rovda **noyob brauzer identifikatsiyasi** bilan yuboradi.
429 xatolardan qochish maqsadida yaratilgan.

```bash
# Oddiy
python otp_stealth.py -e user@gmail.com -t 20

# Proxy bilan
python otp_stealth.py -e user@gmail.com -t 20 --proxy proxies.txt
```

| Argument | Tavsif | Standart |
|----------|--------|----------|
| `-e` | Email manzil | *majburiy* |
| `-t` | Threadlar soni | 10 |
| `--proxy` | Proxy fayli | — |

**Har bir so'rovda o'zgaradi:**

| Element | Xilma-xillik |
|---------|-------------|
| User-Agent | 30+ xil (Chrome, Firefox, Safari, Edge, Mobile) |
| IP manzil | 6 ta header orqali tasodifiy IP |
| Til | 15 xil (en, ru, uz, de, fr...) |
| Sec-CH-UA | 6 xil brauzer versiyasi |
| Platform | Windows, macOS, Linux, Android |
| Referer | Google, Yandex, Bing... |

---

## 6️⃣ otp_turbo.py — Async Turbo (ENG TEZ) ⚡

`aiohttp` asinxron kutubxona bilan ishlaydi. Threadlar o'rniga 
**event loop** — bir vaqtda 50-100 so'rov yuboradi.

```bash
# Standart (50 parallel so'rov)
python otp_turbo.py -e user@gmail.com

# Agressiv (100 parallel)
python otp_turbo.py -e user@gmail.com -c 100

# Ehtiyotkor (20 parallel)
python otp_turbo.py -e user@gmail.com -c 20
```

| Argument | Tavsif | Standart |
|----------|--------|----------|
| `-e` | Email manzil | *majburiy* |
| `-c` | Bir vaqtda nechta so'rov | 50 |
| `-b` | Boshlang'ich kod | 1 |
| `-g` | Oxirgi kod | 10000 |

**Tezlik taqqoslash:**

| Skript | Texnologiya | Tezlik | 10,000 kod |
|--------|-------------|--------|-----------|
| otp_bruteforce.py | threads | ~7 so'rov/s | ~24 daqiqa |
| otp_stealth.py | threads + spoofing | ~7 so'rov/s | ~24 daqiqa |
| **otp_turbo.py** | **async aiohttp** | **~30-50 so'rov/s** | **~3-5 daqiqa** |

---

## 🔍 Hujum jarayoni qisqacha

```
1. main.py → Sayt so'rovlarini monitoring qildim
                    ↓
2. API endpointlarni topdim (/auth/verify-email)
                    ↓
3. OTP 4 xonali va rate limiting yo'qligini aniqladim
                    ↓
4. otp_turbo.py → 0001-9999 kodlarni ~4 daqiqada sinab ko'rdim
                    ↓
5. To'g'ri OTP topildi → Token olindi → Akkauntga kirish
                    ↓
6. Admin emailini topib, uning akkauntiga ham xuddi shunday kirdim
                    ↓
7. Hech narsaga tegmay chiqdim → Responsible Disclosure
```

---

## 🛡️ Taklif qilinadigan yechimlar

| # | Yechim | Muhimlik |
|---|--------|----------|
| 1 | OTP urinishlarini **5 ta**ga cheklash | 🔴 Kritik |
| 2 | OTP kodini **6 xonali** qilish | 🔴 Kritik |
| 3 | **Rate limiting** — IP bo'yicha 5 so'rov/daqiqa | 🔴 Kritik |
| 4 | OTP muddatini **3-5 daqiqaga** qisqartirish | 🟡 Muhim |
| 5 | 3-chi urinishdan keyin **CAPTCHA** | 🟡 Muhim |
| 6 | Admin akkauntlarga **2FA** (Google Authenticator) | 🟡 Muhim |
| 7 | Yangi qurilmadan kirishda **email ogohlantirish** | 🟢 Tavsiya |
| 8 | **X-Forwarded-For** headerni ishonmaslik | 🟢 Tavsiya |
| 9 | **Anomaly detection** — shubhali faoliyatni aniqlash | 🟢 Tavsiya |

---

## 👤 Muallif

**Javokhir**
- Telegram: [@Javokhir00](https://t.me/Javokhir00)
- Maqsad: Responsible Disclosure — xavfsizlikni yaxshilash
