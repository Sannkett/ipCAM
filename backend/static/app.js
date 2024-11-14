// // Make sure this is set to your backend server URL
// //running code on local host
// const socket = io('http://localhost:5002');

// const videoFeed = document.getElementById('video-feed');
// const goLiveBtn = document.getElementById('go-live-btn');
// const stopLiveBtn = document.getElementById('stop-live-btn');

// `
// goLiveBtn.addEventListener('click', () => {
//     console.log("Go Live button clicked. Requesting stream to start...");
//     socket.emit('start_stream');
//     goLiveBtn.style.display = 'none';
//     stopLiveBtn.style.display = 'inline';
// });

// 
// stopLiveBtn.addEventListener('click', () => {
//     console.log("Stop Live button clicked. Requesting stream to stop...");
//     socket.emit('stop_stream');
//     goLiveBtn.style.display = 'inline';
//     stopLiveBtn.style.display = 'none';
// });

//
// socket.on('video_frame', (frame) => {
//     console.log("Received a video frame");
//     videoFeed.src = `data:image/jpeg;base64,${frame}`;
// });

//
// socket.on('connect_error', (err) => {
//     console.error("Socket connection error:", err.message);
// });

//
// socket.on('connect', () => {
//     console.log("Connected to Socket.io server");
// });

// socket.on('disconnect', () => {
//     console.warn("Disconnected from Socket.io server");
// });



// //working code with ngrok
// const socket = io('your_ngrok_link');

// const videoFeed = document.getElementById('video-feed');
// const goLiveBtn = document.getElementById('go-live-btn');
// const stopLiveBtn = document.getElementById('stop-live-btn');

// 
// goLiveBtn.addEventListener('click', () => {
//     console.log("Go Live button clicked. Requesting stream to start...");
//     socket.emit('start_stream');
//     goLiveBtn.style.display = 'none';
//     stopLiveBtn.style.display = 'inline';
// });

// 
// stopLiveBtn.addEventListener('click', () => {
//     console.log("Stop Live button clicked. Requesting stream to stop...");
//     socket.emit('stop_stream');
//     goLiveBtn.style.display = 'inline';
//     stopLiveBtn.style.display = 'none';
// });

// 
// socket.on('video_frame', (frame) => {
//     console.log("Received a video frame");
//     videoFeed.src = `data:image/jpeg;base64,${frame}`;
// });

// 
// socket.on('connect_error', (err) => {
//     console.error("Socket connection error:", err.message);
// });

// 
// socket.on('connect', () => {
//     console.log("Connected to Socket.io server");
// });

// socket.on('disconnect', () => {
//     console.warn("Disconnected from Socket.io server");
// });

const socket = io('http://localhost:5002');

const videoFeed = document.getElementById('video-feed');
const goLiveBtn = document.getElementById('go-live-btn');
const stopLiveBtn = document.getElementById('stop-live-btn');
const snapshotBtn = document.getElementById('snapshot-btn');
const downloadPdfBtn = document.getElementById('download-pdf-btn');
const snapshotList = document.getElementById('snapshot-list');
const projectNameInput = document.getElementById('project-name');

let snapshots = []; 

goLiveBtn.addEventListener('click', () => {
    console.log("Go Live button clicked. Requesting stream to start...");
    socket.emit('start_stream');
    goLiveBtn.style.display = 'none';
    stopLiveBtn.style.display = 'inline';
});

stopLiveBtn.addEventListener('click', () => {
    console.log("Stop Live button clicked. Requesting stream to stop...");
    socket.emit('stop_stream');
    goLiveBtn.style.display = 'inline';
    stopLiveBtn.style.display = 'none';
});

socket.on('video_frame', (frame) => {
    console.log("Received a video frame");
    videoFeed.src = `data:image/jpeg;base64,${frame}`;
});

snapshotBtn.addEventListener('click', () => {
    console.log("Snapshot button clicked");

    fetch('http://localhost:5002/take_snapshot', { 
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.filename) {
            console.log(`Snapshot saved as ${data.filename}`);

            const snapshotURL = `http://localhost:5002/snapshot/${data.filename}`;
            
            const snapshotItem = document.createElement('img');
            snapshotItem.src = snapshotURL;
            snapshotItem.alt = 'Snapshot';
            snapshotItem.classList.add('snapshot');
            
            snapshotList.appendChild(snapshotItem);

            snapshots.push(snapshotURL);
        } else {
            alert('Failed to take snapshot');
        }
    })
    .catch(error => {
        console.error('Error taking snapshot:', error);
    });
});

downloadPdfBtn.addEventListener('click', () => {
    console.log("Download PDF button clicked");

    if (snapshots.length === 0) {
        alert("No snapshots available. Please take at least one snapshot before downloading the PDF.");
        return; 
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    let projectName = projectNameInput.value.trim() || "Project"; 

    let yPosition = 20; 
    
    snapshots.forEach((snapshotURL, index) => {
        doc.addImage(snapshotURL, 'JPEG', 10, yPosition, 180, 100); 
        yPosition += 110; 
        if (index < snapshots.length - 1) {
            doc.addPage(); 
        }
    });

    doc.save(`${projectName}.pdf`);
});
