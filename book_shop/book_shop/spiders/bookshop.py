import scrapy
import csv


class BookSpider(scrapy.Spider):
    name = 'bookshop'
    start_urls = ['https://bookclub.ua/catalog/books/thriller_horror_books/']
    books = []

    def parse(self, response):
        for link in response.css('div.book-inlist-img a::attr(href)'):
            yield response.follow(link, callback=self.parse_book)

        next_page = response.css('a.pages-arrow:last-child::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        name = response.css('article.prd-m-info-block h1::text').get().strip()
        price = response.css('div.prd-your-price-numb::text').get().strip()
        pages = response.css('div.pereplet::text').get().split(' ')[1]
        genre = response.css('div.prd-attr-descr a::text')[1].get()

        self.books.append({
            'name': name,
            'price': price,
            'pages': pages,
            'genre': genre
        })

    def closed(self, reason):
        fieldnames = ['name', 'price', 'pages', 'genre']

        with open('books.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.books)

        print(self.books)
