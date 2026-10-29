import datetime
from email.message import EmailMessage
from config import config
from smtplib import SMTP
import pandas as pd
from mensagens import Mensagens

class Parametros_email:

    def retirada_datos_excel(file_path):
        try:
            with SMTP('smtp.gmail.com', 587) as smtp:
                smtp.set_debuglevel(1)
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login('sampacast@adesampa.com.br', 'zrpf uusb kaed eejl'.replace(' ', ''))

                df = pd.read_excel(file_path)
                for email, group in df.groupby(config.COL_EMAIL):
                    primeira_linha = group.iloc[0]
                    name =str(primeira_linha[config.COL_NOME]).split()[0].title()
                    
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
                    mensagem = Parametros_email.mensagem_personalizada(name, historico_formatado)
                    
                    msg = EmailMessage()
                    msg['Subject'] = 'Sampa Cast - Aviso de advertência'
                    msg['From'] = 'sampacast_eventos@adesampa.com.br'
                    msg['To'] = str(email)
                    msg.set_content(mensagem)

                    smtp.send_message(msg)
                    
        except Exception as e:
            print(f'Ocorreu um erro ao processar os dados de entrada da mensagem: {e}')
    

    def mensagem_personalizada(name, historico):
        return (
            f"Olá, {name}! {Mensagens.saudacao_horario()}!\n\n"
            f"Este é um comunicado oficial de PENALIDADE sobre o uso das unidades do Sampa Cast.\n\n"
            f"Devido à reincidência de infrações (faltas ou cancelamentos com menos de 24 horas de antecedência), informamos que sua conta foi bloqueada para o MÊS ATUAL, conforme previsto em nosso manual de conduta. Seguem as agendas referentes à infração:\n\n"
            f"{historico}\n\n"
            f"Desta forma, os agendamentos que você possuía para este mês serão CANCELADOS imediatamente pelo sistema.\n\n"
            f"Ressaltamos que, em caso de comparecimento a qualquer unidade durante este período, VOCÊ NÃO SERÁ ATENDIDO. O acesso aos estúdios está formalmente suspenso e as equipes locais não possuem autorização para abrir exceções.\n\n"
            f"O objetivo desta norma é garantir a disponibilidade dos horários para outros empreendedores em caso de desistências. Você poderá realizar novos agendamentos assim que o bloqueio do mês for encerrado.\n\n"
            f"Segue o link do manual de conduta para consulta:\n"
            f"{config.MANUAL_URL}\n\n"
            f"Atenciosamente,\n"
            f"Equipe Sampa Cast | ADE SAMPA"
        )
