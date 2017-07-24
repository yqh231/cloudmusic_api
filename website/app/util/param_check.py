from flask import request

class Param(object):
    def __init__(self, _type, optional = False):
        self.func = _type
        self.optional = optional


class ParamCheck(object):
    def __init__(self, params):
        self.params = params

    def __call__(self, func):

        def wraps(*args, **kwargs):
            params = {}
            for k, param in self.params.items():
                if not request.values.get(k) and param.optional == False:
                    raise Exception('{}参数必填'.format(k))
                try:
                    value_ = request.values.get(k)
                    if not value_:
                        continue
                    params[k] = param.func(value_)
                except Exception:
                    raise Exception('{}参数类型不对'.format(k))
            return func(params)

        return wraps


