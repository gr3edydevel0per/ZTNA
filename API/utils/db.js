require('dotenv').config();  // Load environment variables from .env file
const mysql = require('mysql2');

// Create a connection pool instead of a single connection
const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME,
  port: process.env.DB_PORT,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// Promisify the pool to use async/await
const promisePool = pool.promise();

// Function to execute a query
async function executeQuery(sql, params = []) {
  try {
    const [rows] = await promisePool.execute(sql, params);
    return rows;
  } catch (error) {
    throw new Error(`Database error: ${error.message}`);
  }
}

// Test database connection
async function testConnection() {
  try {
    await promisePool.execute('SELECT 1');
    console.log('Database connection successful');
    return true;
  } catch (error) {
    console.error('Database connection failed:', error);
    return false;
  }
}

// Export the function to be used in other files
module.exports = {
  executeQuery,
  testConnection
};
