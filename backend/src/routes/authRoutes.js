const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');
const authMiddleware = require('../middleware/auth');
const { registerValidation, loginValidation } = require('../middleware/validators');
const { authLimiter } = require('../middleware/rateLimiter');

// Ochiq routelar (token kerak emas)
router.post('/register', authLimiter, registerValidation, authController.register);
router.post('/login', authLimiter, loginValidation, authController.login);
router.post('/refresh', authController.refreshToken);
router.post('/logout', authController.logout);

// Himoyalangan routelar (token kerak)
router.get('/me', authMiddleware, authController.getMe);

module.exports = router;
