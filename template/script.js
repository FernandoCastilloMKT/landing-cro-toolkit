(() => {
  "use strict";

  const config = window.LANDING_CONFIG || {};
  const status = document.querySelector("#form-status");
  const form = document.querySelector("#lead-form");

  document.querySelectorAll("[data-brand]").forEach((node) => {
    node.textContent = config.brand || "[MARCA DE DEMOSTRACIÓN]";
  });

  const phone = document.querySelector("[data-phone]");
  phone.textContent = config.phoneDisplay || "[TELÉFONO]";
  if (config.phoneHref) {
    phone.href = `tel:${String(config.phoneHref).replace(/[^+\d]/g, "")}`;
    phone.setAttribute("aria-label", `Llamar al ${phone.textContent}`);
    phone.addEventListener("click", () => track("phone_click"));
  }

  const privacy = document.querySelector("[data-privacy]");
  if (config.privacyUrl) privacy.href = config.privacyUrl;

  document.querySelectorAll("[data-track]").forEach((node) => {
    node.addEventListener("click", () => track(node.dataset.track));
  });

  let started = false;
  form.addEventListener("input", () => {
    if (!started) {
      started = true;
      track("form_start");
    }
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    status.textContent = "";

    if (!form.reportValidity()) return;
    if (!config.formEndpoint) {
      status.textContent = "Modo demostración: configura un endpoint seguro para habilitar el envío.";
      return;
    }

    const button = form.querySelector("button[type='submit']");
    button.disabled = true;
    try {
      const response = await fetch(config.formEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(new FormData(form))),
      });
      if (!response.ok) throw new Error("Submission rejected");
      form.reset();
      status.textContent = "Solicitud enviada correctamente.";
      track("form_submit_success");
    } catch {
      status.textContent = "No se ha podido enviar. Inténtalo de nuevo más tarde.";
      track("form_submit_error");
    } finally {
      button.disabled = false;
    }
  });

  function track(eventName) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: eventName });
  }
})();
