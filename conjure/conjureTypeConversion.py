class ConjureTypeConversion():
    def to_conjure_param_text(variable_name, value):
        if type(value) is bool:
            return "letting {0} be {1}\n".format(variable_name, 'true' if value else 'false')
        else:
            return "letting {0} be {1}\n".format(variable_name, value)