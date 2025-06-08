from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):
    @abstractmethod
    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        """
        Finds the password from the passed username.

        Returns the password if there is one.

        :param username: username
        :return: password by user, if found
        """

    @classmethod
    def check_passwords_match(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        """
        Checking passwords for a match.

        :param password1: first password
        :param password2: second password
        :return:Boolean value of the comparison result
        """
        return password1 == password2

    def validate_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
        Check if the password is valid.

        :param username: whose password to check
        :param password: passed password. Check against the one in the database
        :return: True if they match, otherwise False
        """
        db_password = self.get_user_password(username)
        if db_password is None:
            return False
        return self.check_passwords_match(
            password1=password,
            password2=db_password,
        )
