# 🔐 Auth System Backend

Express.js + PostgreSQL + JWT bilan sodda autentifikatsiya tizimi.

## 📁 Loyiha tuzilishi

```
backend/
├── src/
│   ├── config/
│   │   ├── db.js          # PostgreSQL ulanish
│   │   └── initDb.js      # Database va jadvallarni yaratish
│   ├── controllers/
│   │   └── authController.js  # Auth logikasi
│   ├── middleware/
│   │   ├── auth.js        # JWT tekshirish middleware
│   │   └── validators.js  # Input validatsiya
│   ├── routes/
│   │   └── authRoutes.js  # API routelar
│   └── server.js          # Asosiy server fayl
├── .env                   # Environment o'zgaruvchilar
├── .gitignore
└── package.json
```

## 🚀 Ishga tushirish

### 1. PostgreSQL o'rnatilgan bo'lishi kerak

### 2. `.env` faylni sozlang

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=auth_system
DB_USER=postgres
DB_PASSWORD=sizning_parolingiz
JWT_SECRET=juda_maxfiy_kalit
JWT_REFRESH_SECRET=refresh_uchun_maxfiy_kalit
```

### 3. Dependencylarni o'rnating

```bash
npm install
```

### 4. Database yarating

```bash
npm run db:init
```

### 5. Serverni ishga tushiring

```bash
npm run dev
```

Server `http://localhost:5000` da ishlaydi.

---

## 📋 API Endpoints

### Ro'yxatdan o'tish
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "john",
  "email": "john@example.com",
  "password": "123456"
}
```

### Kirish
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "123456"
}
```

### Token yangilash
```
POST /api/auth/refresh
Content-Type: application/json

{
  "refreshToken": "sizning_refresh_tokeningiz"
}
```

### Chiqish
```
POST /api/auth/logout
Content-Type: application/json

{
  "refreshToken": "sizning_refresh_tokeningiz"
}
```

### Profil (himoyalangan)
```
GET /api/auth/me
Authorization: Bearer sizning_access_tokeningiz
```

---

## 🔑 Token tizimi

- **Access Token** — muddati 1 soat, har bir so'rovda `Authorization: Bearer <token>` header da yuboriladi
- **Refresh Token** — muddati 7 kun, access token muddati tugaganda yangi token olish uchun ishlatiladi
