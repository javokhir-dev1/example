const { body } = require('express-validator');

const registerValidation = [
  body('username')
    .trim()
    .isLength({ min: 3, max: 50 })
    .withMessage('Username 3 dan 50 gacha belgi bo\'lishi kerak')
    .isAlphanumeric()
    .withMessage('Username faqat harf va raqamlardan iborat bo\'lishi kerak'),

  body('email')
    .trim()
    .isEmail()
    .withMessage('Email formati noto\'g\'ri')
    .normalizeEmail(),

  body('password')
    .isLength({ min: 6 })
    .withMessage('Parol kamida 6 ta belgi bo\'lishi kerak'),
];

const loginValidation = [
  body('email')
    .trim()
    .isEmail()
    .withMessage('Email formati noto\'g\'ri')
    .normalizeEmail(),

  body('password')
    .notEmpty()
    .withMessage('Parol kiritilishi kerak'),
];

module.exports = {
  registerValidation,
  loginValidation,
};
