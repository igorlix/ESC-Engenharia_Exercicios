import re

def extrair_emails(texto):
    regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(regex, texto)
    return ' '.join(emails)


if __name__ == '__main__':
    exemplo = 'Favor enviar um e-mail para abc@hotmail.com com cópia para def@abc.com.br'
    resultado = extrair_emails(exemplo)
    print(resultado)
