'use strict';

/**
 * This script is responsible to pre-configure some components and prepare GUI
 * for first use.
 * */

define(['jquery', 'aceEditor', 'toastr'], function ($, aceEditor, toastr) {
  toastr.options = {
    'closeButton': true,
    'debug': false,
    'newestOnTop': true,
    'progressBar': true,
    'positionClass': 'toast-bottom-right',
    'preventDuplicates': false,
    'onclick': null,
    'showDuration': '0',
    'hideDuration': '0',
    'timeOut': '0',
    'extendedTimeOut': '0',
    'showEasing': 'swing',
    'hideEasing': 'linear',
    'showMethod': 'fadeIn',
    'hideMethod': 'fadeOut'
  }
});
