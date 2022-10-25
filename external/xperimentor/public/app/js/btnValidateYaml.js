'use strict';

/**
 * This component controls the validate button click event.
 * */

define(['yamlParser', 'aceEditor', 'Button'], function (yamlParser, aceEditor, Button) {

  function onClick() {
    yamlParser.parseAndNotify(aceEditor.getContent(), {notifySuccess: true});
  }

  return new Button($('#btn-validate'), onClick);
});