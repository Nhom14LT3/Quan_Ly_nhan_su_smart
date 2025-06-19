document.getElementById('searchInput').addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    const tableRows = document.querySelectorAll('#employeeTable tbody tr');
    
    tableRows.forEach(row => {
        const username = row.cells[1].textContent.toLowerCase();
        if (username.includes(searchTerm)) {
            row.style.display = '';
            // Highlight matching text
            const usernameCell = row.cells[1];
            const originalText = usernameCell.textContent;
            if (searchTerm && searchTerm.length > 0) {
                const highlightedText = originalText.replace(
                    new RegExp(searchTerm, 'gi'), 
                    match => `<mark style="background: #fff3cd; padding: 2px 4px; border-radius: 3px;">${match}</mark>`
                );
                usernameCell.innerHTML = `<strong>${highlightedText}</strong>`;
            } else {
                usernameCell.innerHTML = `<strong>${originalText}</strong>`;
            }
        } else {
            row.style.display = 'none';
        }
    });
});

// // Smooth animations
// document.addEventListener('DOMContentLoaded', function() {
//     const rows = document.querySelectorAll('#employeeTable tbody tr');
//     rows.forEach((row, index) => {
//         row.style.opacity = '0';
//         row.style.transform = 'translateY(20px)';
//         setTimeout(() => {
//             row.style.transition = 'all 0.3s ease';
//             row.style.opacity = '1';
//             row.style.transform = 'translateY(0)';
//         }, index * 100);
//     });
// });

// ================== DÙNG CHO LIST EMPLOYEE ==================

// Tìm kiếm và highlight tên nhân viên trong bảng (LIST)
document.getElementById('searchInput').addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    const tableRows = document.querySelectorAll('#employeeTable tbody tr');
    
    tableRows.forEach(row => {
        const username = row.cells[1].textContent.toLowerCase();
        if (username.includes(searchTerm)) {
            row.style.display = '';
            // Highlight matching text
            const usernameCell = row.cells[1];
            const originalText = usernameCell.textContent;
            if (searchTerm && searchTerm.length > 0) {
                const highlightedText = originalText.replace(new RegExp(searchTerm, 'gi'), match => `<mark style="background: #fff3cd; padding: 2px 4px; border-radius: 3px;">${match}</mark>`);
                usernameCell.innerHTML = `<strong>${highlightedText}</strong>`;
            } else {
                usernameCell.innerHTML = `<strong>${originalText}</strong>`;
            }
        } else {
            row.style.display = 'none';
        }
    });
});

// Hiệu ứng xuất hiện mượt cho từng dòng bảng nhân viên (LIST)
document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('#employeeTable tbody tr');
    rows.forEach((row, index) => {
        row.style.opacity = '0';
        row.style.transform = 'translateY(20px)';
        setTimeout(() => {
            row.style.transition = 'all 0.3s ease';
            row.style.opacity = '1';
            row.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// ================== DÙNG CHO UPDATE EMPLOYEE ==================

// Validate form cập nhật nhân viên (UPDATE)
/* Đã có validateForm() và showError() ở phần dưới, nên không cần lặp lại validate submit ở đây */

// ================== DÙNG CHUNG (ADD & UPDATE) ==================

// Hiển thị thông báo lỗi cho input (CHUNG)
function showError(inputId, message) {
    const input = document.getElementById(inputId);
    input.style.borderColor = '#e74c3c';
    
    // Remove existing error message
    const existingError = input.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Add error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.color = '#e74c3c';
    errorDiv.style.fontSize = '0.85rem';
    errorDiv.style.marginTop = '5px';
    errorDiv.textContent = message;
    input.parentNode.appendChild(errorDiv);
    
    // Reset border color after 3 seconds
    setTimeout(() => {
        input.style.borderColor = '#e0e6ed';
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 3000);
}

// Hiệu ứng focus cho input (CHUNG)
document.querySelectorAll('.form-control').forEach(input => {
    input.addEventListener('focus', function() {
        this.parentNode.classList.add('focused');
    });
    input.addEventListener('blur', function() {
        this.parentNode.classList.remove('focused');
    });
});

// Highlight khi thay đổi giá trị input (CHUNG)
document.addEventListener('DOMContentLoaded', function() {
    const originalUsername = "{{ user.username }}";
    const originalRole = "{{ user.role }}";
    document.getElementById('username').addEventListener('input', function() {
        this.style.backgroundColor = (this.value !== originalUsername) ? '#fff3cd' : 'white';
    });
    document.getElementById('role').addEventListener('change', function() {
        this.style.backgroundColor = (this.value !== originalRole) ? '#fff3cd' : 'white';
    });
    document.getElementById('password').addEventListener('input', function() {
        this.style.backgroundColor = (this.value.length > 0) ? '#fff3cd' : 'white';
    });
});

// ================== DÙNG CHO ADD EMPLOYEE ==================

// (Nếu có validate riêng cho form thêm nhân viên thì đặt ở đây)

// ================== DÙNG CHUNG (ADD & UPDATE) ==================

// Toggle password visibility (hiện/ẩn mật khẩu) dùng cho cả form thêm và cập nhật

// document.addEventListener('DOMContentLoaded', function() {
//     const toggleBtn = document.querySelector('.password-toggle');
//     if (toggleBtn) {
//         toggleBtn.addEventListener('click', function() {
//             const passwordInput = document.getElementById('password');
//             const icon = document.getElementById('togglePasswordIcon');
//             if (passwordInput.type === 'password') {
//                 passwordInput.type = 'text';
//                 icon.classList.remove('fa-eye');
//                 icon.classList.add('fa-eye-slash');
//             } else {
//                 passwordInput.type = 'password';
//                 icon.classList.remove('fa-eye-slash');
//                 icon.classList.add('fa-eye');
//             }
//         });
//     }
// });
