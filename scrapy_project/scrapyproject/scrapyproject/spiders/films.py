from typing import Iterable
import scrapy


class FilmsSpider(scrapy.Spider):
    name = "films"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&pagefrom=%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D1%82%D0%B5%D1%82+%28%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%2C+2008%29#mw-pages"]

    def parse_film(self, response):
        if response.css('td.plainlist')[0].css('a::text').get():
            genre = response.css('td.plainlist')[0].css('a::text').get()
        else:
            genre = response.css('td.plainlist > span::text').get()
   
        yield {
            'Name':  response.css('span.mw-page-title-main::text').get(),
            'Genre': genre,
            'Director': response.css('td.plainlist')[1].css('a::text').get(),
            'Country': response.css('span.nowrap::attr(data-sort-value)').get(),
            'Year': response.css('span.dtstart::text').get() 
        }

    def parse(self, response):
        blocks = response.css("div.mw-category-group")[1:]
        links = []

        for block in blocks:
            films_in_block = block.css("ul > li")
            for film in films_in_block:
                links.append('https://ru.wikipedia.org/' + film.css('li > a::attr(href)').get())
        
        next_page = 'https://ru.wikipedia.org' + response.css('#mw-pages > a:nth-child(7)::attr(href)').get()

        for link in links:
            yield response.follow(link, callback=self.parse_film)
        
        yield response.follow(next_page, callback=self.parse)
