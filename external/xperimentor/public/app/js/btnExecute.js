'use strict';

/**
 * This component controls the execute file button action.
 * It is responsible to launch the experiment.
 * */

define(['jquery', 'Button', 'graphEditor'], function ($, Button, graphEditor) {

  function onClick() {
    requirejs(['experiment', 'toastr'], function (experiment) {
      console.log('btnExecute - Início da função')
      console.log("experiment: ", experiment)
      if (experiment.isRunning) {
        toastr.error(message, 'Experiment is already running');
      } else {
        graphEditor.getNetwork().stopSimulation();
        graphEditor.getNetwork().setOptions({physics: {enabled: false}});
        console.log("")
        setTimeout(function () {
          experiment.execute();
        }, 3000);
      }
    });
  }

  return new Button($('#btn-execute'), onClick);
});