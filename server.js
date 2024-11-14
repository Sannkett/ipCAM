const express = require('express');
const path = require('path');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

app.use('/static', express.static(path.join(__dirname, 'backend/static')));


app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'backend/templates', 'index.html'));
});

http.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});

io.on('connection', (socket) => {
    console.log(`User connected: ${socket.id}`);

    socket.on('start_stream', () => {
        console.log(`Start stream requested by ${socket.id}`);
    });

    socket.on('stop_stream', () => {
        console.log(`Stop stream requested by ${socket.id}`);
    });

    socket.on('disconnect', () => {
        console.log(`User disconnected: ${socket.id}`);
    });
});
