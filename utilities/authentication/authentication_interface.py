from abc import abstractmethod
from models import User

class AuthenticationInterface: 
    @abstractmethod
    def get_access_token(user: User) -> str:
        pass

    @abstractmethod
    def get_refresh_token(user: User) -> str:
        pass

    @abstractmethod
    def verify_jwt_token(token: str) -> User:
        pass

    @abstractmethod
    def get_hashed_password(password: str) -> str:
        pass

    @abstractmethod
    def verify_password(password: str, hashed_pass: str) -> bool:
        pass

