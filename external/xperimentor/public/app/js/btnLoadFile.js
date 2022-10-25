'use strict';

/**
 * This component controls the open file button action.
 * It is responsible to load a file chosen by the user and put it's content in the Ace editor component.
 * */

define(['jquery', 'aceEditor', 'Button'], function ($, aceEditor, Button) {
  const $btnLoadFile = $('#btn-load-file');
  const $hiddenFileInput = $('#hiddenFileInput');

  $hiddenFileInput.on('change', function onClick(event) {
    const file = event.target.files[0];
    if (!file) return;
    console.debug(`File loaded: ${file.name}`);
    const reader = new FileReader();
    reader.onload = readerEvent => aceEditor.setContent(readerEvent.target['result']);
    reader.readAsText(file, 'UTF-8');
  });

  return new Button($btnLoadFile, () => $hiddenFileInput.trigger('click'));
});