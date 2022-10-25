define(function () {

  function performAction() {
    if (this.isEnabled) {
      return this._action();
    }
  }

  return class Button {
    constructor(element, action, enabled = true) {
      this._element = element;
      this._enabled = enabled;
      this._action = action;
      this._element.on('click', () => performAction.call(this));
    }

    enable() {
      this._element.prop('disabled', false);
      this._element.css('cursor', 'pointer');
      this._enabled = true;
    }

    disable() {
      this._element.prop('disabled', true);
      this._element.css('cursor', 'not-allowed');
      this._enabled = false;
    }

    get isEnabled() {
      return this._enabled;
    }
  }
});