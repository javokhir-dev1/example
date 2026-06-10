const rateLimit = require('express-rate-limit');

/**
 * IP ni aniqlash funksiyasi
 * X-Forwarded-For, X-Real-IP yoki socket IP dan oladi
 */
function getClientIp(req) {
  const xff = req.headers['x-forwarded-for'];
  if (xff) {
    // Birinchi IP ni olamiz (virgul bilan ajratilgan bo'lishi mumkin)
    return xff.split(',')[0].trim();
  }
  return req.headers['x-real-ip'] || req.ip || req.socket.remoteAddress;
}

/**
 * Umumiy rate limiter — barcha endpointlar uchun
 * 15 daqiqada 100 ta so'rov (har bir IP uchun)
 */
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 daqiqa
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req) => getClientIp(req),
  message: {
    success: false,
    message: 'Juda ko\'p so\'rov yubordingiz. 15 daqiqadan keyin qayta urinib ko\'ring.',
  },
});

/**
 * Auth endpointlar uchun qattiqroq limiter
 * Login/Register — 15 daqiqada 10 ta urinish (har bir IP uchun)
 */
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req) => getClientIp(req),
  message: {
    success: false,
    message: 'Juda ko\'p urinish. 15 daqiqadan keyin qayta urinib ko\'ring.',
  },
});

module.exports = { globalLimiter, authLimiter };
