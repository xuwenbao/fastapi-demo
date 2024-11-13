from fastapi_demo.models.diocese import Diocese
from fastapi_demo.services.base import BaseService


class DioceseService(BaseService):

    model = Diocese

