"use strict";
(() => {
  for (const state of document.querySelectorAll(".text-state")) {
    switch (state.textContent.trim()) {
      case "Ожидает":
        state.classList.add("text-warning");
        break;
      case "В работе":
        state.classList.add("text-primary");
        break;
      case "Просрочено":
        state.classList.add("text-danger");
        break;
      case "Завершено":
        state.classList.add("text-success");
        break;
      case "Исправление":
        state.classList.add("text-danger");
        break;
    }
  }
})();
