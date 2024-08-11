from datetime import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup


class Medals():
    def __init__(self) -> None:
        pass

    def get_response(self) -> object:
        print("Getting data...")
        
        URL = 'https://olympics.com/en/paris-2024/medals'
        HEADERS = {"User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        
        response = requests.get(url=URL, headers=HEADERS)
        # Verifica que la solicitud fue exitosa
        if response.status_code == 200:
            # Parsear el contenido HTML de la respuesta
            self.soup = BeautifulSoup(response.content, 'html.parser')
        else:
            raise Exception(f"Error al realizar la solicitud: {response.status_code}")
        return self.soup
    
    # Extrae y limpia el texto de los elementos encontrados por Span
    def get_by_span(self, span: str) -> list:
        spans = self.soup.select(span)
        values = [span.get_text(strip=True) for span in spans]
        return values

    def get_medals(self, execution_date) -> pd.DataFrame:
        # Selecciona el elemento del medallero usando el XPath
        medallero_div = self.soup.select_one('#p2024-main-content > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(2)')

        # Si se encuentra el medallero, procesa y muestra la información
        if medallero_div:
            medals = self.get_by_span('span.e1oix8v91.emotion-srm-81g9w1')
            
            # se agrupan por grupos de 3 [gold, silver, bronze]
            medals_list = []
            for i,e in enumerate(medals):
                temp = []
                if i % 3 == 0:
                    temp.append(e)
                    temp.append(medals[i + 1])
                    temp.append(medals[i + 2])
                    medals_list.append(temp)

            # Crear DataFrame
            self.medallero_df = pd.DataFrame(medals_list ,columns=['Gold', 'Silver', 'Bronze'])
            # Se agregan los paises al DataFrame
            countries = self.get_by_span('span.euzfwma5.emotion-srm-uu3d5n')
            self.medallero_df.insert(0,'Country', countries, True)

            # Obtener el total de medallas
            self.medallero_df['Total'] = self.medallero_df.apply(lambda x: int(x['Gold']) + int(x['Silver']) + int(x['Bronze']), axis=1)
            # Agregra fecha de ejecucion
            self.medallero_df['execution_date'] = execution_date
            # Settear indice a 1
            self.medallero_df.index += 1
        
            return self.medallero_df

        else:
            raise Exception("No se encontró el medallero en la página.")

    def save_to_csv(self) -> None:
        today = datetime.now().strftime("%Y-%m-%d")
        # name = 'medals_' + str(today) + '.csv'
        name = 'medals.csv'
        self.medallero_df.to_csv(name)


if __name__ == '__main__':
    medals = Medals()
    medals.get_response()
    print(medals.get_medals())
    medals.save_to_csv()