document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  form.addEventListener("submit", () => {
    alert("Your pizza order is being processed 🍕");
  });
});
