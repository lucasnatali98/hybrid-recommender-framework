'use strict';

/**
 * This component controls the VisJS graph.
 * It is responsible to configure VisJS look and behaviour.
 * */

define(['vis/vis'], function (vis) {
  const container = document.getElementById('graph');
  const options = {
    layout: {
      hierarchical: {
        direction: "LR",
        sortMethod: "directed",
        // levelSeparation: 250,
        // nodeSpacing: 70,
        // treeSpacing: 70,
      }
    },
    physics: {
      enabled: true
    },
    // configure: {
    //   filter: function (option, path) {
    //     return path.indexOf('hierarchical') !== -1;
    //   },
    //   showButton: false
    // },
    interaction: {
      navigationButtons: true,
      keyboard: false
    },
    edges: {
      arrows: {
        to: {enabled: true, type: 'arrow'}
      }
    },
    nodes: {
      font: {
        size: 14,
        face: 'Lucida Console, Lucida Sans Typewriter, monaco, Bitstream Vera Sans Mono, monospace',
        multi: 'html',
        vadjust: 2
      },
      widthConstraint: {minimum: 15},
      heightConstraint: {minimum: 15},
    }
  };

  const highPerformanceOption = {
    layout: {
      improvedLayout: false
    },
    nodes: {
      shape: 'dot',
      scaling: {
        min: 10,
        max: 30
      },
      font: {
        size: 12,
        face: 'Tahoma'
      }
    },
    edges: {
      width: 0.15,
      color: {inherit: 'from'},
      smooth: {
        type: 'continuous'
      }
    },
    physics: {
      stabilization: false,
      barnesHut: {
        gravitationalConstant: -80000,
        springConstant: 0.001,
        springLength: 200
      }
    },
    interaction: {
      tooltipDelay: 200,
      hideEdgesOnDrag: true
    }
  };

  let network = null;

  function draw(visJsData) {
    this.clear();
    network = new vis.Network(container, visJsData, highPerformanceOption);
    network.on("click", function (params) {
      requirejs(['taskInfo', 'experiment'], function (taskInfo, experiment) {
        params.event = "[original event]";
        const taskId = params.nodes[0];
        const task = experiment.getTask(taskId);
        if (task) {
          taskInfo.updateInfo(task);
        }
      });
    });
  }

  function clear() {
    if (network) {
      network.destroy();
    }
    network = null;
  }

  return {
    draw,
    clear,
    getNetwork: () => network
  };
});