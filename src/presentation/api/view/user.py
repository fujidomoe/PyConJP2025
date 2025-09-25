from flask import jsonify, make_response

from src.application.usecase.user import IUserMeUseCase
from src.domain.model.user import User
from src.presentation.api.schema.user import UserMeResponse
from src.presentation.api.view.base import APIMethodView, me_context


class UserMe(APIMethodView):
    def get(self, interactor: IUserMeUseCase):
        u: User = me_context.get()  # type: ignore
        x = interactor.handle(u)
        response = UserMeResponse.from_dto(x)
        return make_response(jsonify(response.model_dump()), 200)
