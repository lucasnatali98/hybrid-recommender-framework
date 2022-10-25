/**
 * This module is responsible to show the task status of a given task
 */
define(['jquery', 'Task', 'Button'], function ($, Task, Button) {
  const DOM = {};

  let currentTask = null;

  const btnRetry = new Button($('#btn-retry'), retry);
  const btnAccept = new Button($('#btn-accept'), accept);

  /* =================== private functions ================= */

  function cacheDom() {
    DOM.$card = $('#task-card');
    DOM.$taskId = $('#task-card-title');
    DOM.$taskStatus = $('#task-card-status');
    DOM.$taskCommand = $('#task-card-command');
    DOM.$taskStdout = $('#task-card-stdout');
    DOM.$taskStderr = $('#task-card-stderr');
    DOM.$taskReturnCode = $('#task-card-return-code');
  }

  function retry() {
    require(['experiment'], function (experiment) {
      experiment.retry(currentTask.id);
      updateControls();
    });
  }

  function accept() {
    require(['experiment'], function (experiment) {
      experiment.updateTaskStatus(currentTask.id, Task.Status.FORCED_SUCCESSFULLY_FINISHED);
      experiment.executeAllTasksWaitingForFinishedTask(currentTask.id);
      updateControls();
    });
  }

  /* =================== public functions ================== */

  function updateControls(task) {
    task = task || currentTask;

    let canRetry = true;
    let canAccept = true;

    switch (task.status) {
      case Task.Status.SUCCESSFULLY_FINISHED:
        break;
      case Task.Status.FINISHED_WITH_ERRORS_NON_ZERO:
        break;
      case Task.Status.FINISHED_WITH_NON_ZERO:
        break;
      case Task.Status.FINISHED_WITH_ERRORS:
        break;
      case Task.Status.WAITING:
        break;
      case Task.Status.RUNNING:
        canRetry = false;
        canAccept = false;
        break;
      case Task.Status.FAILED:
        break;
      case Task.Status.FORCED_SUCCESSFULLY_FINISHED:
        canAccept = false;
        break;
    }

    if (canAccept) {
      btnAccept.enable();
    } else {
      btnAccept.disable();
    }

    if (canRetry) {
      btnRetry.enable();
    } else {
      btnRetry.disable();
    }
  }

  function updateInfo(task) {
    updateControls(task);
    currentTask = task;
    // TODO scape html
    //DOM.$card
    DOM.$taskId.text(task.id);
    DOM.$taskStatus.text(Task.Status.toString(currentTask.status));
    DOM.$taskCommand.text(task.command);
    if (task.executionData) {
      DOM.$taskStdout.text(task.executionData['stdout']);
      DOM.$taskStderr.text(task.executionData['stderr']);
      DOM.$taskReturnCode.text(task.executionData['return_code']);
    } else {
      DOM.$taskStdout.text('');
      DOM.$taskStderr.text('');
      DOM.$taskReturnCode.text('');
    }
  }

  cacheDom();

  return {
    updateInfo
  };
});
