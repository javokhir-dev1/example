const jwt = require('jsonwebtoken');

/**
 * JWT token tekshirish middleware
 * Authorization header dan Bearer token ni oladi va tekshiradi
 */
function authMiddleware(req, res, next) {
  const authHeader = req.headers['authorization'];

  if (!authHeader) {
    return res.status(401).json({
      success: false,
      message: 'Token topilmadi. Authorization header kerak.',
    });
  }

  // "Bearer <token>" formatini tekshiramiz
  const parts = authHeader.split(' ');
  if (parts.length !== 2 || parts[0] !== 'Bearer') {
    return res.status(401).json({
      success: false,
      message: 'Token formati noto\'g\'ri. Format: Bearer <token>',
    });
  }

  const token = parts[1];

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded; // { id, username, email }
    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return res.status(401).json({
        success: false,
        message: 'Token muddati tugagan. Yangi token oling.',
      });
    }
    return res.status(401).json({
      success: false,
      message: 'Token noto\'g\'ri.',
    });
  }
}

module.exports = authMiddleware;
