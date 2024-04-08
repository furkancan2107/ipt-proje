from pydantic import BaseModel, Field, constr

class ChangePasswordRequest(BaseModel):
    activation_code: str = Field(..., title="Aktivasyon Kodu", description="Aktivasyon kodu zorunlu bir alan")
    new_password: constr(min_length=8, max_length=256, regex="^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$") = Field(..., title="Yeni Şifre", description="Lütfen en az bir büyük harf, bir küçük harf ve bir rakam içeren en az 8 karakter uzunluğunda bir şifre kullanın.")
