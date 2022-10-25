'use strict';

define(['jsYaml', 'toastr'], function (parser, toastr) {
  function parseAndNotify(document, options) {
    const notifySuccess = options['notifySuccess'] || false;
    const notifyFailure = options['notifyFailure'] || true;

    try {
      // FIXME improve validation
      let parsedDocument = parser.safeLoad(document);
      if (parsedDocument && parsedDocument['clusterEndpoint']) {
        if (notifySuccess) {
          toastr.success('This is a valid <samp>YAML</samp> document');
        }
        return parsedDocument;
      } else {
        if (notifyFailure) {
          toastr.error('Missing <samp>clusterEndpoint</samp> field');
        }
        return null;
      }
    } catch (e) {
      if (notifyFailure) {
        const message = `<samp>${e.message}</samp>`;
        if (e instanceof parser.YAMLException) {
          toastr.error(message, 'Invalid <samp>YAML</samp> document');
        } else {
          toastr.error(message, 'Something went failed while parsing the <samp>YAML</samp> document');
        }
      }
      return null;
    }
  }

  return {
    parseAndNotify
  }
});