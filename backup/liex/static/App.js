document.addEventListener("DOMContentLoaded", () => {
  const topbar = document.querySelector(".topbar");
  const links = Array.from(document.querySelectorAll("[data-screen-link]"));

  if (topbar && links.length) {
    let indicator = topbar.querySelector(".topbar-indicator");

    if (!indicator) {
      indicator = document.createElement("div");
      indicator.className = "topbar-indicator";
      topbar.prepend(indicator);
    }

    const getActiveLink = () => topbar.querySelector(".topbar-link.active") || links[0];

    const setIndicator = (link, animate = true) => {
      const topbarRect = topbar.getBoundingClientRect();
      const linkRect = link.getBoundingClientRect();

      if (!animate) {
        indicator.style.transition = "none";
      }

      indicator.style.left = `${linkRect.left - topbarRect.left}px`;
      indicator.style.width = `${linkRect.width}px`;

      if (!animate) {
        requestAnimationFrame(() => {
          indicator.style.transition = "left 0.22s ease, width 0.22s ease";
        });
      }
    };

    setIndicator(getActiveLink(), false);

    window.addEventListener("resize", () => {
      setIndicator(getActiveLink(), false);
    });

    links.forEach((link) => {
      link.addEventListener("click", (event) => {
        const href = link.getAttribute("href");

        if (!href || href === "#") {
          event.preventDefault();
          return;
        }

        event.preventDefault();
        setIndicator(link, true);

        setTimeout(() => {
          window.location.href = href;
        }, 180);
      });
    });
  }

  const studentIdEl = document.getElementById("student-id");
  const studentNameEl = document.getElementById("student-name");
  const scanStatusEl = document.getElementById("scan-status");
  const cameraDateTimeBar = document.getElementById("camera-datetime-bar");

  const setClockBar = () => {
    if (!cameraDateTimeBar) return;

    const now = new Date();
    const weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const months = [
      "January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];

    const hours24 = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const suffix = hours24 >= 12 ? "PM" : "AM";
    const hours12 = ((hours24 + 11) % 12) + 1;

    cameraDateTimeBar.textContent =
      `${months[now.getMonth()].toUpperCase()} ${now.getDate()}, ${now.getFullYear()} : ${weekdays[now.getDay()].toUpperCase()}  ||  ${hours12}:${minutes} ${suffix}`;
  };

  setClockBar();
  setInterval(setClockBar, 1000);

  if (!studentIdEl || !studentNameEl || !scanStatusEl) {
    return;
  }

  const applyStatusClass = (text) => {
    scanStatusEl.classList.remove("status-success", "status-warning", "status-danger");

    const value = (text || "").toLowerCase();
    let className = "status-warning";

    if (value.includes("recorded") || value.includes("success")) {
      className = "status-success";
    } else if (
      value.includes("error") ||
      value.includes("failed") ||
      value.includes("not found") ||
      value.includes("invalid") ||
      value.includes("already")
    ) {
      className = "status-danger";
    }

    scanStatusEl.classList.add(className);
  };

  const updateCameraData = async () => {
    try {
      const response = await fetch("/scan_data", { cache: "no-store" });
      if (!response.ok) throw new Error("Failed");

      const data = await response.json();

      const studentId =
        data.student_id && data.student_id.trim() !== ""
          ? data.student_id
          : "Waiting for scan...";

      const studentName =
        data.student_name && data.student_name.trim() !== ""
          ? data.student_name
          : "Waiting for scan...";

      const status =
        data.status && data.status.trim() !== ""
          ? data.status
          : "No valid ID detected.";

      studentIdEl.textContent = studentId;
      studentNameEl.textContent = studentName;
      scanStatusEl.textContent = status;

      applyStatusClass(status);
    } catch (error) {
      studentIdEl.textContent = "Waiting for scan...";
      studentNameEl.textContent = "Waiting for scan...";
      scanStatusEl.textContent = "No valid ID detected.";
      applyStatusClass("No valid ID detected.");
    }
  };

  updateCameraData();
  setInterval(updateCameraData, 600);
});