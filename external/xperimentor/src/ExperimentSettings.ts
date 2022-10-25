import {ArgumentType, ArgumentValue} from "./TypeAliases";
import {Process} from "./Process";
import {Recipe} from "./Recipe";
import {Experiment} from "./Experiment";

/**
 * This interface is a data model to store an experiment setting.
 * Objects from this class are populated by parsing the YAML configuration file.
 * This data model is required to build an {@link Experiment}.
 */
export interface ExperimentSettings {
  /**
   * The endpoint of the cluster where the commands should be executed.
   */
  clusterEndpoint: string;
  processes: Array<Process>;
  recipeDefaults: Map<ArgumentType, Array<ArgumentValue>>;
  recipes: Array<Recipe>;
}