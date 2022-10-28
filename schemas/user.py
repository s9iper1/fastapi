from pydantic import BaseModel, validator, validate_email


class User(BaseModel):
    name: str | None
    email: str | None
    password: str | None
    profile_image: str | None

    @validator("email")
    def validate_email(cls, values):
        validate = validate_email(values)
        print(f'valid email {validate}')

        if not validate:
            raise ValueError("Enter Correct email")
        return values

    @validator("password")
    def check_password_length(cls, values):
        if len(values) <= 4:
            raise ValueError("Password must be of 5 character")
        return values
