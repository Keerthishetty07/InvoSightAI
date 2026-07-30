document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".flash-message").forEach((el) => {
    setTimeout(() => {
      el.style.opacity = "0";
      el.style.transform = "translateY(-6px)";
      el.style.transition = "opacity .25s ease, transform .25s ease";
      setTimeout(() => el.remove(), 260);
    }, 4200);
  });
});