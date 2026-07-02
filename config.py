import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_SENDER = "sampacast_eventos@adesampa.com.br"
    
    COL_EMAIL = "Usuário - Email"
    COL_NOME = "Usuário - Nome"
    COL_UNIDADE = "Unidade"
    COL_DATA = "Data do Agendamento"
    
    MANUAL_URL = "https://adesampa.com.br/wp-content/uploads/2025/11/Manual-de-conduta-unificado.pdf" 

config = Config()