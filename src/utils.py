def object_equals_type(obj, object_type):
    print("obj type: ", type(obj))
    print("object_type", type(object_type))
    if type(obj) is object_type:
        return True

    return False

