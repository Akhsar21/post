const password = document.getElementById("password");
const toggle = document.getElementById("toggle");

function showHide() {
  if (password.type === "password") {
    password.setAttribute("type", "text");
    toggle.classList.add("hide");
  } else {
    password.setAttribute("type", "password");
    toggle.classList.remove("hide");
  }
}

const modal = document.querySelector(".modal");
const previews = document.querySelectorAll(".gallery img");
const original = document.querySelector(".full-img");
const caption = document.querySelector(".caption");

previews.forEach((preview) => {
  modal.classList.add("open");
  original.classList.add("open");
  // Dynamyc change text and image
  const originalSrc = preview.getAttribute("data-original");
  original.src = `./full/${originalSrc}`;
  const altText = preview.alt;
  caption.textContent = altText;
});

modal.addEventListener("click", (e) => {
  if (e.target.classList.contains("modal")) {
    modal.classList.remove("open");
    original.classList.remove("open");
  }
});
