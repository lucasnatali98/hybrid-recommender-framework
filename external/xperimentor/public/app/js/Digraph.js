'use strict';

define(function () {

  class Node {
    constructor(id) {
      this._id = id;
      this._in = new Set();
      this._out = new Set();
    }

    addInputNode(nodeId) {
      this._in.add(nodeId);
    }

    addOutputNode(nodeId) {
      this._out.add(nodeId);
    }

    get id() {
      return this._id;
    }

    get inputNodes() {
      return this._in;
    }

    get outputNodes() {
      return this._out;
    }
  }

  class Digraph {
    constructor() {
      this._nodes = new Map();
    }

    getNode(id) {
      return this._nodes.get(id);
    }

    addNode(id) {
      if (!this.getNode(id)) {
        this._nodes.set(id, new Node(id));
      }
    }

    get nodesMap() {
      return this._nodes;
    }

    connect(fromID, toID) {
      if (fromID === toID) {
        throw new Error(`Self connection (${fromID})`)
      }

      let from = this.getNode(fromID);

      if (!from) {
        this.addNode(fromID);
        from = this.getNode(fromID)
      }

      let to = this.getNode(toID);

      if (!to) {
        this.addNode(toID);
        to = this.getNode(toID);
      }

      from.addOutputNode(toID);
      to.addInputNode(fromID);
      // console.debug(`Connecting nodes ${fromID} -> ${toID}`);
    }
  }

  return Digraph;
});