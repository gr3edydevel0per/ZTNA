require('dotenv').config();  // Load environment variables from .env file
const mysql = require('mysql2');

// Read values from environment variables
const dbHost = process.env.DB_HOST || 'localhost';
const dbUser = process.env.DB_USER || 'root';
const dbPass = process.env.DB_PASS || 'root';
const dbName = process.env.DB_NAME || 'ztna';
const dbPort = process.env.DB_PORT || 3306;

// Create a connection to the database
const connection = mysql.createConnection({
  host: dbHost,
  user: dbUser,
  password: dbPass,
  database: dbName,
  port: dbPort
});

// Function to execute a query
function executeQuery(sql) {
  return new Promise((resolve, reject) => {
    connection.query(sql, (err, results) => {
      if (err) {
        reject('Error executing query: ' + err);
      } else {
        resolve(results);
      }
    });
  });
}

// Export the function to be used in other files
module.exports = {
  executeQuery
};
