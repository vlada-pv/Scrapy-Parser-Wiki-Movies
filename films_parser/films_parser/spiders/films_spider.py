import scrapy

class FilmSpider(scrapy.Spider):
    name = "films_spider"
    start_urls = ['https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту']

    def parse(self, response):
        # Парсим список букв со страницы
        letters = response.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr/td/a/@href').getall()

        # Проходим по каждой букве
        for letter in letters:
            yield response.follow(letter, callback=self.parse_letter)

    def parse_letter(self, response):
        # Парсим список фильмов со страницы
        films = response.xpath('//div[@class="mw-category-group"]/ul/li/a/@href').getall()

        # Проходим по каждому фильму
        for film in films:
            yield response.follow(film, callback=self.parse_film)

    def parse_film(self, response):
        # Парсим информацию о фильме
        title = response.xpath('//h1//text()').get()
        genre = response.xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[3]/td/span/a/text()[re:test(., "[а-я]+")] | /html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[4]/td/span/a/text()[re:test(., "[а-я]+")] | /html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[3]/td/span/text()[re:test(., "[а-я]+")]').getall()
        director = response.xpath('//th[contains(text(), "Режиссёр") or contains(text(), "Режиссёры")]/following-sibling::td//a/text()[re:test(., "[А-Я]")]').get() or \
                   response.xpath('//th[contains(text(), "Режиссёр") or contains(text(), "Режиссёры")]/following-sibling::td//span/text()[re:test(., "[А-Я]")]').get()
        country = response.xpath('//th[contains(text(), "Страна") or contains(text(), "Страны")]/following-sibling::td//a/span/text()').getall()
        year = response.xpath('//th[contains(text(), "Год") or contains(text(), "Дата выхода") or contains(text(), "Первый показ")]/following-sibling::td//text()[string-length(normalize-space())=4 and translate(., "0123456789", "")=""]').getall()
        
        # Возвращаем собранную информацию
        yield {
            'Название': title,
            'Жанр/Жанры': genre,
            'Режиссёр': director,
            'Страна/Страны': country,
            'Год': year
        }
    
    

