import {expect} from "chai";
import {Command} from "../src/Command";

describe('Command', function () {
  it('constructor - Invalid argument error', function () {
    expect(function () {
      new Command('{X}');
    }).to.throw('Missing argument mapping for "X"');
  });

  it('getArgument', function () {
    const command =
      new Command('{X} {Y}', new Map([['X', '1'], ['Y', '2']]));

    expect(command.getArgument('X')).to.equal('1');
    expect(command.getArgument('Y')).to.equal('2');
  });

  it('getArgument - error', function () {
    const command =
      new Command('{X} {Y}', new Map([['X', '1'], ['Y', '2']]));

    expect(() => command.getArgument('Z')).to.throw('Argument "Z" not found');
  });

  it('runnableCommand', function () {
    const command =
      new Command('{X} {Y}', new Map([['X', '1'], ['Y', '2']]));

    expect(command.runnableCommand).to.equal('1 2');
  });
});