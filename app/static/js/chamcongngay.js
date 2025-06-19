document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('face-video');
    const placeholder = document.getElementById('face-placeholder');
    const startBtn = document.getElementById('start-btn');
    const resultPopup = document.getElementById('result-popup');
    const resultMessage = document.getElementById('result-message');
    let stream = null;

    function autoCaptureAndSend() {
        if (!video.srcObject) return;
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        const imageData = canvas.toDataURL('image/png');

        fetch('/api/face_recognition', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({image: imageData})
        })
        .then(res => res.json())
        .then(data => {
            showResultPopup(data.success, data.message);
            // Tắt camera sau khi chấm công
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
                video.style.display = 'none';
                placeholder.style.display = 'block';
                startBtn.style.display = 'inline-block';
            }
        })
        .catch(err => {
            showResultPopup(false, 'Có lỗi khi gửi ảnh lên server!');
        });
    }

    startBtn.addEventListener('click', function(e) {
        e.preventDefault();
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(s => {
                stream = s;
                video.srcObject = stream;
                video.style.display = 'block';
                placeholder.style.display = 'none';
                startBtn.style.display = 'none';
                // Đợi camera ổn định rồi tự động chụp và gửi ảnh (ví dụ sau 11 giây)
                setTimeout(autoCaptureAndSend, 2000);
            })
            .catch(err => {
                alert('Không thể truy cập camera: ' + err);
            });
    });
});
function showResultPopup(success, message) {
    const popup = document.getElementById('result-popup-center');
    const icon = document.getElementById('result-icon-center');
    const msg = document.getElementById('result-message-center');
    popup.className = 'result-popup-center active ' + (success ? 'success' : 'fail');
    if(success) {
        icon.innerHTML = `<svg width="64" height="64" viewBox="0 0 64 64">
            <circle cx="32" cy="32" r="30" fill="#fff" stroke="#38d430" stroke-width="4"/>
            <polyline points="18,34 28,46 46,20" fill="none" stroke="#38d430" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`;
        icon.className = 'icon glow-success';
    } else {
        icon.innerHTML = `<svg width="64" height="64" viewBox="0 0 64 64">
            <circle cx="32" cy="32" r="30" fill="#fff" stroke="#ff3b3b" stroke-width="4"/>
            <line x1="20" y1="20" x2="44" y2="44" stroke="#ff3b3b" stroke-width="6" stroke-linecap="round"/>
            <line x1="44" y1="20" x2="20" y2="44" stroke="#ff3b3b" stroke-width="6" stroke-linecap="round"/>
        </svg>`;
        icon.className = 'icon glow-fail';
    }
    msg.innerText = message;
    popup.style.display = 'flex';
    setTimeout(() => {
        popup.style.display = 'none';
        popup.className = 'result-popup-center';
        if(success) location.reload(); // Thêm dòng này để reload khi thành công
    }, 3000);
}