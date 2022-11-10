'use strict';

define(function (require) {
  const
      $ = require('jquery'),
      vis = require('vis/vis'),
      Digraph = require('Digraph'),
      toastr = require('toastr'),
      Task = require('Task');

  /* =================== private functions ================= */

  function generateTaskMap(tasks) {
    console.log("tasks in generate task map: ")
    console.log(tasks)
    let taskMap = new Map();
    for (const taskRawData of tasks) {
      const task = new Task(taskRawData);
      taskMap.set(task.id, task);
    }
    return taskMap;
  }

  function generateFlowDigraph(taskMap) {
    const flowDigraph = new Digraph();
    for (const [taskId, task] of taskMap.entries()) {
      flowDigraph.addNode(taskId);
      for (const dependencyId of task.deps) {
        flowDigraph.addNode(dependencyId);
        flowDigraph.connect(dependencyId, taskId)
      }
    }
    return flowDigraph;
  }

  function buildVisJSGraph(flowDigraph) {
    const nodes = new vis.DataSet();
    const edges = new vis.DataSet();

    nodes.add({id: '_S', label: 'S'});
    nodes.add({id: '_T', label: 'T'});

    for (const [nodeId, node] of flowDigraph.nodesMap) {
      nodes.add({id: nodeId, label: nodeId.toString()});

      if (node.inputNodes.size === 0) {
        edges.add({from: '_S', to: nodeId});
      }

      if (node.outputNodes.size === 0) {
        edges.add({from: nodeId, to: '_T'});
      }

      for (const dependencyId of node.inputNodes) {
        edges.add({from: dependencyId, to: nodeId});
      }
    }

    return {nodes: nodes, edges: edges};
  }

  /* =================== private methods ================= */

  function getStatusByResponseData(responseData) {
    let status;

    if (responseData['return_code'] === 0 && responseData['stderr'] === '') {
      status = Task.Status.SUCCESSFULLY_FINISHED;
    } else if (responseData['return_code'] === 0 && responseData['stderr'] !== '') {
      status = Task.Status.FINISHED_WITH_ERRORS;
    } else if (responseData['return_code'] !== 0 && responseData['stderr'] === '') {
      status = Task.Status.FINISHED_WITH_NON_ZERO;
    } else if (responseData['return_code'] !== 0 && responseData['stderr'] !== '') {
      status = Task.Status.FINISHED_WITH_ERRORS_NON_ZERO;
    }

    return status;
  }

  function processUnsuccessfullyFinishedTask(taskId) {
    this.updateTaskStatus(taskId, Task.Status.FAILED);
    toastr.error(`Cannot execute task <samp>"${taskId}"</samp>`, 'Server not responding');
  }

  function isReadyToRun(taskId) {
    if (taskId.status === Task.Status.RUNNING) {
      return false;
    }
    const dependencies = this._flowDigraph.getNode(taskId).inputNodes;
    for (const dependencyId of dependencies) {
      const dependency = this.getTask(dependencyId);
      const number = dependency.status & (Task.Status.SUCCESSFULLY_FINISHED | Task.Status.FORCED_SUCCESSFULLY_FINISHED);
      if (number === 0) {
        return false;
      }
    }
    return true;
  }

  function finishExperiment() {
    this._isRunning = false;
    toastr.info('All tasks finished!');
    requirejs(['btnExecute'], btn => btn.enable());
  }

  /* =================== public methods ================= */

  class Experiment {
    constructor() {
      this._clusterEndpoint = 'http://0.0.0.0:5050/run';
      this._tasksMap = new Map();
      this._isRunning = false;
      this._flowDigraph = new Digraph();
      this._visJsData = null;

      processUnsuccessfullyFinishedTask = processUnsuccessfullyFinishedTask.bind(this);
      isReadyToRun = isReadyToRun.bind(this);
      finishExperiment = finishExperiment.bind(this);
    }

    set experimentData(data) {
      this._clusterEndpoint = data['clusterEndpoint'] || this._clusterEndpoint;
      this._tasksMap = generateTaskMap(data['tasks']);
      this._isRunning = false;
      this._flowDigraph = generateFlowDigraph(this._tasksMap);
      this._visJsData = buildVisJSGraph(this._flowDigraph);
    }

    getTask(taskId) {
      return this._tasksMap.get(taskId)
    }

    get isRunning() {
      return this._isRunning;
    }

    get visJsData() {
      return this._visJsData;
    }

    execute() {
      if (this._visJsData === null) {
        toastr.error('Experiment not built');
        return;
      }

      if (this.isRunning) {
        toastr.error('Experiment is already running');
        return;
      }

      toastr.info('Experiment initialized');

      this._isRunning = true;

      requirejs(['btnExecute'], btn => btn.disable());

      const initialTaskIDs = [...this._tasksMap.keys()].filter(isReadyToRun);

      const self = this;

      for (const taskId of initialTaskIDs) {
        this.executeTask(taskId, function (ignored, executionData) {
          self.processFinishedTask(taskId, executionData);
          self.executeAllTasksWaitingForFinishedTask(taskId);
        }, processUnsuccessfullyFinishedTask);
      }
    }

    executeAllTasksWaitingForFinishedTask(finishedTaskId) {
      for (const waitingTaskId of this._flowDigraph.getNode(finishedTaskId).outputNodes) {
        if (isReadyToRun(waitingTaskId)) {
          const self = this;
          this.executeTask(waitingTaskId, function (ignored, executionData) {
            const finishedTaskId = waitingTaskId;
            self.processFinishedTask(finishedTaskId, executionData);
            self.executeAllTasksWaitingForFinishedTask(finishedTaskId);
          }, processUnsuccessfullyFinishedTask);
        }
      }
    }

    executeTask(taskId, onSuccess, onFailure) {
      // console.debug('Initializing task: ' + taskId);
      const task = this.getTask(taskId);
      this.updateTaskStatus(taskId, Task.Status.RUNNING);

      onSuccess = onSuccess || (() => {
      });
      onFailure = onFailure || (() => {
      });
      console.log("Cluster endpoint")
      console.log(this._clusterEndpoint)
      console.log("WIndow hrf: ", window.location.href)

      $.ajax({
        context: this,
        type: "post",
        url: this._clusterEndpoint,
        contentType: 'application/json;charset=UTF-8',
        cache: false,
        method: 'POST',
        dataType: 'json',
        data: JSON.stringify({id: taskId, command: task.command}),
        success: function (responseData) {
          onSuccess(taskId, responseData);
        },
        error: function () {
          onFailure(taskId);
        },
        complete: function () {
          const unfinishedTasks =
              [...this._tasksMap.values()]
                  .filter(t => (t.status & (Task.Status.RUNNING | Task.Status.WAITING)) > 0);

          if (unfinishedTasks.length === 0) {
            finishExperiment();
          }
        }
      });
    }

    updateTaskStatus(taskId, status) {
      const task = this.getTask(taskId);
      task.status = status;

      switch (status) {
        case Task.Status.WAITING:
          this._visJsData.nodes.update({id: taskId, color: '#97C2FC'});
          break;
        case Task.Status.RUNNING:
          this._visJsData.nodes.update({id: taskId, color: '#0053fc'});
          break;
        case Task.Status.SUCCESSFULLY_FINISHED:
          this._visJsData.nodes.update({id: taskId, color: '#70FF9A'});
          break;
        case Task.Status.FINISHED_WITH_ERRORS:
          this._visJsData.nodes.update({id: taskId, color: '#FFF900'});
          break;
        case Task.Status.FINISHED_WITH_NON_ZERO:
          this._visJsData.nodes.update({id: taskId, color: '#FFBF00'});
          break;
        case Task.Status.FINISHED_WITH_ERRORS_NON_ZERO:
          this._visJsData.nodes.update({id: taskId, color: '#FF6000'});
          break;
        case Task.Status.FAILED:
          this._visJsData.nodes.update({id: taskId, color: '#D70000'});
          break;
        case Task.Status.FORCED_SUCCESSFULLY_FINISHED:
          this._visJsData.nodes.update({id: taskId, color: '#D70085'});
          break;
      }
    }

    processFinishedTask(finishedTaskId, responseData) {
      const task = this._tasksMap.get(finishedTaskId);
      task.executionData = responseData;

      let status = getStatusByResponseData(responseData);

      this.updateTaskStatus(finishedTaskId, status);

      if (status !== Task.Status.SUCCESSFULLY_FINISHED) {
        toastr.warning(`Task <samp><b>${finishedTaskId}</b></samp> unsuccessfully finished`);
      }

      // TODO update task info

      return task;
    }

    retry(taskId) {
      const self = this;
      if (isReadyToRun(taskId)) {
        this.executeTask(taskId, function (ignored, executionData) {
          self.processFinishedTask(taskId, executionData);
          self.executeAllTasksWaitingForFinishedTask(taskId);
        }, processUnsuccessfullyFinishedTask);
      }
    }
  }

  return new Experiment();
});
