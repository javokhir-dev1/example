const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { validationResult } = require('express-validator');
const pool = require('../config/db');

/**
 * Access va Refresh tokenlarni yaratish
 */
function generateTokens(user) {
  const accessToken = jwt.sign(
    { id: user.id, username: user.username, email: user.email },
    process.env.JWT_SECRET,
    { expiresIn: process.env.JWT_EXPIRES_IN }
  );

  const refreshToken = jwt.sign(
    { id: user.id },
    process.env.JWT_REFRESH_SECRET,
    { expiresIn: process.env.JWT_REFRESH_EXPIRES_IN }
  );

  return { accessToken, refreshToken };
}

/**
 * POST /api/auth/register
 * Yangi foydalanuvchi ro'yxatdan o'tkazish
 */
async function register(req, res) {
  // Validatsiya xatolarini tekshiramiz
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      success: false,
      errors: errors.array().map((e) => e.msg),
    });
  }

  const { username, email, password } = req.body;

  try {
    // Email yoki username allaqachon mavjudligini tekshiramiz
    const existingUser = await pool.query(
      'SELECT id FROM users WHERE email = $1 OR username = $2',
      [email, username]
    );

    if (existingUser.rows.length > 0) {
      return res.status(409).json({
        success: false,
        message: 'Bu email yoki username allaqachon ro\'yxatdan o\'tgan',
      });
    }

    // Parolni hash qilamiz
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    // Foydalanuvchini database ga saqlaymiz
    const result = await pool.query(
      'INSERT INTO users (username, email, password) VALUES ($1, $2, $3) RETURNING id, username, email, created_at',
      [username, email, hashedPassword]
    );

    const newUser = result.rows[0];

    // Tokenlarni yaratamiz
    const { accessToken, refreshToken } = generateTokens(newUser);

    // Refresh token ni database ga saqlaymiz
    const refreshExpiresAt = new Date();
    refreshExpiresAt.setDate(refreshExpiresAt.getDate() + 7); // 7 kun

    await pool.query(
      'INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES ($1, $2, $3)',
      [newUser.id, refreshToken, refreshExpiresAt]
    );

    res.status(201).json({
      success: true,
      message: 'Muvaffaqiyatli ro\'yxatdan o\'tdingiz!',
      data: {
        user: {
          id: newUser.id,
          username: newUser.username,
          email: newUser.email,
          created_at: newUser.created_at,
        },
        tokens: {
          accessToken,
          refreshToken,
        },
      },
    });
  } catch (err) {
    console.error('Register xatosi:', err);
    res.status(500).json({
      success: false,
      message: 'Server xatosi. Qayta urinib ko\'ring.',
    });
  }
}

/**
 * POST /api/auth/login
 * Foydalanuvchini tizimga kiritish
 */
async function login(req, res) {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      success: false,
      errors: errors.array().map((e) => e.msg),
    });
  }

  const { email, password } = req.body;

  try {
    // Foydalanuvchini email bo'yicha topamiz
    const result = await pool.query('SELECT * FROM users WHERE email = $1', [
      email,
    ]);

    if (result.rows.length === 0) {
      return res.status(401).json({
        success: false,
        message: 'Email yoki parol noto\'g\'ri',
      });
    }

    const user = result.rows[0];

    // Parolni tekshiramiz
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({
        success: false,
        message: 'Email yoki parol noto\'g\'ri',
      });
    }

    // Tokenlarni yaratamiz
    const { accessToken, refreshToken } = generateTokens(user);

    // Eski refresh tokenlarni o'chiramiz va yangi saqlaymiz
    await pool.query('DELETE FROM refresh_tokens WHERE user_id = $1', [
      user.id,
    ]);

    const refreshExpiresAt = new Date();
    refreshExpiresAt.setDate(refreshExpiresAt.getDate() + 7);

    await pool.query(
      'INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES ($1, $2, $3)',
      [user.id, refreshToken, refreshExpiresAt]
    );

    res.json({
      success: true,
      message: 'Muvaffaqiyatli kirdingiz!',
      data: {
        user: {
          id: user.id,
          username: user.username,
          email: user.email,
        },
        tokens: {
          accessToken,
          refreshToken,
        },
      },
    });
  } catch (err) {
    console.error('Login xatosi:', err);
    res.status(500).json({
      success: false,
      message: 'Server xatosi. Qayta urinib ko\'ring.',
    });
  }
}

