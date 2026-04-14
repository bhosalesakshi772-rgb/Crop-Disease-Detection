// Image preview and form handling
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const fileInfo = document.querySelector('.file-info');
    const submitBtn = document.getElementById('submitBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');

    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImg.src = e.target.result;
                    imagePreview.style.display = 'block';
                    fileInfo.innerHTML = `<i class="fas fa-check-circle text-success me-2"></i>
                                       ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Form submission with loading state
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function() {
            submitBtn.disabled = true;
            loadingSpinner.classList.remove('d-none');
            submitBtn.innerHTML = 'Analyzing... Please wait';
        });
    }

    // Animate progress bars on result page
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.getAttribute('style').match(/width: (\d+)%/)[1];
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width + '%';
        }, 500);
    });

    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Add loading overlay for predictions (if needed)
function showLoading() {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="text-center">
            <div class="spinner me-3"></div>
            <div class="d-inline-block">
                <div class="h4 mb-2">Analyzing Image</div>
                <div class="text-muted">Deep Learning Model Processing...</div>
                <div class="spinner-border spinner-border-sm text-success mt-2" style="width: 2rem; height: 2rem;"></div>
            </div>
        </div>
    `;
    document.body.appendChild(overlay);
    return overlay;
}

function hideLoading(overlay) {
    if (overlay) {
        overlay.remove();
    }
}

