import {Process} from "./Process";
import {ProcessId, RecipeId, TaskId} from "./TypeAliases";
import {Command} from "./Command";
import {Serialize} from "serialazy";
import {IDSerializer} from "./Utils";

/**
 * Tasks can be seen as instances of {@link Process Processes}.
 * Tasks are Xperimentor's essence.
 * The framework was initially developed to manage this tasks.
 */
export class Task {
  @Serialize.Custom(IDSerializer)
  private _id: TaskId;

  /**
   * Indicates which process this task came from.
   */
  @Serialize.Custom(IDSerializer)
  private _processId: ProcessId;

  /**
   * Indicates which recipe this task came from.
   */
  @Serialize.Custom(IDSerializer)
  private _recipeId: RecipeId;

  /**
   * The command that should be executed by TaskExecutor.
   */
  @Serialize()
  private _command: Command;

  @Serialize.Custom({
    down(originalValue: Array<TaskId>): Array<TaskId> {
      return originalValue;
    },
    up(serializedValue: Array<TaskId>): Array<TaskId> {
      return serializedValue;
    }
  })
  private _dependencyIds: Array<TaskId>;

  @Serialize()
  private _status: Task.Status = Task.Status.IDLE;

  constructor(id: TaskId = null,
              processId: ProcessId = null,
              recipeId: RecipeId = null,
              command: Command = null,
              dependencyIds = new Array<TaskId>()) {
    this._id = id;
    this._processId = processId;
    this._recipeId = recipeId;
    this._command = command;
    this._dependencyIds = dependencyIds;
  }

  get id(): TaskId {
    return this._id;
  }

  set id(value: TaskId) {
    this._id = value;
  }

  get processId(): ProcessId {
    return this._processId;
  }

  set processId(value: ProcessId) {
    this._processId = value;
  }

  get recipeId(): RecipeId {
    return this._recipeId;
  }

  set recipeId(value: RecipeId) {
    this._recipeId = value;
  }

  get command(): Command {
    return this._command;
  }

  set command(value: Command) {
    this._command = value;
  }

  get dependencyIds(): Array<TaskId> {
    return this._dependencyIds;
  }

  set dependencyIds(value: Array<TaskId>) {
    this._dependencyIds = value;
  }

  get status(): Task.Status {
    return this._status;
  }

  set status(value: Task.Status) {
    this._status = value;
  }

  start(): Promise<Task.ExecutionData> {
    return new Promise((resolve, reject) => {
      resolve(new Task.ExecutionData());
    });
  }
}

export namespace Task {
  export enum Status {
    // @formatter:off
    IDLE    = 1 << 0,
    RUNNING = 1 << 1,
    SUCCESS = 1 << 2,
    ERROR   = 1 << 3,
    FAILED  = 1 << 4
    // @formatter:on
  }

  export class ExecutionData {
    stdout: string;
    stderr: string;
    code: number;
  }
}
