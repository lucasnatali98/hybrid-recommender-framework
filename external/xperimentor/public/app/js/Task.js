'use strict';

define(function () {
  class Task {
    // @formatter:off
    static Status = {
      WAITING:                        1 << 0,
      RUNNING:                        1 << 1,
      SUCCESSFULLY_FINISHED:          1 << 2,
      FINISHED_WITH_ERRORS:           1 << 3,
      FINISHED_WITH_NON_ZERO:         1 << 4,
      FINISHED_WITH_ERRORS_NON_ZERO:  1 << 5,
      FAILED:                         1 << 6,
      FORCED_SUCCESSFULLY_FINISHED:   1 << 7
    };
    // @formatter:on

    constructor(props) {
      this._status = Task.Status.WAITING;
      this._id = props['id'];
      this._command = props['command'];
      this._deps = props['deps'] || [];
      this._rawData = props;
      this._executionData = null;

      Task.Status.toString = function (status) {
        for (const key in Task.Status) {
          if (Task.Status[key] === status) {
            return key;
          }
        }
      }
    }

    get executionData() {
      return this._executionData;
    }

    set executionData(value) {
      this._executionData = value;
    }

    get id() {
      return this._id;
    }

    get status() {
      return this._status;
    }

    set status(status) {
      this._status = status;
    }

    get command() {
      return this._command;
    }

    get deps() {
      return this._deps;
    }
  }

  return Task;
});