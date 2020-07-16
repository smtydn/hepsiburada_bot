from src.parser import Parser
from src.email_service import EmailService

if __name__ == '__main__':
    data = Parser.run()
    EmailService.send_mail(data)
