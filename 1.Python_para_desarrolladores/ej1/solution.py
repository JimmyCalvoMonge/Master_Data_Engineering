import doctest
import re
from datetime import datetime
import logging

logging.basicConfig(filename='ej1.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

"""
Program to analize the logs files of an apache server.
An example of file acommpanies this file: access.log
"""

def get_user_agent(line: str) -> str:
    """
    Get the user agent of the line.
    Buscamos todas las substrings que estan encerradas entre comillas,
    es decir que son de la forma 
    "(.*?)"
    Esperamos que hayan tres de estas, el request, el url y el usuario. Regresamos la última.

    Examples
    ---------
    >>> get_user_agent('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

    >>> get_user_agent('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'
    """
    quotes_oc = re.findall('"(.*?)"', line)
    if len(quotes_oc) >= 3:
        return quotes_oc[2]
    else:
        logging.error('La línea no tiene el formato esperado. No se pudo conseguir el usuario.')


def is_bot(line: str) -> bool:
    '''
    Check of the access in the line correspons to a bot

    Examples
    --------
    >>> is_bot('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    False

    >>> is_bot('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
    True

    >>> is_bot('213.180.203.109 - - [15/Sep/2023:00:12:18 +0200] "GET /robots.txt HTTP/1.1" 302 567 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"')
    True
    '''
    return 'bot' in line.lower()


def get_ipaddr(line):
    '''
    Gets the IP address of the line
    Esperamos que la línea sea de la forma "<ip_address> (.*)"

    >>> get_ipaddr('213.180.203.109 - - [15/Sep/2023:00:12:18 +0200] "GET /robots.txt HTTP/1.1" 302 567 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"')
    '213.180.203.109'

    >>> get_ipaddr('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    '147.96.46.52'
    '''
    return line.split(' ')[0]


def get_hour(line: str) -> int:
    """
    Get the user agent of the line.
    Suponemos que la fecha está en la primera
    ocurrencia de un grupo dentro de paréntesis cuadrados.
    Luego usamos el módulo datetime para obtener
    la hora de la fecha.
    No supe cómo hacer el parsing de '+0200' con
    el módulo datetime así que simplemente hice un split por
    espacio e hice el parsing con el formato '%d/%b/%Y:%H:%M:%S'

    Expamples
    ---------
    >>> get_hour('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
    0

    >>> get_hour('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antacres.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    12
    """
    date_line = re.findall('\[(.*?)\]', line)[0]
    datetime_object = datetime.strptime(date_line.split(' ')[0], '%d/%b/%Y:%H:%M:%S')
    return int(datetime_object.hour)


def histbyhour(filename: str) -> dict[int, int]:
    '''
    Computes the histogram of access by hour.
    Creamos un diccionario cuyas claves son las horas,
    y sus valores son cuantas líneas tienen
    dicha hora. Ponemos el try dentro de la lectura de
    cada línea para evitar que una línea
    incorrecta e intermedia arruine todo el programa.
    '''
    hour_dict = {}
    with open(filename, 'r') as f:
        for log_line in f:
            try:
                hour_line = get_hour(log_line)
                hour_dict[hour_line] = hour_dict.get(hour_line, 0) + 1
            except ValueError as e:
                logging.error(f'Error obteniendo hora: {e}')
    return hour_dict


def ipaddreses(filename: str) -> set[str]:
    '''
    Returns the IPs of the accesses that are not bots
    '''
    ipaddreses_set = set()
    with open(filename, 'r') as f:
        for log_line in f:
            try:
                if not is_bot(log_line):
                    ipadd_line = get_ipaddr(log_line)
                    ipaddreses_set.add(ipadd_line)
            except ValueError as e:
                logging.error(f'Error obteniendo ip address: {e}')
    return ipaddreses_set


def test_doc():
    doctest.run_docstring_examples(get_user_agent, globals(), verbose=True)
    doctest.run_docstring_examples(is_bot, globals(), verbose=True)
    doctest.run_docstring_examples(get_ipaddr, globals(), verbose=True)
    doctest.run_docstring_examples(get_hour, globals(), verbose=True)


def test_ipaddresses(filename: str, ipadds_dict: dict):
    assert ipaddreses(filename) == ipadds_dict


def test_hist(filename: str, hist_dict: dict):
    hist = histbyhour(filename)
    assert hist == hist_dict


def main(filename: str, ip_addresses: set, hist_dict: dict):

    # Ejecutamos las funciones de prueba
    test_doc()
    test_ipaddresses(filename, ip_addresses)
    test_hist(filename, hist_dict)

    logging.info("¡Éxito!")

if __name__ == '__main__':

    # Probar el archivo short:
    ips_add_short = {'34.105.93.183', '39.103.168.88'}
    hist_dict_short = {5: 3, 7: 2, 23: 1}
    main(filename='access_short.log', ip_addresses=ips_add_short, hist_dict=hist_dict_short)

    # Probar el archivo normal:
    ips_add_all = {'203.2.64.59','189.217.221.3', '34.132.45.188',
                   '20.120.74.197', '188.76.13.241', '65.154.226.171',
                   '119.120.163.213', '94.23.8.213', '23.229.104.2',
                   '147.96.60.31', '34.105.93.183', '39.103.168.88',
                   '185.105.102.189', '34.79.162.186'}
    hist_dict_all = {2: 2, 5: 4, 7: 2, 10: 2, 11: 3,
    12: 2, 15: 2, 17: 3, 18: 2, 20: 3, 21: 16, 22: 3, 23: 4}
    main(filename='access.log', ip_addresses=ips_add_all, hist_dict=hist_dict_all)
