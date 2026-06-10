const { Pool } = require('pg');
require('dotenv').config();

/**
 * Database va jadvallarni yaratish uchun skript.
 * Ishga tushirish: npm run db:init
 */
async function initDatabase() {
  // Avval 'postgres' database ga ulanamiz, keyin auth_system ni yaratamiz
  const adminPool = new Pool({
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    database: 'postgres',
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
  });

  try {
    // Database mavjudligini tekshiramiz
    const dbCheck = await adminPool.query(
      "SELECT 1 FROM pg_database WHERE datname = $1",
      [process.env.DB_NAME]
    );

    if (dbCheck.rows.length === 0) {
      await adminPool.query(`CREATE DATABASE ${process.env.DB_NAME}`);
      console.log(`✅ "${process.env.DB_NAME}" database yaratildi`);
    } else {
      console.log(`ℹ️  "${process.env.DB_NAME}" database allaqachon mavjud`);
    }
  } catch (err) {
    console.error('❌ Database yaratishda xato:', err.message);
  } finally {
    await adminPool.end();
  }

  // Endi auth_system database ga ulanamiz va jadvallarni yaratamiz
  const appPool = new Pool({
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
  });

  try {
    // Users jadvali
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('✅ "users" jadvali yaratildi');

    // Refresh tokens jadvali
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS refresh_tokens (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        token VARCHAR(500) NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('✅ "refresh_tokens" jadvali yaratildi');

    console.log('\n🎉 Database muvaffaqiyatli sozlandi!');
  } catch (err) {
    console.error('❌ Jadvallarni yaratishda xato:', err.message);
  } finally {
    await appPool.end();
  }
}

initDatabase();
