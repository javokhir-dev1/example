const rateLimit = require('express-rate-limit');

/**
 * Umumiy rate limiter — barcha endpointlar uchun
 * 15 daqiqada 100 ta so'rov
 */
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 daqiqa
  max: 100,
  standardHeaders: true, // RateLimit-* headerlarni qaytaradi
  legacyHeaders: false,
  message: {
    success: false,
    message: 'Juda ko\'p so\'rov yubordingiz. 15 daqiqadan keyin qayta urinib ko\'ring.',
  },
});

/**
 * Auth endpointlar uchun qattiqroq limiter
 * Login/Register — 15 daqiqada 10 ta urinish
 */
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    success: false,
    message: 'Juda ko\'p urinish. 15 daqiqadan keyin qayta urinib ko\'ring.',
  },
});

module.exports = { globalLimiter, authLimiter };
