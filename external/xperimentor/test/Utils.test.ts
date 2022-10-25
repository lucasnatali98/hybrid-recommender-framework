import {expect} from "chai";
import {cartesianProduct, getCommandArgumentTypes} from "../src/Utils";
import {ArgumentType, ArgumentValue} from "../src/TypeAliases";

describe('Utils', function () {
  it('getCommandArgumentTypes', function () {
    const command = 'python mammals.py {LION} {CAT} {DOG} {HUMAN}';
    const expected: Array<ArgumentType> = ['LION', 'CAT', 'DOG', 'HUMAN'];
    const actual = getCommandArgumentTypes(command);
    expect(actual).to.eql(expected);
  });

  it('cartesianProduct', function () {
    const arrays: Array<Array<ArgumentValue>> = [
      ['A1', 'A2'],
      ['B1', 'B2'],
      ['C1', 'C2']
    ];

    const expected: Array<Array<ArgumentValue>> = [
      ['A1', 'B1', 'C1'],
      ['A1', 'B1', 'C2'],
      ['A1', 'B2', 'C1'],
      ['A1', 'B2', 'C2'],
      ['A2', 'B1', 'C1'],
      ['A2', 'B1', 'C2'],
      ['A2', 'B2', 'C1'],
      ['A2', 'B2', 'C2'],
    ];

    const actual = cartesianProduct(arrays);

    expect(expected).to.eql(actual);
  });
});