from flask import jsonify, make_response
from src.application.usecase.user import IUserMeUseCase
from src.presentation.api.schema.user import UserMeResponse
from flask.views import MethodView

class UserMe(MethodView):
    def get(self, interactor: IUserMeUseCase):
        x = interactor.handle(user_id=1)
        response = UserMeResponse.from_dto(x)
        return make_response(jsonify(response.model_dump()), 200)
