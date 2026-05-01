(function () {
  "use strict";

  var navToggle = document.querySelector(".nav-toggle");
  var mobileNav = document.querySelector(".mobile-nav");
  var fabBtn = document.querySelector(".fab-main");
  var fabPanel = document.querySelector(".fab-panel");

  if (navToggle && mobileNav) {
    navToggle.addEventListener("click", function () {
      var open = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", !open);
      mobileNav.classList.toggle("is-open", !open);
      document.body.style.overflow = open ? "" : "hidden";
    });

    mobileNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navToggle.setAttribute("aria-expanded", "false");
        mobileNav.classList.remove("is-open");
        document.body.style.overflow = "";
      });
    });
  }

  if (fabBtn && fabPanel) {
    fabBtn.addEventListener("click", function () {
      fabPanel.classList.toggle("is-open");
      fabBtn.setAttribute(
        "aria-expanded",
        fabPanel.classList.contains("is-open")
      );
    });
    document.addEventListener("click", function (e) {
      if (!fabBtn.contains(e.target) && !fabPanel.contains(e.target)) {
        fabPanel.classList.remove("is-open");
        fabBtn.setAttribute("aria-expanded", "false");
      }
    });
  }

  function openModal(id) {
    var el = document.getElementById(id);
    if (el) {
      el.classList.add("is-open");
      el.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    }
  }

  function closeModal(id) {
    var el = document.getElementById(id);
    if (el) {
      el.classList.remove("is-open");
      el.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    }
  }

  document.querySelectorAll("[data-open-modal]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      openModal(btn.getAttribute("data-open-modal"));
    });
  });

  document.querySelectorAll("[data-close-modal]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      closeModal(btn.getAttribute("data-close-modal"));
    });
  });

  document.querySelectorAll(".modal-overlay").forEach(function (overlay) {
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) {
        overlay.classList.remove("is-open");
        overlay.setAttribute("aria-hidden", "true");
        document.body.style.overflow = "";
      }
    });
  });

  /**
   * Замініть PHONE_WHATSAPP на ваш міжнародний номер без плюса, наприклад 380501234567
   * Замініть TELEGRAM_USERNAME на ваш username без @
   */
  var PHONE_WHATSAPP = "380501234567";
  var TELEGRAM_USERNAME = "taxlawyer_ua";

  function pageLang() {
    var l = (document.documentElement.getAttribute("lang") || "uk").toLowerCase();
    if (l.indexOf("ru") === 0) return "ru";
    if (l.indexOf("en") === 0) return "en";
    return "uk";
  }

  var FORM_I18N = {
    uk: {
      consultTitle: "Консультація",
      docsTitle: "Документи на аналіз",
      name: "Ім'я: ",
      phone: "Телефон: ",
      message: "Повідомлення: "
    },
    ru: {
      consultTitle: "Консультация",
      docsTitle: "Документы на анализ",
      name: "Имя: ",
      phone: "Телефон: ",
      message: "Сообщение: "
    },
    en: {
      consultTitle: "Consultation request",
      docsTitle: "Document review",
      name: "Name: ",
      phone: "Phone: ",
      message: "Details: "
    }
  };

  function buildWhatsAppUrl(text) {
    return (
      "https://wa.me/" +
      PHONE_WHATSAPP +
      "?text=" +
      encodeURIComponent(text || "")
    );
  }

  function buildTelegramUrl(text) {
    return (
      "https://t.me/" +
      TELEGRAM_USERNAME +
      (text ? "?text=" + encodeURIComponent(text) : "")
    );
  }

  document.querySelectorAll("a[data-wa-prefill]").forEach(function (a) {
    a.href = buildWhatsAppUrl(a.getAttribute("data-wa-prefill") || "");
  });

  document.querySelectorAll("a[data-tg-prefill]").forEach(function (a) {
    a.href = buildTelegramUrl(a.getAttribute("data-tg-prefill") || "");
  });

  document.querySelectorAll("form[data-contact-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var type = form.getAttribute("data-contact-form");
      var fd = new FormData(form);
      var name = (fd.get("name") || "").toString().trim();
      var phone = (fd.get("phone") || "").toString().trim();
      var message = (fd.get("message") || "").toString().trim();
      var t = FORM_I18N[pageLang()] || FORM_I18N.uk;
      var lines = [
        type === "docs" ? t.docsTitle : t.consultTitle,
        name ? t.name + name : "",
        phone ? t.phone + phone : "",
        message ? t.message + message : ""
      ].filter(Boolean);
      var text = lines.join("\n");

      var success = form.querySelector(".form-success");
      if (success) {
        success.classList.add("is-visible");
        form.reset();
        setTimeout(function () {
          success.classList.remove("is-visible");
        }, 8000);
      }

      window.open(buildWhatsAppUrl(text), "_blank", "noopener,noreferrer");
    });
  });
})();
