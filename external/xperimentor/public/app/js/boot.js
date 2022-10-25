'use strict';

/**
 * This file is the first script called after RequireJS lib loads.
 * It is responsible to configure RequireJS lib and script loading order.
 * */

requirejs.config({
  baseUrl: '/',
  paths: {
    /* ========================== libs ========================== */
    jquery: '/node-dependencies/jquery/dist/jquery',
    ace: '/node-dependencies/ace-builds/src',
    vis: '/node-dependencies/visjs-network/dist/',
    jsYaml: '/node-dependencies/js-yaml/dist/js-yaml',
    bootstrap: '/node-dependencies/bootstrap/dist/js/bootstrap.bundle',
    fontawesome: '/node-dependencies/@fortawesome/fontawesome-free/js/all',
    toastr: '/node-dependencies/toastr/build/toastr.min',
    /* ========================== app ========================== */
    aceEditor: 'app/js/aceEditor',
    btnLoadFile: 'app/js/btnLoadFile',
    btnValidateYaml: 'app/js/btnValidateYaml',
    graphEditor: 'app/js/graphEditor',
    btnBuild: 'app/js/btnBuild',
    btnExecute: 'app/js/btnExecute',
    loadingScreen: 'app/js/loadingScreen',
    Task: 'app/js/Task',
    Digraph: 'app/js/Digraph',
    experiment: 'app/js/experiment',
    app: 'app/js/app',
    yamlParser: 'app/js/yamlParser',
    taskInfo: 'app/js/taskInfo',
    Button: 'app/js/Button'
  }
});

requirejs(['jquery'], function () {
  requirejs(['bootstrap', 'fontawesome'], function () {
    requirejs(['loadingScreen'], function (loadingScreen) {
      loadingScreen.show();
      requirejs([
        'aceEditor',
        'btnLoadFile',
        'graphEditor',
        'btnExecute',
        'btnValidateYaml',
        'btnBuild'], function () {
        requirejs(['app'], () => $(document).ready(loadingScreen.hide));
      });
    });
  });
});
