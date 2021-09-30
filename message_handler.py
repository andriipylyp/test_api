class errors:
    def __init__(self, *args) -> None:
        self.arguments = args

    def __str__(self):
        st = ['Wrong data types:']
        [st.append(x) for x in self.arguments]
        return ' '.join(st)

    @staticmethod    
    def wrong_login_pas():
        return 'Wrong login, password.'
    
    @staticmethod
    def login_occupied():
        return 'Login already occupied.'

    @staticmethod
    def user_not_found():
        return 'User not found.'
    
    @staticmethod
    def item_not_found():
        return 'Item not found.'

    @staticmethod
    def nothing_to_receive():
        return 'Nothing to receive.'
    
class api:
    def __init__(self) -> None:
        pass

    @staticmethod
    def operation_success(operation):
        return f'{operation} was successful.'

    @staticmethod
    def not_provided(*args):
        s = 'Not provided:'
        [s.append(x) for x in args]
        return ' '.join(s)
    
    @staticmethod
    def not_logged():
        return 'You are not logged.'

    @staticmethod
    def wrong_type(att, tp):
        return f'{att} must be {tp}'

    
