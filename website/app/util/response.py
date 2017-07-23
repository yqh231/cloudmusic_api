from flask import jsonify


def JsonSuccess(data):
    response = {
        'code': 0,
        'data': data
    }

    return jsonify(response)


def JsonError(data):
    response = {
        'code': 1,
        'data': data
    }
    return jsonify(response)
