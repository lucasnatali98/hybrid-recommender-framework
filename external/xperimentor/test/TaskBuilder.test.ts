import {expect} from "chai";
import {Process} from "../src/Process";
import {Recipe} from "../src/Recipe";
import {ArgumentMap, ArgumentType, ArgumentValue, RecipeUsage} from "../src/TypeAliases";
import {TaskBuilder} from "../src/TaskBuilder";
import {ExperimentSettings} from "../src/ExperimentSettings";
import {Task} from "../src/Task";
import {Command} from "../src/Command";
import {deflate, inflate} from "serialazy";

describe('TaskBuilder', function () {
  // ensureRecipeArgument tests
  (function () {
    it('ensureRecipeArgument - recipe only', function () {
      const process =
        new Process(
          'TestProcess',
          'python script.py {NAME} {AGE} {WEIGHT}',
          [/* Irrelevant for this test */]);

      const recipeUsage: RecipeUsage = new Map<ArgumentType, Array<ArgumentValue>>([
        ['NAME', ['John', 'Katy', 'Mike']],
        ['AGE', ['18', '23']],
        ['WEIGHT', ['60.9', '80.2']]
      ]);

      const recipe = new Recipe('TestRecipe', [/* Irrelevant for this test */], recipeUsage);
      const builder = new TaskBuilder();
      const actual = builder['ensureRecipeArgument'](process, recipe, new Map(/* Irrelevant for this test */));

      expect(actual).to.eql(recipeUsage);
    });

    it('ensureRecipeArgument - recipe only - error', function () {
      const process =
        new Process('TestProcess',
          'python script.py {NAME} {AGE} {WEIGHT}',
          [/* Irrelevant for this test */]);

      const recipeUsage: RecipeUsage = new Map<ArgumentType, Array<ArgumentValue>>([
        ['NAME', ['John', 'Katy', 'Mike']],
        ['AGE', ['18', '23']],
      ]);

      // Missing param WEIGHT
      const recipe = new Recipe('TestRecipe', [/* Irrelevant for this test */], recipeUsage);

      const expectedErrorMessage = `Required argument "WEIGHT" from process "${process.id}" not found`;

      expect(function () {
        const builder = new TaskBuilder();
        builder['ensureRecipeArgument'](process, recipe, new Map(/* Irrelevant for this test */));
      }).to.throw(expectedErrorMessage);
    });

    it('ensureRecipeArgument - recipeDefaults only', function () {
      const process = new Process(
        'TestProcess',
        'python script.py {NAME} {AGE} {WEIGHT}',
        [/* Irrelevant for this test */]);
      const emptyRecipe =
        new Recipe(
          'TestRecipe',
          [/* Irrelevant for this test */],
          new Map(/* Irrelevant for this test */));

      const recipeDefaults: RecipeUsage = new Map<ArgumentType, Array<ArgumentValue>>([
        ['NAME', ['John', 'Katy', 'Mike']],
        ['AGE', ['18', '23']],
        ['WEIGHT', ['60.9', '80.2']]
      ]);

      const builder = new TaskBuilder();
      const actual = builder['ensureRecipeArgument'](process, emptyRecipe, recipeDefaults);
      expect(actual).to.eql(recipeDefaults);
    });

    it('ensureRecipeArgument - recipeDefaults only - error', function () {
      const process =
        new Process(
          'TestProcess',
          'python script.py {NAME} {AGE} {WEIGHT}',
          [/* Irrelevant for this test */]);
      const emptyRecipe =
        new Recipe('TestRecipe',
          [/* Irrelevant for this test */],
          new Map(/* Irrelevant for this test */));

      const recipeDefaults: RecipeUsage = new Map<ArgumentType, Array<ArgumentValue>>();
      recipeDefaults.set('NAME', ['John', 'Katy', 'Mike']);
      recipeDefaults.set('AGE', ['18', '23']);
      // Misspelled param WEIGHT
      recipeDefaults.set('WEIGTH', ['60.9', '80.2']);

      const builder = new TaskBuilder();
      const expectedErrorMessage = `Required argument "WEIGHT" from process "${process.id}" not found`;
      expect(function () {
        builder['ensureRecipeArgument'](process, emptyRecipe, recipeDefaults);
      }).to.throw(expectedErrorMessage);
    });

    it('ensureRecipeArgument - recipe & recipeDefaults', function () {
      const process =
        new Process(
          'TestProcess',
          'python script.py {NAME} {AGE} {WEIGHT}',
          [/* Irrelevant for this test */]);

      const recipeUsage: RecipeUsage = new Map<ArgumentType, Array<ArgumentValue>>([
        ['NAME', ['John', 'Katy', 'Mike']],
        ['AGE', ['18', '23']]
      ]);

      const recipe = new Recipe('TestRecipe', [/* Irrelevant for this test */], recipeUsage);

      const recipeDefaults: RecipeUsage = new Map<ArgumentType, Array<ArgumentValue>>([
        ['WEIGHT', ['60.5', '80.2', '75.4']]
      ]);

      const builder = new TaskBuilder();
      const actual = builder['ensureRecipeArgument'](process, recipe, recipeDefaults);
      const expected: RecipeUsage = new Map<ArgumentType, Array<ArgumentValue>>([...recipeUsage, ...recipeDefaults]);

      expect(actual).to.eql(expected);
    });

    it('ensureRecipeArgument - recipe & recipeDefaults - error', function () {
      const process =
        new Process(
          'TestProcess',
          'python script.py {NAME} {AGE} {WEIGHT}',
          [/* Irrelevant for this test */]);

      const recipeUsage: RecipeUsage = new Map<ArgumentType, Array<ArgumentValue>>([
        ['NAME', ['John', 'Katy', 'Mike']],
        ['AGE', ['18', '23']]
      ]);

      // Misspelled param WEIGHT
      const recipeDefaults: RecipeUsage = new Map<ArgumentType, Array<ArgumentValue>>([
        ['WEIGHT', ['60.5', '80.2', '75.4']]
      ]);

      const recipe = new Recipe('TestRecipe', [/* Irrelevant for this test */], recipeUsage);
      const builder = new TaskBuilder();
      const expectedErrorMessage = `Required argument "WEIGHT" from process "${process.id}" not found`;

      expect(function () {
        builder['ensureRecipeArgument'](process, recipe, new Map());
      }).to.throw(expectedErrorMessage);
    });
  })();

  // generateArgumentMappings
  (function () {
    it('generateArgumentMappings - recipe only', function () {
      const process =
        new Process(
          'TestProcess',
          'python script.py {NAME} {AGE} {WEIGHT}',
          [/* Irrelevant for this test */]);

      const recipeUsage: RecipeUsage = new Map<ArgumentType, Array<ArgumentValue>>([
        ['NAME', ['John', 'Katy']],
        ['AGE', ['18', '23']],
        ['WEIGHT', ['60', '80']]
      ]);

      const recipe = new Recipe('TestRecipe', [/* Irrelevant for this test */], recipeUsage);

      const builder = new TaskBuilder();
      const actualArgumentMappings: Array<ArgumentMap> =
        builder['generateArgumentMappings'](process, recipe, new Map(/* Irrelevant for this test */));

      const expectedArgumentMappings: Array<ArgumentMap> = new Array<ArgumentMap>(
        new Map([['NAME', 'John'], ['AGE', '18'], ['WEIGHT', '60']]),
        new Map([['NAME', 'John'], ['AGE', '18'], ['WEIGHT', '80']]),
        new Map([['NAME', 'John'], ['AGE', '23'], ['WEIGHT', '60']]),
        new Map([['NAME', 'John'], ['AGE', '23'], ['WEIGHT', '80']]),
        new Map([['NAME', 'Katy'], ['AGE', '18'], ['WEIGHT', '60']]),
        new Map([['NAME', 'Katy'], ['AGE', '18'], ['WEIGHT', '80']]),
        new Map([['NAME', 'Katy'], ['AGE', '23'], ['WEIGHT', '60']]),
        new Map([['NAME', 'Katy'], ['AGE', '23'], ['WEIGHT', '80']])
      );

      expect(actualArgumentMappings).to.deep.equal(expectedArgumentMappings);
    });

    it('generateArgumentMappings - recipeDefaults only', function () {
      const process =
        new Process('TestProcess',
          'python script.py {NAME} {AGE} {WEIGHT}',
          [/* Irrelevant for this test */]);

      const recipeDefaults: RecipeUsage = new Map<ArgumentType, Array<ArgumentValue>>([
        ['NAME', ['John', 'Katy']],
        ['AGE', ['18', '23']],
        ['WEIGHT', ['60', '80']],
      ]);

      const emptyRecipe =
        new Recipe('TestRecipe',
          [/* Irrelevant for this test */],
          new Map(/* Irrelevant for this test */));

      const builder = new TaskBuilder();
      const actualArgumentMappings: Array<ArgumentMap> =
        builder['generateArgumentMappings'](process, emptyRecipe, recipeDefaults);

      const expectedArgumentMappings: Array<ArgumentMap> = new Array<ArgumentMap>(
        new Map([['NAME', 'John'], ['AGE', '18'], ['WEIGHT', '60']]),
        new Map([['NAME', 'John'], ['AGE', '18'], ['WEIGHT', '80']]),
        new Map([['NAME', 'John'], ['AGE', '23'], ['WEIGHT', '60']]),
        new Map([['NAME', 'John'], ['AGE', '23'], ['WEIGHT', '80']]),
        new Map([['NAME', 'Katy'], ['AGE', '18'], ['WEIGHT', '60']]),
        new Map([['NAME', 'Katy'], ['AGE', '18'], ['WEIGHT', '80']]),
        new Map([['NAME', 'Katy'], ['AGE', '23'], ['WEIGHT', '60']]),
        new Map([['NAME', 'Katy'], ['AGE', '23'], ['WEIGHT', '80']]),
      );

      expect(actualArgumentMappings).to.deep.equal(expectedArgumentMappings);
    });

    it('generateArgumentMappings - recipe & recipeDefaults', function () {
      const process =
        new Process(
          'TestProcess',
          'python script.py {NAME} {AGE} {WEIGHT}',
          [/* Irrelevant for this test */]);

      const recipeUsage: RecipeUsage =
        new Map<ArgumentType, Array<ArgumentValue>>([
          ['NAME', ['John', 'Katy']],
          ['AGE', ['18', '23']]
        ]);

      const recipeDefaults: RecipeUsage =
        new Map<ArgumentType, Array<ArgumentValue>>([['WEIGHT', ['60', '80']]]);

      const recipe = new Recipe('TestRecipe', [/* Irrelevant for this test */], recipeUsage);

      const builder = new TaskBuilder();
      const actualArgumentMappings: Array<ArgumentMap> =
        builder['generateArgumentMappings'](process, recipe, recipeDefaults);

      const expectedArgumentMappings: Array<ArgumentMap> = new Array<ArgumentMap>(
        new Map([['NAME', 'John'], ['AGE', '18'], ['WEIGHT', '60']]),
        new Map([['NAME', 'John'], ['AGE', '18'], ['WEIGHT', '80']]),
        new Map([['NAME', 'John'], ['AGE', '23'], ['WEIGHT', '60']]),
        new Map([['NAME', 'John'], ['AGE', '23'], ['WEIGHT', '80']]),
        new Map([['NAME', 'Katy'], ['AGE', '18'], ['WEIGHT', '60']]),
        new Map([['NAME', 'Katy'], ['AGE', '18'], ['WEIGHT', '80']]),
        new Map([['NAME', 'Katy'], ['AGE', '23'], ['WEIGHT', '60']]),
        new Map([['NAME', 'Katy'], ['AGE', '23'], ['WEIGHT', '80']]),
      );

      expect(actualArgumentMappings).to.deep.equal(expectedArgumentMappings);
    });
  })();

  // computeDependencies
  (function () {
    it('computeDependencies - without pruning', function () {

      const p1 = new Process('P1', '{P1_A1} {P1_A2}', [/* Irrelevant for this test */]);
      const p2 = new Process('P2', '{P2_A1} {P2_A2}', ['P1']);

      const r1 = new Recipe('R1', [/* Irrelevant for this test */],
        new Map<ArgumentType, Array<ArgumentValue>>([
          ['P1_A1', ['P1_A1_VA']],
          ['P1_A2', ['P1_A2_VB']],
          ['P2_A1', ['P2_A1_VC', 'P2_A1_VD']],
          ['P2_A2', ['P2_A2_VE', 'P2_A2_VF']]
        ]));

      const r2 = new Recipe('R2', [/* Irrelevant for this test */],
        new Map<ArgumentType, Array<ArgumentValue>>([
          ['P1_A1', ['P1_A1_VH']],
          ['P1_A2', ['P1_A2_VI']],
          ['P2_A1', ['P2_A1_VJ', 'P2_A1_VK']],
          ['P2_A2', ['P2_A2_VL', 'P2_A2_VM']]
        ]));

      const settings: ExperimentSettings = {
        processes: [p1, p2],
        recipes: [r1, r2],
        clusterEndpoint: "", /* Irrelevant for this test */
        recipeDefaults: null /* Irrelevant for this test */
      };

      const p1_r1_1 = new Task(`${p1.id}_${r1.id}_1`, p1.id, r1.id,
        new Command(p1.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P1_A1', 'P1_A1_VA'], ['P1_A2', 'P1_A2_VB']
        ])));
      const p1_r2_1 = new Task(`${p1.id}_${r2.id}_1`, p1.id, r2.id,
        new Command(p1.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P1_A1', 'P1_A1_VH'], ['P1_A2', 'P1_A2_VI']
        ])));
      const p2_r1_1 = new Task(`${p2.id}_${r1.id}_1`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VC'], ['P2_A2', 'P2_A2_VE'],
        ])));
      const p2_r1_2 = new Task(`${p2.id}_${r1.id}_2`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VC'], ['P2_A2', 'P2_A2_VF'],
        ])));
      const p2_r1_3 = new Task(`${p2.id}_${r1.id}_3`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VD'], ['P2_A2', 'P2_A2_VE'],
        ])));
      const p2_r1_4 = new Task(`${p2.id}_${r1.id}_4`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VD'], ['P2_A2', 'P2_A2_VF'],
        ])));
      const p2_r2_1 = new Task(`${p2.id}_${r2.id}_1`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VJ'], ['P2_A2', 'P2_A2_VL'],
        ])));
      const p2_r2_2 = new Task(`${p2.id}_${r2.id}_2`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VJ'], ['P2_A2', 'P2_A2_VM'],
        ])));
      const p2_r2_3 = new Task(`${p2.id}_${r2.id}_3`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VK'], ['P2_A2', 'P2_A2_VL'],
        ])));
      const p2_r2_4 = new Task(`${p2.id}_${r2.id}_4`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VK'], ['P2_A2', 'P2_A2_VM'],
        ])));

      const expectedTasksWithDependencies = new Array<Task>(
        p1_r1_1,

        p1_r2_1,

        p2_r1_1,
        p2_r1_2,
        p2_r1_3,
        p2_r1_4,

        p2_r2_1,
        p2_r2_2,
        p2_r2_3,
        p2_r2_4,
      );

      const expectedTasksWithoutDependencies =
        expectedTasksWithDependencies.map(t => inflate(Task, deflate(t)));

      p2_r1_1.dependencyIds = [p1_r1_1.id];
      p2_r1_2.dependencyIds = [p1_r1_1.id];
      p2_r1_3.dependencyIds = [p1_r1_1.id];
      p2_r1_4.dependencyIds = [p1_r1_1.id];
      p2_r2_1.dependencyIds = [p1_r2_1.id];
      p2_r2_2.dependencyIds = [p1_r2_1.id];
      p2_r2_3.dependencyIds = [p1_r2_1.id];
      p2_r2_4.dependencyIds = [p1_r2_1.id];

      const builder = new TaskBuilder();

      const actualTasks: Array<Task> = builder['computeDependencies'](settings, expectedTasksWithoutDependencies);

      expect(actualTasks).to.deep.equal(expectedTasksWithDependencies);
    });

    it('computeDependencies - with pruning', function () {

      const p1 = new Process('P1', '{P1_A1} {P1_A2} {PR}', [/* Irrelevant for this test */]);
      const p2 = new Process('P2', '{P2_A1} {P2_A2} {PR}', ['P1']);

      const r1 = new Recipe('R1', [/* Irrelevant for this test */],
        new Map<ArgumentType, Array<ArgumentValue>>([
          ['P1_A1', ['P1_A1_VA']],
          ['P1_A2', ['P1_A2_VB']],
          ['P2_A1', ['P2_A1_VC', 'P2_A1_VD']],
          ['P2_A2', ['P2_A2_VE', 'P2_A2_VF']],
          ['PR', ['PR1']]
        ]));

      const r2 = new Recipe('R2', ['PR'], new Map<ArgumentType, Array<ArgumentValue>>([
        ['P1_A1', ['P1_A1_VH']],
        ['P1_A2', ['P1_A2_VI']],
        ['P2_A1', ['P2_A1_VJ', 'P2_A1_VK']],
        ['P2_A2', ['P2_A2_VL', 'P2_A2_VM']],
        ['PR', ['PR2']]
      ]));

      const settings: ExperimentSettings = {
        processes: [p1, p2],
        recipes: [r1, r2],
        clusterEndpoint: "", /* Irrelevant for this test */
        recipeDefaults: null /* Irrelevant for this test */
      };

      const p1_r1_1 = new Task(`${p1.id}_${r1.id}_1`, p1.id, r1.id,
        new Command(p1.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P1_A1', 'P1_A1_VA'], ['P1_A2', 'P1_A2_VB'], ['PR', 'PR1']
        ])));
      const p1_r2_1 = new Task(`${p1.id}_${r2.id}_1`, p1.id, r2.id,
        new Command(p1.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P1_A1', 'P1_A1_VH'], ['P1_A2', 'P1_A2_VI'], ['PR', 'PR2']
        ])));
      const p2_r1_1 = new Task(`${p2.id}_${r1.id}_1`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VC'], ['P2_A2', 'P2_A2_VE'], ['PR', 'PR1']
        ])));
      const p2_r1_2 = new Task(`${p2.id}_${r1.id}_2`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VC'], ['P2_A2', 'P2_A2_VF'], ['PR', 'PR1']
        ])));
      const p2_r1_3 = new Task(`${p2.id}_${r1.id}_3`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VD'], ['P2_A2', 'P2_A2_VE'], ['PR', 'PR1']
        ])));
      const p2_r1_4 = new Task(`${p2.id}_${r1.id}_4`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VD'], ['P2_A2', 'P2_A2_VF'], ['PR', 'PR1']
        ])));
      const p2_r2_1 = new Task(`${p2.id}_${r2.id}_1`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VJ'], ['P2_A2', 'P2_A2_VL'], ['PR', 'PR2']
        ])));
      const p2_r2_2 = new Task(`${p2.id}_${r2.id}_2`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VJ'], ['P2_A2', 'P2_A2_VM'], ['PR', 'PR2']
        ])));
      const p2_r2_3 = new Task(`${p2.id}_${r2.id}_3`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VK'], ['P2_A2', 'P2_A2_VL'], ['PR', 'PR2']
        ])));
      const p2_r2_4 = new Task(`${p2.id}_${r2.id}_4`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VK'], ['P2_A2', 'P2_A2_VM'], ['PR', 'PR2']
        ])));

      const expectedTasksWithDependencies = new Array<Task>(
        p1_r1_1,

        p1_r2_1,

        p2_r1_1,
        p2_r1_2,
        p2_r1_3,
        p2_r1_4,

        p2_r2_1,
        p2_r2_2,
        p2_r2_3,
        p2_r2_4,
      );

      const expectedTasksWithoutDependencies =
        expectedTasksWithDependencies.map(t => inflate(Task, deflate(t)));

      p2_r1_1.dependencyIds = [p1_r1_1.id];
      p2_r1_2.dependencyIds = [p1_r1_1.id];
      p2_r1_3.dependencyIds = [p1_r1_1.id];
      p2_r1_4.dependencyIds = [p1_r1_1.id];

      p2_r2_1.dependencyIds = [p1_r2_1.id];
      p2_r2_2.dependencyIds = [p1_r2_1.id];
      p2_r2_3.dependencyIds = [p1_r2_1.id];
      p2_r2_4.dependencyIds = [p1_r2_1.id];

      const builder = new TaskBuilder();

      const actualTasks: Array<Task> = builder['computeDependencies'](settings, expectedTasksWithoutDependencies);

      expect(actualTasks).to.deep.equal(expectedTasksWithDependencies);
    });
  })();

  // build
  (function () {
    it('build - without pruning', function () {

      const p1 = new Process('P1', '{P1_A1} {P1_A2}', []);
      const p2 = new Process('P2', '{P2_A1} {P2_A2}', ['P1']);

      const r1 = new Recipe('R1', [/* Irrelevant for this test */],
        new Map<ArgumentType, Array<ArgumentValue>>([
          ['P1_A1', ['P1_A1_VA']],
          ['P1_A2', ['P1_A2_VB']],
          ['P2_A1', ['P2_A1_VC', 'P2_A1_VD']],
          ['P2_A2', ['P2_A2_VE', 'P2_A2_VF']]
        ]));

      const r2 = new Recipe('R2', [/* Irrelevant for this test */],
        new Map<ArgumentType, Array<ArgumentValue>>([
          ['P1_A1', ['P1_A1_VH']],
          ['P1_A2', ['P1_A2_VI']],
          ['P2_A1', ['P2_A1_VJ', 'P2_A1_VK']],
          ['P2_A2', ['P2_A2_VL', 'P2_A2_VM']]
        ]));

      const settings: ExperimentSettings = {
        processes: [p1, p2],
        recipes: [r1, r2],
        clusterEndpoint: "", /* Irrelevant for this test */
        recipeDefaults: null /* Irrelevant for this test */
      };

      const p1_r1_1 = new Task(`${p1.id}_${r1.id}_1`, p1.id, r1.id,
        new Command(p1.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P1_A1', 'P1_A1_VA'], ['P1_A2', 'P1_A2_VB']
        ])));
      const p1_r2_1 = new Task(`${p1.id}_${r2.id}_1`, p1.id, r2.id,
        new Command(p1.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P1_A1', 'P1_A1_VH'], ['P1_A2', 'P1_A2_VI']
        ])));
      const p2_r1_1 = new Task(`${p2.id}_${r1.id}_1`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VC'], ['P2_A2', 'P2_A2_VE'],
        ])));
      const p2_r1_2 = new Task(`${p2.id}_${r1.id}_2`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VC'], ['P2_A2', 'P2_A2_VF'],
        ])));
      const p2_r1_3 = new Task(`${p2.id}_${r1.id}_3`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VD'], ['P2_A2', 'P2_A2_VE'],
        ])));
      const p2_r1_4 = new Task(`${p2.id}_${r1.id}_4`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VD'], ['P2_A2', 'P2_A2_VF'],
        ])));
      const p2_r2_1 = new Task(`${p2.id}_${r2.id}_1`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VJ'], ['P2_A2', 'P2_A2_VL'],
        ])));
      const p2_r2_2 = new Task(`${p2.id}_${r2.id}_2`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VJ'], ['P2_A2', 'P2_A2_VM'],
        ])));
      const p2_r2_3 = new Task(`${p2.id}_${r2.id}_3`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VK'], ['P2_A2', 'P2_A2_VL'],
        ])));
      const p2_r2_4 = new Task(`${p2.id}_${r2.id}_4`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['P2_A1', 'P2_A1_VK'], ['P2_A2', 'P2_A2_VM'],
        ])));

      const expectedTasks = new Array<Task>(
        p1_r1_1,

        p1_r2_1,

        p2_r1_1,
        p2_r1_2,
        p2_r1_3,
        p2_r1_4,

        p2_r2_1,
        p2_r2_2,
        p2_r2_3,
        p2_r2_4,
      );

      const builder = new TaskBuilder();
      const actualTasksWithoutDependencies = builder['generateTasks'](settings);
      expect(actualTasksWithoutDependencies).to.deep.equal(expectedTasks);

      p2_r1_1.dependencyIds = [p1_r1_1.id];
      p2_r1_2.dependencyIds = [p1_r1_1.id];
      p2_r1_3.dependencyIds = [p1_r1_1.id];
      p2_r1_4.dependencyIds = [p1_r1_1.id];

      p2_r2_1.dependencyIds = [p1_r2_1.id];
      p2_r2_2.dependencyIds = [p1_r2_1.id];
      p2_r2_3.dependencyIds = [p1_r2_1.id];
      p2_r2_4.dependencyIds = [p1_r2_1.id];

      const actualTasks = builder.build(settings);
      expect(actualTasks).to.deep.equal(expectedTasks);
    });

    it('build - with pruning', function () {

      const p1 = new Process('P1', '{X} {Y}', []);
      const p2 = new Process('P2', '{X} {Y} {Z}', ['P1']);

      const r1 = new Recipe('R1', [], new Map<ArgumentType, Array<ArgumentValue>>([
        ['X', ['X1', 'X2']],
        ['Y', ['Y1']],
        ['Z', ['Z1']]
      ]));

      const r2 = new Recipe('R2', ['X'], new Map<ArgumentType, Array<ArgumentValue>>([
        ['X', ['X1', 'X2']],
        ['Y', ['Y1']],
        ['Z', ['Z1']]
      ]));

      const settings: ExperimentSettings = {
        processes: [p1, p2],
        recipes: [r1, r2],
        clusterEndpoint: "", /* Irrelevant for this test */
        recipeDefaults: null /* Irrelevant for this test */
      };

      const p1_r1_1 = new Task(`${p1.id}_${r1.id}_1`, p1.id, r1.id,
        new Command(p1.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['X', 'X1'], ['Y', 'Y1']
        ])));
      const p1_r1_2 = new Task(`${p1.id}_${r1.id}_2`, p1.id, r1.id,
        new Command(p1.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['X', 'X2'], ['Y', 'Y1']
        ])));

      const p1_r2_1 = new Task(`${p1.id}_${r2.id}_1`, p1.id, r2.id,
        new Command(p1.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['X', 'X1'], ['Y', 'Y1']
        ])));
      const p1_r2_2 = new Task(`${p1.id}_${r2.id}_2`, p1.id, r2.id,
        new Command(p1.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['X', 'X2'], ['Y', 'Y1']
        ])));

      const p2_r1_1 = new Task(`${p2.id}_${r1.id}_1`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['X', 'X1'], ['Y', 'Y1'], ['Z', 'Z1']
        ])));
      const p2_r1_2 = new Task(`${p2.id}_${r1.id}_2`, p2.id, r1.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['X', 'X2'], ['Y', 'Y1'], ['Z', 'Z1']
        ])));

      const p2_r2_1 = new Task(`${p2.id}_${r2.id}_1`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['X', 'X1'], ['Y', 'Y1'], ['Z', 'Z1']
        ])));
      const p2_r2_2 = new Task(`${p2.id}_${r2.id}_2`, p2.id, r2.id,
        new Command(p2.commandTemplate, new Map<ArgumentType, ArgumentValue>([
          ['X', 'X2'], ['Y', 'Y1'], ['Z', 'Z1']
        ])));

      const expectedTasks: Array<Task> = [
        p1_r1_1, p1_r1_2, p1_r2_1, p1_r2_2, p2_r1_1, p2_r1_2, p2_r2_1, p2_r2_2
      ];

      const actualTasksWithoutDependencies: Array<Task> = new TaskBuilder()['generateTasks'](settings);
      expect(actualTasksWithoutDependencies).to.deep.equal(expectedTasks);

      p2_r1_1.dependencyIds = [p1_r1_1.id, p1_r1_2.id];
      p2_r1_2.dependencyIds = [p1_r1_1.id, p1_r1_2.id];

      p2_r2_1.dependencyIds = [p1_r2_1.id];
      p2_r2_2.dependencyIds = [p1_r2_2.id];

      const actualTasks: Array<Task> = new TaskBuilder().build(settings);

      expect(actualTasks).to.deep.equal(expectedTasks);
    })
  })();
});