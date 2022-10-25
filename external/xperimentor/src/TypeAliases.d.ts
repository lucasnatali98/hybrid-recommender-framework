export type ArgumentType = string;
export type ArgumentValue = string;
export type TaskId = string | number;
export type RecipeId = number | string;
export type ArgumentMap = Map<ArgumentType, ArgumentValue>
export type RecipeUsage = Map<ArgumentType, Array<ArgumentValue>>
export type ProcessId = number | string;