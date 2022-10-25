import {ArgumentType, TaskId} from "./TypeAliases";
import JsonType from "serialazy/lib/dist/types/json_type";

export const ARGUMENT_REGEXP = /{([a-zA-Z0-9_]+)}/g;

export function getCommandArgumentTypes(command: string): Array<ArgumentType> {
  const argumentTypes: Array<ArgumentType> = [];
  let match = ARGUMENT_REGEXP.exec(command);
  while (match) {
    argumentTypes.push(match[1]);
    match = ARGUMENT_REGEXP.exec(command);
  }
  return argumentTypes;
}

// font: https://stackoverflow.com/a/36234242/6039697
export function cartesianProduct<T>(arr: Array<Array<T>>): Array<Array<T>> {
  return arr.reduce(function (a, b) {
    return a.map(function (x) {
      return b.map(function (y) {
        return x.concat(y);
      })
    }).reduce(function (a, b) {
      return a.concat(b)
    }, [])
  }, [[]])
}

/**
 * Converts a Map to an object of JsonType
 * @param map map to be converted
 */
export function map2obj(map: Map<any, any>): JsonType {
  return Array.from(map).reduce((obj, [key, value]) => {
    obj[key] = value;
    return obj;
  }, {});
}

/**
 * Converts an object to a map
 * @param obj object to be converted
 */
export function obj2map(obj) {
  return new Map(Object.entries(obj));
}

export const IDSerializer = {
  down(originalValue: TaskId): string {
    return originalValue.toString()
  },
  up(serializedValue: string): TaskId {
    return serializedValue;
  }
};