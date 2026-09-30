
// SENTINEL AI - NAVIGATION + CHARTS

document.addEventListener("DOMContentLoaded", function () {

    // PAGE NAVIGATION

    const navLinks = document.querySelectorAll(".nav-link");
    const pages = document.querySelectorAll(".page");
    const currentPage = document.getElementById("current-page");

    function showPage(pageId) {

        pages.forEach(page => {
            page.classList.remove("active");
        });

        const target = document.getElementById(pageId);

        if (target) {
            target.classList.add("active");
        }

        navLinks.forEach(link => {
            link.classList.toggle(
                "active",
                link.dataset.page === pageId
            );
        });

        if (currentPage) {
            currentPage.textContent =
                pageId.charAt(0).toUpperCase() + pageId.slice(1);
        }
    }

    navLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            showPage(this.dataset.page);
        });
    });

    // NEW VERIFICATION

    const startButton = document.getElementById("start-auth");

    if (startButton) {
        startButton.addEventListener("click", function () {
            showPage("authentication");
        });
    }

    // CHARACTER COUNTER

    const typingInput = document.getElementById("typing-input");
    const characterCount = document.getElementById("character-count");
    const captureStatus = document.getElementById("capture-status");

    if (typingInput) {
        typingInput.addEventListener("input", function () {

            if (characterCount) {
                characterCount.textContent = this.value.length;
            }

            if (captureStatus) {
                captureStatus.textContent =
                    this.value.length > 0
                    ? "Typing input received"
                    : "Waiting for input...";
            }
        });
    }

    // DEMO AUTHENTICATION

    const verifyButton = document.getElementById("verify-btn");
    const authResult = document.getElementById("auth-result");

    if (verifyButton) {
        verifyButton.addEventListener("click", function () {

            const username =
                document.getElementById("username").value.trim();

            const text = typingInput.value.trim();

            if (!username || !text) {
                authResult.textContent =
                    "Please enter username and typing sample.";

                authResult.className = "auth-result error";
                return;
            }

            authResult.textContent =
                "Sample captured successfully. ML model integration pending.";

            authResult.className = "auth-result";
        });
    }

    // CHARTS

    if (typeof Chart === "undefined") {
        console.error("Chart.js not loaded. Check internet connection.");
        return;
    }

    // TYPING CONSISTENCY LINE CHART

    const typingCanvas = document.getElementById("typingChart");

    if (typingCanvas) {

        const typingChart = new Chart(typingCanvas, {

            type: "line",

            data: {
                labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],

                datasets: [{
                    label: "Typing Consistency",
                    data: [72, 78, 75, 85, 82, 91, 88],

                    borderColor: "#35d6b0",
                    backgroundColor: "rgba(53,214,176,0.12)",

                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: "#35d6b0"
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: false
                    }
                },

                scales: {
                    x: {
                        ticks: {
                            color: "#8b9ba5"
                        },
                        grid: {
                            display: false
                        }
                    },

                    y: {
                        min: 0,
                        max: 100,

                        ticks: {
                            color: "#8b9ba5"
                        },

                        grid: {
                            color: "rgba(255,255,255,0.07)"
                        }
                    }
                }
            }
        });

        const period = document.getElementById("chart-period");

        if (period) {
            period.addEventListener("change", function () {

                if (this.value === "week") {
                    typingChart.data.labels =
                        ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

                    typingChart.data.datasets[0].data =
                        [72, 78, 75, 85, 82, 91, 88];

                } else if (this.value === "month") {
                    typingChart.data.labels =
                        ["Week 1", "Week 2", "Week 3", "Week 4"];

                    typingChart.data.datasets[0].data =
                        [70, 79, 84, 90];

                } else {
                    typingChart.data.labels =
                        ["Jan", "Feb", "Mar", "Apr", "May", "Jun"];

                    typingChart.data.datasets[0].data =
                        [65, 72, 76, 81, 87, 91];
                }

                typingChart.update();
            });
        }
    }

    // ANALYTICS BAR CHART

    const analyticsCanvas = document.getElementById("analyticsChart");

    if (analyticsCanvas) {

        new Chart(analyticsCanvas, {

            type: "bar",

            data: {
                labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],

                datasets: [{
                    label: "Sessions",
                    data: [12, 19, 15, 22, 18, 25, 21],

                    backgroundColor: "#35d6b0",
                    borderRadius: 6
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: false
                    }
                },

                scales: {
                    x: {
                        ticks: {
                            color: "#8b9ba5"
                        },
                        grid: {
                            display: false
                        }
                    },

                    y: {
                        beginAtZero: true,

                        ticks: {
                            color: "#8b9ba5"
                        },

                        grid: {
                            color: "rgba(255,255,255,0.07)"
                        }
                    }
                }
            }
        });
    }

    // NOTIFICATION

    const notification = document.querySelector(".notification-btn");

    if (notification) {
        notification.addEventListener("click", function () {
            alert("You're all caught up!");
        });
    }

    showPage("overview");

    console.log("Sentinel AI JavaScript loaded!");

});