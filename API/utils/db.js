require('dotenv').config();  // Load environment variables from .env file
const mysql = require('mysql2');

// Read values from environment variables
const dbHost = process.env.DB_HOST ; 
const dbUser = process.env.DB_USER ;
const dbPass = process.env.DB_PASS ;
const dbName = process.env.DB_NAME ;
const dbPort = process.env.DB_PORT ;

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
