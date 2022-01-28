from flask import Request, jsonify

from laketemp import run


def main(request: Request):
    """."""
    print(request.args)
    return jsonify(run(lake_ids=[k for k, v in request.args.items() if v == "true"])), 200
