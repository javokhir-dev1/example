const express = require('express');
const cors = require('cors');
require('dotenv').config();

const authRoutes = require('./routes/authRoutes');
const { globalLimiter } = require('./middleware/rateLimiter');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.set('trust proxy', true); // X-Forwarded-For headerni ishonchli deb qabul qilish
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(globalLimiter);

// Routes
app.use('/api/auth', authRoutes);

// Asosiy route
app.get('/', (req, res) => {
  res.json({
    success: true,
    message: '🔐 Auth System API ishlayapti!',
    endpoints: {
      register: 'POST /api/auth/register',
      login: 'POST /api/auth/login',
      refresh: 'POST /api/auth/refresh',
      logout: 'POST /api/auth/logout',
      me: 'GET /api/auth/me (token kerak)',
    },
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: `${req.method} ${req.url} topilmadi`,
  });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error('Server xatosi:', err);
  res.status(500).json({
    success: false,
    message: 'Ichki server xatosi',
  });
});

app.listen(PORT, () => {
  console.log(`\n🚀 Server ishga tushdi: http://localhost:${PORT}`);
  console.log(`📋 API endpoints: http://localhost:${PORT}/api/auth\n`);
});

module.exports = app;
