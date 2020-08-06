// $(function counter() {
//   var count = setInterval(function () {
//     var c = parseInt($(".counter").text());
//     $(".counter").text((++c).toString());
//     if (c == 100) {
//       clearInterval(count);
//       $(".counter").addClass("hide");
//       $(".preloader").addClass("active");
//     }
//   }, 40);
// });

window.addEventListener("load", () => {
  const preloader = document.querySelector(".preloader");
  const counter = document.querySelector(".loader-inner");
  preloader.classList.add("active");
  counter.classList.add("hide");
});

// Select DOM Items
const menuBtn = document.querySelector(".menu-btn");
const menu = document.querySelector(".menu");
const menuNav = document.querySelector(".menu-nav");
const Brand = document.querySelector(".brand");
const navItems = document.querySelectorAll(".nav-item");

// Set Initial State Of Menu
let showMenu = false;

menuBtn.addEventListener("click", toggleMenu);

function toggleMenu() {
  if (!showMenu) {
    menuBtn.classList.add("active");
    menu.classList.add("show");
    menuNav.classList.add("show");
    Brand.classList.add("show");
    navItems.forEach((item) => item.classList.add("show"));

    // Set Menu State
    showMenu = true;
  } else {
    menuBtn.classList.remove("active");
    menu.classList.remove("show");
    menuNav.classList.remove("show");
    Brand.classList.remove("show");
    navItems.forEach((item) => item.classList.remove("show"));

    // Set Menu State
    showMenu = false;
  }
}

// To top
window.addEventListener("scroll", () => {
  const toTop = document.querySelector(".to-top");
  if (window.pageYOffset > 100) {
    toTop.classList.add("active");
  } else {
    toTop.classList.remove("active");
  }
});
