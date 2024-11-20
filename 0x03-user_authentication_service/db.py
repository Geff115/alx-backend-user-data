#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adding a user to the database"""
        if not email or not hashed_password:
            raise ValueError("Email and hashed_password must be provided")

        # Creating a new instance of User with the email and hashed_password
        user = User(
            email=email,
            hashed_password=hashed_password
        )
        # Adding the new user to the database and committing the changes
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """Finding a user by arbitrary keyword
        arguments.
        """
        if not kwargs:
            raise ValueError("key=value words must be passed in")

        # Querying the user database by the provided **kwargs
        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """This method updates a user's credentials based
        on the user's id.
        """
        if not user_id:
            raise ValueError("A valid user_id must be provided")

        if not kwargs:
            raise ValueError("key=value words must be passed in")

        # Getting the user by user_id
        found_user = self.find_user_by(id=user_id)
        # Updating the found user's attribute by looping through kwargs
        for key, value in kwargs.items():
            if hasattr(User, key):
                setattr(found_user, key, value)
            else:
                raise KeyError(f"Invalid key to update: {key}")

        # Commiting the changes to the database
        self._session.commit()
