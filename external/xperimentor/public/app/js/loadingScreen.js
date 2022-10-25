'use strict';

define(['jquery'], function ($) {

  const DOM = {};

  /* =================== private functions ================= */

  function cacheDOM() {
    DOM.$body = $('body');
    DOM.$loadingScreenModal = $("#loading-screen-modal");
  }

  /* =================== public functions ================= */

  function show() {
    DOM.$loadingScreenModal.modal({
      backdrop: "static", // remove ability to close modal with click
      keyboard: false,
      show: true
    });
  }

  function hide() {
    DOM.$loadingScreenModal.removeClass("in");
    $(".modal-backdrop").remove();
    DOM.$body.removeClass('modal-open');
    DOM.$body.css('padding-right', '');
    DOM.$loadingScreenModal.hide();
  }

  cacheDOM();

  /* =================== auto loading ================= */

  return {
    show,
    hide
  }
});