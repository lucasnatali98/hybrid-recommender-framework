/**
 * This is the project main class.
 * It is responsible to build and manage the experiment lifetime.
 */
import {ExperimentSettings} from "./ExperimentSettings";
import {Task} from "./Task";

export class Experiment {
  private settings: ExperimentSettings;
  private tasks: Array<Task>;


  constructor(settings: ExperimentSettings) {
    this.settings = settings;
  }
}