export const addHitMessagesEventListeners = () => {
  const elements = document.querySelectorAll("[data-hit-messages]");
  if (elements.length) {
    elements.forEach((element) => {
      element.addEventListener("htmx:afterRequest", () => {
        document.getElementById("messages").click();
      });
    });
  }
};
