const express = require('express');
const jwt = require('jsonwebtoken');
const dotenv = require('dotenv');
const { executeQuery } = require("../utils/db");
const e = require('express');

dotenv.config();
const router = express.Router();




// Middleware to verify JWT  : to check if the user is authenticated and remove unauthorized users
const verifyToken = (req, res, next) => {
    const token = req.headers['authorization'];
    if (!token) return res.status(403).json({ message: "No token provided" });

    jwt.verify(token.split(' ')[1], process.env.JWT_SECRET, (err, decoded) => {
        if (err) return res.status(401).json({ message: "Unauthorized" });
        req.user = decoded;
        next();
    });
};


// Link a device to a user : If the user logged in with a device, the device is trusted by the organization
// if the device is not linked to any user, then the device can be used by any user

router.put('/linker/:u_id/:d_id', verifyToken, async (req, res) => {
    try {
        const { u_id, d_id } = req.params;
        console.log(u_id, d_id);
        // Check if device exists
        const device = await executeQuery(
            'SELECT id FROM trusted_devices WHERE device_id = ?',
            [d_id]
        );
        const user = await executeQuery(
            'SELECT id FROM users WHERE uuid = ?',
            [u_id]
        );
        if (device.length === 0) {
            return res.status(404).json({
                status: 'error',
                message: 'Device not found'
            });
        }

        // Check if user is already linked to this device
        const existingLink = await executeQuery(
            'SELECT id FROM userDeviceMapping WHERE u_id = ? AND d_id = ?',
            [user[0].id, device[0].id]
        );  
        if (existingLink.length > 0) {
            return res.status(400).json({
                status: 'error',
                message: 'Device already linked to this user'
            });
        }
        
        // Insert new link
        const result = await executeQuery(
            'INSERT INTO userDeviceMapping (u_id, d_id) VALUES (?, ?)',
            [user[0].id, device[0].id]
        );
        console.log(result);
        res.status(201).json({
            status: 'success',
            message: 'Device linked successfully',
            data: {
                id: result.insertId,
                u_id: user[0].id,
                d_id: device[0].id
            }
        });
    } catch (error) {
        console.error('Error linking device:', error);
        res.status(500).json({
            status: 'error',
            message: 'Server error',
            details: error.message
        });
    }
});



// Register a new device : Done by Organization Admin : Maintaining a list of trusted devices
router.post('/register', verifyToken, async (req, res) => {
    try {
        const {
            device_id,
            device_fingerprint,
            device_name,
            device_type,
            device_os,
            hardware_fingerprint
        } = req.body;

        // Validate required fields
        if (!device_id || !device_fingerprint || !device_name || !device_type || !device_os || !hardware_fingerprint) {
            return res.status(400).json({
                status: 'error',
                message: 'All device fields are required'
            });
        }

        // Validate device type
        if (!['desktop', 'laptop'].includes(device_type)) {
            return res.status(400).json({
                status: 'error',
                message: 'Invalid device type. Must be either "desktop" or "laptop"'
            });
        }

        // Check if device already exists
        const existingDevice = await executeQuery(
            'SELECT id FROM trusted_devices WHERE device_id = ? OR device_fingerprint = ? OR hardware_fingerprint = ?',
            [device_id, device_fingerprint, hardware_fingerprint]
        );

        if (existingDevice.length > 0) {
            return res.status(400).json({
                status: 'error',
                message: 'Device already registered'
            });
        }

        // Insert new device
        const result = await executeQuery(
            'INSERT INTO trusted_devices (device_id, device_fingerprint, device_name, device_type, device_os, hardware_fingerprint) VALUES (?, ?, ?, ?, ?, ?)',
            [device_id, device_fingerprint, device_name, device_type, device_os, hardware_fingerprint]
        );

        res.status(201).json({
            status: 'success',
            message: 'Device registered successfully',
            data: {
                id: result.insertId,
                device_id,
                device_name,
                device_type,
                device_os
            }
        });
    } catch (error) {
        console.error('Error registering device:', error);
        res.status(500).json({
            status: 'error',
            message: 'Server error',
            details: error.message
        });
    }
});


// check if the device is trusted by the organization
// also check whether the deice fingerprint is tampered or not
router.post('/isTrusted', verifyToken, async (req, res) => {
    try {
        const deviceData = req.body;
        console.log(deviceData);
        const device = await executeQuery(
            'SELECT id FROM trusted_devices WHERE device_id = ?',
            [deviceData.device_id]
        );
        if (device.length === 0) {
            return res.status(404).json({
                status: 'error',
                message: 'Device not found'
            });
        }

        res.status(200).json({
            status: 'success',
            message: 'Device is trusted'
        });
    } catch (error) {
        console.error('Error checking trust:', error);
        res.status(500).json({
            status: 'error',
            message: 'Server error',
            details: error.message
        });
    }
});



// check whether the deivce is authorized for the user or not
router.post('/isAuthorized', verifyToken, async (req, res) => {
    try {
       const  deviceData = req.body;

        const device = await executeQuery(
            'SELECT id FROM trusted_devices WHERE device_id = ?',
            [deviceData.device_id]
        );
        const user = await executeQuery(
            'SELECT id FROM users WHERE uuid = ?',
            [deviceData.uuid]
        );

        const mapper = await executeQuery(
            'SELECT id FROM userDeviceMapping WHERE d_id = ? AND u_id = ?',
            [device[0].id, user[0].id]
        );
        if (mapper.length === 0) {
            return res.status(404).json({   
                status: 'error',
                message: 'Device is not authorized'
            });
        }
        res.status(200).json({
            status: 'success',
            message: 'Device is authorized'
        });
    } catch (error) {
        console.error('Error checking trust:', error);
        res.status(500).json({
            status: 'error',
            message: 'Server error',
            details: error.message
        });
    }
});



module.exports = router;
