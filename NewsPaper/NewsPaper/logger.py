import logging
import logging.handlers


DEBUG = True


django_logger = logging.getLogger('django')


console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
console_handler.setLevel(logging.DEBUG)


general_file_handler = logging.FileHandler('general.log')
general_file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
general_file_handler.setFormatter(general_file_formatter)
general_file_handler.setLevel(logging.INFO)


errors_file_handler = logging.FileHandler('errors.log')
errors_file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(pathname)s\n%(exc_info)s')
errors_file_handler.setFormatter(errors_file_formatter)
errors_file_handler.setLevel(logging.ERROR)


security_file_handler = logging.FileHandler('security.log')
security_file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
security_file_handler.setFormatter(security_file_formatter)
security_file_handler.setLevel(logging.INFO)


mail_handler = logging.handlers.SMTPHandler(mailhost=('smtp.example.com', 587),
                                            fromaddr='@example.com',
                                            toaddrs='@example.com',
                                            subject='Ошибка в приложении.')
mail_handler.setLevel(logging.ERROR)
mail_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(pathname)s')
mail_handler.setFormatter(mail_formatter)


console_handler.addFilter(lambda record: DEBUG)
general_file_handler.addFilter(lambda record: not DEBUG)


django_logger.addHandler(console_handler)
django_logger.addHandler(general_file_handler)
django_logger.addHandler(errors_file_handler)
django_logger.addHandler(security_file_handler)


django_request_logger = logging.getLogger('django.request')
django_server_logger = logging.getLogger('django.server')

django_request_logger.addHandler(errors_file_handler)
django_request_logger.addHandler(mail_handler)

django_server_logger.addHandler(errors_file_handler)
django_server_logger.addHandler(mail_handler)