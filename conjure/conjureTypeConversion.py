class ConjureTypeConversion():
    @staticmethod
    def to_conjure_param_text(variable_name, value) -> str:
        if type(value) is bool:
            return "letting {0} be {1}\n".format(variable_name, 'true' if value else 'false')
        if type(value) is dict:
            return "letting {0} be function ({1})".format(variable_name, ", ".join(
                list(map(lambda x: (str(x[0]) + ' --> ' + str(x[1])), value.items())))
            )
        else:
            return "letting {0} be {1}\n".format(variable_name, value)
