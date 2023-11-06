import requests
from requests.exceptions import ConnectionError
import re
import zipfile
import io


class UrlEMT():

    EMT = 'https://opendata.emtmadrid.es/'
    GENERAL = "/Datos-estaticos/Datos-generales-(1)"

    def __init__(self):
        self.valid_urls = UrlEMT.select_valid_urls()

    @staticmethod
    def select_valid_urls() -> list[str]:
        try:
            r = requests.get(f'{UrlEMT.EMT}{UrlEMT.GENERAL}')
            html_text = r.text
            links = UrlEMT.get_links(html_text)
            return links
        except ConnectionError as errc:
            print("Error Connecting:", errc)
            return []

    @staticmethod
    def get_links(htmlText: str) -> list[str]:
        valid_links = re.findall('href="(.*?)trips_(.*?).aspx"', htmlText)
        valid_links = [
            f'{link[0]}trips_{link[1]}.aspx' for link in valid_links]
        return valid_links

    def get_url(self, month: int, year: int) -> str:

        if (month >= 1) and (month <= 12) and (year >= 21) and (year <= 23):

            urlsReturn = [
                link for link in self.valid_urls if
                f'trips_{year}_{str(month).zfill(2)}' in link]

            if len(urlsReturn) == 0:

                raise ValueError(
                    "No link available for this month-year combination")

            else:
                return f'{UrlEMT.EMT}{urlsReturn[0]}'

        else:
            raise ValueError(
                """Month and year need to be integers
                between 1 and 12 and 21 and 23 respectively""")

    def get_csv(self, month: int, year: int) -> io.StringIO:

        url = self.get_url(month, year)
        # Ahora usamos el mismo código que aplicamos en el notebook.
        try:
            r = requests.get(url)
            if r.status_code == 200:
                bytes = io.BytesIO(r.content)
                zfile = zipfile.ZipFile(bytes)
                files = zfile.filelist
                for file in files:
                    if len(re.findall('^trips_(.*?).csv', file.filename)) > 0:
                        with zfile.open(file.filename) as f:
                            contents = f.read()
                        contentstr = contents.decode('utf-8')
                        fstr = io.StringIO(contentstr)
                        return fstr
        except ConnectionError as errc:
            print("Error Connecting:", errc)


if __name__ == '__main__':

    urlemt = UrlEMT()
    for vu in urlemt.valid_urls:
        print(vu)

    print('---')
    print(urlemt.get_url(2, 23))
