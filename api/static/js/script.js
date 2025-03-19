document.addEventListener("DOMContentLoaded", function () {
    let menuItems = document.querySelectorAll(".menu-item > a");

    menuItems.forEach((item) => {
        item.addEventListener("click", function (e) {
            e.preventDefault();
            let submenu = this.nextElementSibling;

            if (submenu && submenu.classList.contains("submenu")) {
                submenu.style.display = submenu.style.display === "block" ? "none" : "block";
            }
        });
    });

    let submenuItems = document.querySelectorAll(".submenu-item > a");

    submenuItems.forEach((item) => {
        item.addEventListener("click", function (e) {
            e.preventDefault();
            let subsubmenu = this.nextElementSibling;

            if (subsubmenu && subsubmenu.classList.contains("sub-submenu")) {
                subsubmenu.style.display = subsubmenu.style.display === "block" ? "none" : "block";
            }
        });
    });
});
