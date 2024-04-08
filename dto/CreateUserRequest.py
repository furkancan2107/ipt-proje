from pydantic import BaseModel, Field, EmailStr, constr

class CreateUserDto(BaseModel):
    username: str = Field(..., title="Kullanıcı Adı", description="Kullanıcı adı girmek zorunludur")
    email: EmailStr = Field(..., title="E-posta", description="E-posta girmek zorunludur. Lütfen doğru bir biçimde email adresi girin")
    password: constr(min_length=8, max_length=256, regex="^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$") = Field(..., title="Şifre", description="Lütfen en az bir büyük harf, bir küçük harf ve bir rakam içeren en az 8 karakter uzunluğunda bir şifre kullanın.")
