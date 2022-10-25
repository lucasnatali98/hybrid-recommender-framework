'use strict';

/**
 * This component controls the build file button action.
 * It is responsible to update graph view with current yaml content.
 */

define(function (require) {
  const
      aceEditor = require('aceEditor'),
      experiment = require('experiment'),
      parser = require('yamlParser'),
      graphEditor = require('graphEditor'),
      toastr = require('toastr'),
      Button = require('Button');

  function onClick() {
    if (experiment.isRunning) {
      toastr.error('Cannot build until experiment finishes');
      return;
    }

    const updatedContent = aceEditor.getContent();

    let parsedDocument = parser.parseAndNotify(updatedContent, {notifySuccess: false});
    if (!parsedDocument) return;
    experiment.experimentData = parsedDocument;
    graphEditor.draw(experiment.visJsData);
  }

  return new Button($('#btn-build'), onClick);
});