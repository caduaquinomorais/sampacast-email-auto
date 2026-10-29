import logging
from datetime import datetime
from email.message import EmailMessage
from smtplib import SMTP
import pandas as pd
from config import config

logging.basicConfig(level=logging.INFO)

class ServicoEmail:
    
    @staticmethod
    def saudacao_horario():
        """Gera saudação com base no horário atual (independente do script de WhatsApp)"""
        now = datetime.now().time()
        if now < datetime.strptime("13:00:00", "%H:%M:%S").time():
            return "Bom dia"
        else:
            return "Boa tarde"

    @staticmethod
    def mensagem_personalizada(name, historico):
        return (
            f"Olá, {name}! {ServicoEmail.saudacao_horario()}!\n\n"
            f"Este é um comunicado oficial de PENALIDADE sobre o uso das unidades do Sampa Cast.\n\n"
            f"Devido à reincidência de infrações (faltas ou cancelamentos com menos de 24 horas de antecedência), informamos que sua conta foi bloqueada para o MÊS ATUAL, conforme previsto em nosso manual de conduta. Segue agendas referentes a infração:\n\n"
            f"{historico}\n\n"
            f"Desta forma, os agendamentos que você possuía para este mês serão CANCELADOS imediatamente pelo sistema.\n\n"
            f"É importante ressaltar que, em caso de comparecimento em qualquer unidade durante este mês, VOCÊ NÃO SERÁ ATENDIDO. O acesso aos estúdios está formalmente suspenso e as equipes locais não têm autorização para abrir exceções durante o período de penalidade.\n\n"
            f"O objetivo desta norma é garantir que os horários fiquem disponíveis para outros empreendedores quando houver desistências. Você poderá realizar novos agendamentos assim que o bloqueio do mês atual for encerrado.\n\n"
            f"Segue link do manual de conduta para consulta:\n"
            f"{config.MANUAL_URL}\n\n"
            f"Atenciosamente,\n"
            f"Equipe Sampa Cast | ADE SAMPA"
        )

    @staticmethod
    def processar_e_enviar(caminho_excel):
        
        # Validação de segurança básica antes de iniciar o SMTP
        if not config.EMAIL_USER or not config.EMAIL_PASS:
            logging.error("Credenciais de e-mail não encontradas no arquivo .env!")
            return

        try:
            logging.info("Conectando ao servidor SMTP...")
            with SMTP(config.EMAIL_HOST, config.EMAIL_PORT) as smtp:
                # smtp.set_debuglevel(1) # Descomente para ver o log completo do envio
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(config.EMAIL_USER, config.EMAIL_PASS)
                logging.info("Login realizado com sucesso.")

                df = pd.read_excel(caminho_excel)
                
                # Agrupa por e-mail para evitar envios duplicados para a mesma pessoa
                for email, group in df.groupby(config.COL_EMAIL):
                    primeira_linha = group.iloc[0]
                    name = str(primeira_linha[config.COL_NOME]).split()[0].title()
                    
                    data_lista = []
                    for i, row in group.iterrows():
                        unid = str(row[config.COL_UNIDADE]).strip()
                        data_raw = row[config.COL_DATA]
                        
                        if hasattr(data_raw, 'strftime'):
                            data_formatada = data_raw.strftime('%d/%m/%Y')
                        else:
                            data_formatada = str(data_raw)

                        data_lista.append(f'\t📅 {unid} no dia {data_formatada}')

                    historico_formatado = '\n'.join(data_lista)
                    mensagem = ServicoEmail.mensagem_personalizada(name, historico_formatado)
                    
                    msg = EmailMessage()
                    msg['Subject'] = 'Sampa Cast - Aviso de advertência'
                    msg['From'] = config.EMAIL_SENDER
                    msg['To'] = str(email)
                    msg.set_content(mensagem)

                    logging.info(f"Enviando e-mail para: {email}")
                    smtp.send_message(msg)
                    
            logging.info("Processo de e-mails concluído.")
                    
        except Exception as e:
            logging.error(f'Ocorreu um erro ao processar os dados de entrada da mensagem: {e}')