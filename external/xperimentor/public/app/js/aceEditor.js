'use strict';

/**
 * This component controls the Ace div container.
 * It is responsible to configure the Ace theme and content.
 * */

define(['jquery', 'ace/ace'], function ($, ace) {

  const DOM = {};

  /* =================== private functions ================= */

  function cacheDom() {
    // If used as CDN
    // ace.config.set("packaged", true);
    // ace.config.set("basePath", require.toUrl("ace"));
    DOM.$editor = ace.edit('editor');
  }

  function configure() {
    DOM.$editor.setTheme('ace/theme/eclipse');
    DOM.$editor.session.setMode('ace/mode/yaml');
  }

  /* =================== public functions ================== */

  function setContent(content) {
    DOM.$editor.setValue(content);
  }

  function getContent() {
    return DOM.$editor.getValue();
  }

  cacheDom();
  configure();

  return {
    getContent,
    setContent
  };
});