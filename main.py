import string
import json
import pydantic

from typing import List, Optional
from pathlib import Path

# Existing Path
path_cwd = Path.cwd()
path_data = path_cwd / "data"

# Existing Files
file_json_a = path_data / "data.json"
file_json_b = path_data / "test_data_0001.json"
file_json_c = path_data / "test_data_0002.json"

# Current file to be tested
current_file = file_json_b

class User(pydantic.BaseModel):
    username: str
    password: str
    age: int
    score: float
    
    email: Optional[str]
    phone_number: Optional[str]
    
    @pydantic.validator("username")
    @classmethod
    def validate_username(cls, value):
        if any(p in value for p in string.punctuation):
            raise ValueError("Username must not include punctuation or special characters.")
        else:
            return value
        
    @pydantic.validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be atleast 8 characters long.")
        if any(p in value for p in string.punctuation):
            if any(d in value for d in string.digits):
                if any(l in value for l in string.ascii_lowercase):
                    if any(u in value for u in string.ascii_uppercase):
                        return value
        raise ValueError("Password needs at least one punctuation symbol, digit, upper and lower case string.")
    
    @pydantic.validator("age", "score")
    @classmethod
    def validate_number(cls, value):
        if value >= 0:
            return value
        else:
            raise ValueError("Numbers must be a integer or float")


def main() -> None:
    """ Main function. """

    # Read data from a JSON file
    with open(current_file) as file:
        datas = json.load(file)
        
        # Check and parse the given JSON data.
        try:
            books: List[Book] = [User(**item) for item in datas]
        except:
            print("-"*50)
            print("Try Again...")
            print("-"*50)


if __name__ == "__main__":
    main()
    
    print("-"*50)
    print("File Executed...")
    print("-"*50)