/**
 * POST /api/auth/refresh
 * Yangi access token olish (refresh token orqali)
 */
async function refreshToken(req, res) {
  const { refreshToken: token } = req.body;

  if (!token) {
    return res.status(400).json({
      success: false,
      message: 'Refresh token kerak',
    });
  }

  try {
    // Refresh token ni tekshiramiz
    const decoded = jwt.verify(token, process.env.JWT_REFRESH_SECRET);

    // Database da mavjudligini tekshiramiz
    const tokenRecord = await pool.query(
      'SELECT * FROM refresh_tokens WHERE token = $1 AND user_id = $2 AND expires_at > NOW()',
      [token, decoded.id]
    );

    if (tokenRecord.rows.length === 0) {
      return res.status(401).json({
        success: false,
        message: 'Refresh token noto\'g\'ri yoki muddati tugagan',
      });
    }

    // Foydalanuvchi ma'lumotlarini olamiz
    const userResult = await pool.query(
      'SELECT id, username, email FROM users WHERE id = $1',
      [decoded.id]
    );

    if (userResult.rows.length === 0) {
      return res.status(401).json({
        success: false,
        message: 'Foydalanuvchi topilmadi',
      });
    }

    const user = userResult.rows[0];

    // Yangi tokenlar yaratamiz
    const newTokens = generateTokens(user);

    // Eski refresh token ni yangilaymiz
    await pool.query('DELETE FROM refresh_tokens WHERE token = $1', [token]);

    const refreshExpiresAt = new Date();
    refreshExpiresAt.setDate(refreshExpiresAt.getDate() + 7);

    await pool.query(
      'INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES ($1, $2, $3)',
      [user.id, newTokens.refreshToken, refreshExpiresAt]
    );

    res.json({
      success: true,
      message: 'Token yangilandi!',
      data: {
        tokens: {
          accessToken: newTokens.accessToken,
          refreshToken: newTokens.refreshToken,
        },
      },
    });
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      // Muddati tugagan refresh token ni database dan o'chiramiz
      await pool.query('DELETE FROM refresh_tokens WHERE token = $1', [token]);
      return res.status(401).json({
        success: false,
        message: 'Refresh token muddati tugagan. Qayta kiring.',
      });
    }
    console.error('Refresh token xatosi:', err);
    res.status(500).json({
      success: false,
      message: 'Server xatosi',
    });
  }
}

/**
 * POST /api/auth/logout
 * Tizimdan chiqish (refresh token ni o'chirish)
 */
async function logout(req, res) {
  const { refreshToken: token } = req.body;

  try {
    if (token) {
      await pool.query('DELETE FROM refresh_tokens WHERE token = $1', [token]);
    }

    res.json({
      success: true,
      message: 'Muvaffaqiyatli chiqdingiz!',
    });
  } catch (err) {
    console.error('Logout xatosi:', err);
    res.status(500).json({
      success: false,
      message: 'Server xatosi',
    });
  }
}

/**
 * GET /api/auth/me
 * Joriy foydalanuvchi ma'lumotlarini olish (himoyalangan)
 */
async function getMe(req, res) {
  try {
    const result = await pool.query(
      'SELECT id, username, email, created_at, updated_at FROM users WHERE id = $1',
      [req.user.id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({
        success: false,
        message: 'Foydalanuvchi topilmadi',
      });
    }

    res.json({
      success: true,
      data: { user: result.rows[0] },
    });
  } catch (err) {
    console.error('GetMe xatosi:', err);
    res.status(500).json({
      success: false,
      message: 'Server xatosi',
    });
  }
}

module.exports = {
  register,
  login,
  refreshToken,
  logout,
  getMe,
};
