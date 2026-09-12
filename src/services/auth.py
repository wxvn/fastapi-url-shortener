import uuid

from ..errors import InvalidCredentialsError, AlreadyExistsError
from ..models.user import User
from ..repositories.user import UserRepository
from ..redis.session import SessionStore
from ..utils.password import PasswordHasher

SESSION_TTL = 60 * 60 * 24 * 7

class AuthService:
    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
        session_store: SessionStore,
    ):
        self.repository = repository
        self.password_hasher = password_hasher
        self.session_store = session_store

    async def register(self, user_name: str, password: str) -> tuple[User, str]:
        existing_user = await self.repository.get_user_by_name(user_name)
        if existing_user is not None:
            raise AlreadyExistsError()

        password_hash = self.password_hasher.hash(password)
        user = await self.repository.create_user(user_name, password_hash)

        session_id = str(uuid.uuid4())
        await self.session_store.create(session_id, user.id, SESSION_TTL)

        return user, session_id

    async def login(self, user_name: str, password: str) -> tuple[User, str]:
        user = await self.repository.get_user_by_name(user_name)
        if user is None:
            raise InvalidCredentialsError()

        if not self.password_hasher.verify(password, user.password_hash):
            raise InvalidCredentialsError()

        session_id = str(uuid.uuid4())
        await self.session_store.create(session_id, user.id, SESSION_TTL)

        return user, session_id

    async def logout(self, session_id: str) -> None:
        await self.session_store.delete(session_id)