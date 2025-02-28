const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const dotenv = require('dotenv');
const { executeQuery } = require("../utils/db");

dotenv.config();
const router = express.Router();




router.get('/testConnection', async (req,res)=>{
    try {
        // Example SQL query (change to your own SQL)
        const query = 'SELECT * FROM users';
        
        // Execute the query and get the results
        const results = await executeQuery(query);
        
        // Log the results
        console.log('Query results: ', results);
        res.json(results)
      } catch (error) {
        console.error('Error: ', error);
      }

})

// User Login
router.post('/login', async (req, res) => {
    const { username, password} = req.body;

    // Validate input fields
    if (!username || !password) {
        return res.status(400).json({ message: "Username and password are required" });
    }

    try {
        // Query to get the user by username
        const query = 'SELECT * FROM users WHERE username = ?';
        const users = await executeQuery(query, [username]);

        // If no user is found
        if (users.length === 0) {
            return res.status(401).json({ message: "Invalid credentials" });
        }

        const user = users[0];

        // Compare the hashed password with the input password
        const validPassword = await bcrypt.compare(password, user.password);
        if (!validPassword) {
            return res.status(401).json({ message: "Invalid credentials" });
        }

        // Generate a JWT token
        const token = jwt.sign(
            { uuid: user.uuid, username: user.username }, 
            process.env.JWT_SECRET, 
            { expiresIn: '1h' }
        );

        // Send the token back as a response
        res.json({ token });

    } catch (error) {
        console.error('Error during login:', error);
        res.status(500).json({ message: "Server error", error });
    }
});


module.exports = router;
