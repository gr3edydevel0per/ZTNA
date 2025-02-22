const express = require('express');
const jwt = require('jsonwebtoken');
const dotenv = require('dotenv');

dotenv.config();
const router = express.Router();

// Middleware to verify JWT
const verifyToken = (req, res, next) => {
    const token = req.headers['authorization'];
    if (!token) return res.status(403).json({ message: "No token provided" });

    jwt.verify(token.split(' ')[1], process.env.JWT_SECRET, (err, decoded) => {
        if (err) return res.status(401).json({ message: "Unauthorized" });
        req.user = decoded;
        next();
    });
};

// Device Authorization - Check device posture
router.post('/authorize', verifyToken, async (req, res) => {
    const { device_id, os, antivirus_installed } = req.body;

    if (!device_id || !os || antivirus_installed === undefined) {
        return res.status(400).json({ message: "Missing device information" });
    }

    // Example security posture check
    if (os !== 'Windows' || !antivirus_installed) {
        return res.status(403).json({ message: "Device does not meet security requirements" });
    }

    res.json({ message: "Device authorized" });
});

module.exports = router;
