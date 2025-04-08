const express = require('express');
const bodyParser = require('body-parser');
const dotenv = require('dotenv');

const userRoutes = require('./routes/userRoutes');
const deviceRoutes = require('./routes/deviceRoutes');

dotenv.config();
const cors = require('cors');
const app = express();

app.use(cors());

const PORT = process.env.PORT || 5069;

// Middleware



app.use(bodyParser.json());

// Routes
app.use('/api/users', userRoutes);
app.use('/api/devices', deviceRoutes);

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on 0.0.0.0:${PORT}`);
  });
  