const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { executeQuery } = require("../utils/db");
const router = express.Router();



router.get('/testConnection', async (req, res) => {
    try {
        const results = await executeQuery('SELECT 1 as test');
        res.json({ status: 'success', data: results });
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ status: 'error', message: error.message });
    }
});


router.post('/addUser', async (req, res) => {
    try {
        const { email, department_id } = req.body;
        
        // Validate input
        if (!email) return res.status(400).json({ status: 'error', message: 'Email is required' });
        if (!department_id) return res.status(400).json({ status: 'error', message: 'Department ID is required' });

        // Check if email already exists
        const existingUser = await executeQuery('SELECT * FROM users WHERE email = ?', [email]);
        if (existingUser.length > 0) {
            return res.status(400).json({ status: 'error', message: 'Email already registered' });
        }

        // Check if department exists
        const deptCheck = await executeQuery('SELECT id FROM departments d WHERE d.id = ?', [department_id]);
        if (deptCheck.length === 0) {
            return res.status(400).json({ status: 'error', message: 'Invalid department ID' });
        }

        // Generate and hash password
        const password = Math.random().toString(36).slice(-16);
        const hashedPassword = await bcrypt.hash(password, 10);
        
        // Insert user
        const query = 'INSERT INTO users (email, password, department_id) VALUES (?, ?, ?)';
        const result = await executeQuery(query, [email, hashedPassword, department_id]);
        
        // Get the created user
        const user = await executeQuery('SELECT * FROM users WHERE email = ?', [email]);
        console.log(user);
        
        console.log('Generated password:', password); // For debugging
        
        res.status(201).json({ 
            status: 'success',
            data: {
                user,
                password // Note: This should be sent via email in production
            }
        });
    } catch (error) {
        console.error('Error creating user:', error);
        res.status(500).json({ status: 'error', message: error.message });
    }
});

// User Login
router.post('/login', async (req, res) => {
    console.log("req recieved");
    try {
        const { email, password } = req.body;

        // Validate input
        if (!email || !password) {
            return res.status(400).json({ 
                status: 'error', 
                message: "Email and password are required" 
            });
        }

        // Get user by email
        const users = await executeQuery(
            'SELECT  email, password, uuid, department_id FROM users WHERE email = ?', 
            [email]
        );

        // Check if user exists
        if (users.length === 0) {
            return res.status(401).json({ 
                status: 'error', 
                message: "Invalid credentials" 
            });
        }

        const user = users[0];

        // Verify password
        const validPassword = await bcrypt.compare(password, user.password);
        if (!validPassword) {
            return res.status(401).json({ 
                status: 'error', 
                message: "Invalid credentials" 
            });
        }

        // Generate JWT token
        const token = jwt.sign(
            { 
                uuid: user.uuid, 
                email: user.email,
                department_id: user.department_id
            }, 
            process.env.JWT_SECRET, 
            { expiresIn: '24h' }
        );

        res.json({ 
            status: 'success',
            data: {
                token,
                user: {
                    email: user.email,
                    uuid: user.uuid,
                    department_id: user.department_id
                }
            }
        });
    } catch (error) {
        console.error('Error during login:', error);
        res.status(500).json({ 
            status: 'error', 
            message: "Server error", 
            details: error.message 
        });
    }
});

module.exports = router;
