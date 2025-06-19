// Ẩn thông báo flash sau 4 giây
document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 4000);
    });
});
function updateClock() {
  const now = new Date();
  const options = { weekday: 'long', day: '2-digit', month: '2-digit', year: 'numeric' };
  const timeString = now.toLocaleDateString('vi-VN', options) + " - " + now.toLocaleTimeString('vi-VN');
  document.getElementById('clock').textContent = timeString;
}
setInterval(updateClock, 1000);
updateClock();