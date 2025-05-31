# import db_proxy

class UserAuth:
    """
    UserAuth class handles user authentication operations such as login and signup.
    """

    def __init__(self):
        #user_db = db_proxy
        pass

    def login(self, email: str, password: str):
        # Validate the input data
        if not email or not password:
            raise ValueError("Invalid login data: email and password are required")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Invalid email format")
        
        # Simulate checking credentials
        # Here you would typically check the credentials against a database
        if email != '' or password != '':  # Replace with actual credential check
            return {
                "message": "Login successful",
                "user": {
                    "email": email
                }
            }
        
    def signup(self, name: str, email: str, password: str):
        # Validate the input data
        # Check if email is unique, valid, and password meets security requirements
        if not name or not email or not password:
            raise ValueError("Invalid signup data: name, email, and password are required")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Invalid email format")
        # TODO: check if the email already exists
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        
        # Here you would typically add logic to save the user to a database
        # For this example, we will just return a success message
        return {
            "message": "User signed up successfully",
            "user": {
                "name": name,
                "email": email
            }
        }