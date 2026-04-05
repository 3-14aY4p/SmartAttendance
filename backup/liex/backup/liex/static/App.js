document.addEventListener('DOMContentLoaded', () => {
  // movement on navigation
  const topbar = document.querySelector('.topbar');
  const links = Array.from(document.querySelectorAll('[data-screen-link]'));

  if (topbar && links.length) {
    let indicator = topbar.querySelector('.topbar-indicator');

    if (!indicator) {
      indicator = document.createElement('div');
      indicator.className = 'topbar-indicator';
      topbar.prepend(indicator);
    }

    const getActiveLink = () => topbar.querySelector('.topbar-link.active') || links[0];

    const setIndicator = (link, animate = true) => {
      const topbarRect = topbar.getBoundingClientRect();
      const linkRect = link.getBoundingClientRect();

      if (!animate) {
        indicator.style.transition = 'none';
      }

      indicator.style.left = `${linkRect.left - topbarRect.left}px`;
      indicator.style.width = `${linkRect.width}px`;

      if (!animate) {
        requestAnimationFrame(() => {
          indicator.style.transition = 'left 0.24s ease, width 0.24s ease';
        });
      }
    };

    setIndicator(getActiveLink(), false);

    window.addEventListener('resize', () => {
      setIndicator(getActiveLink(), false);
    });

    links.forEach(link => {
      link.addEventListener('click', event => {
        const href = link.getAttribute('href');

        if (!href || href === '#') {
          event.preventDefault();
          return;
        }

        event.preventDefault();
        setIndicator(link, true);

        window.setTimeout(() => {
          window.location.href = href;
        }, 215);
      });
    });
  }

  const studentIdEl = document.getElementById('student-id');
  const studentNameEl = document.getElementById('student-name');
  const scanStatusEl = document.getElementById('scan-status');
  const previewStudentIdEl = document.getElementById('preview-student-id');
  const previewStudentNameEl = document.getElementById('preview-student-name');
  const previewStatusEl = document.getElementById('preview-status');
  const previewPlaceholderEl = document.getElementById('id-preview-placeholder');

  if (!studentIdEl || !studentNameEl || !scanStatusEl) {
    return;
  }

  const setStatusClass = statusText => {
    scanStatusEl.classList.remove('status-success', 'status-warning', 'status-danger');

    const value = (statusText || '').toLowerCase();

    if (value.includes('recorded')) {
      scanStatusEl.classList.add('status-success');
    } else if (
      value.includes('hold') ||
      value.includes('waiting') ||
      value.includes('scan')
    ) {
      scanStatusEl.classList.add('status-warning');
    } else if (
      value.includes('not found') ||
      value.includes('error') ||
      value.includes('failed') ||
      value.includes('already')
    ) {
      scanStatusEl.classList.add('status-danger');
    }
  };

  const updateCameraData = async () => {
    try {
      // gets backend data
      const response = await fetch('/scan_data', {
        cache: 'no-store'
      });

      if (!response.ok) {
        throw new Error('Failed to fetch scan data');
      }

      const data = await response.json();

      const studentId = data.student_id && data.student_id.trim() !== '' ? data.student_id : 'Waiting for scan...';
      const studentName = data.student_name && data.student_name.trim() !== '' ? data.student_name : 'Waiting for scan...';
      const status = data.status && data.status.trim() !== '' ? data.status : 'Waiting for scan...';

      // updates UI
      studentIdEl.textContent = studentId;
      studentNameEl.textContent = studentName;
      scanStatusEl.textContent = status;

      if (previewStudentIdEl) {
        previewStudentIdEl.textContent = data.student_id && data.student_id.trim() !== '' ? data.student_id : '---';
      }

      if (previewStudentNameEl) {
        previewStudentNameEl.textContent = data.student_name && data.student_name.trim() !== '' ? data.student_name : '---';
      }

      if (previewStatusEl) {
        previewStatusEl.textContent = status;
      }

      if (previewPlaceholderEl) {
        if (data.student_id && data.student_id.trim() !== '') {
          previewPlaceholderEl.innerHTML = `
            <i class="bi bi-person-badge"></i>
            <span>ID detected</span>
          `;
        } else {
          previewPlaceholderEl.innerHTML = `
            <i class="bi bi-person-vcard"></i>
            <span>No scan yet</span>
          `;
        }
      }
    // changes status color
      setStatusClass(status);
    } catch (error) {
      studentIdEl.textContent = 'Connection error';
      studentNameEl.textContent = 'Connection error';
      scanStatusEl.textContent = 'Could not load scan data';
      setStatusClass('Could not load scan data');

      if (previewStudentIdEl) {
        previewStudentIdEl.textContent = '---';
      }

      if (previewStudentNameEl) {
        previewStudentNameEl.textContent = '---';
      }

      if (previewStatusEl) {
        previewStatusEl.textContent = 'Could not load scan data';
      }

      if (previewPlaceholderEl) {
        previewPlaceholderEl.innerHTML = `
          <i class="bi bi-wifi-off"></i>
          <span>Connection error</span>
        `;
      }
    }
  };

  updateCameraData();
  window.setInterval(updateCameraData, 500);
});
