import scrapy

class BookSpider(scrapy.Spider):
    name = "bookspider"
    start_urls = ["https://books.toscrape.com"]



    def parse(self, response):
            # Loop through each book on the page
            for book in response.css('article.product_pod'):
                yield {
                    'title': book.css('h3 a::attr(title)').get(),
                    'price': book.css('p.price_color::text').get(),
                    'image_link': response.urljoin(book.css('div.image_container img::attr(src)').get()),
                    'rating': book.css('p.star-rating::attr(class)').get().split()[-1]  # Extracts the rating
                }

            # Follow pagination links
            next_page = response.css('li.next a::attr(href)').get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
