from flask import jsonify
from estacao.exceptions.nocontent import abort, NoContentException
from flask_restful import Resource


from estacao.models import Consolidado, Pressao, Users


class ConsolidadoResource(Resource):
    def get(self, date_from, date_to):
        date_interval = Consolidado.data.between(date_from, date_to)
        query = Consolidado.query.filter(date_interval)
        data = query.all()
        return jsonify(
            {"consolidado": [consolidado.to_dict() for consolidado in data]}
        )


class PressaoResource(Resource):
    def get(self, date_from, date_to):
        date_interval = Pressao.data.between(date_from, date_to)
        query = Pressao.query.filter(date_interval)
        data = query.all()
        return jsonify(
            {"pressao": [pressao.to_dict() for pressao in data]}
        )


class UserResource(Resource):
    def get(self, login):
        try:
            user = Users.query.filter_by(login=login).first() or abort(204)
            response = jsonify(
                {"user": {"id": user.id, "login": user.login}}
            )
        except NoContentException:
            response = jsonify({
                "user": {},
                "status": 204,
                "message": "User not found"
            })
        return response
