import scrapy
from scrapy.http import HtmlResponse
from vkontakte.items import VkontakteItem
from scrapy.loader import ItemLoader


class VkSpider(scrapy.Spider):
    name = "vk"
    allowed_domains = ["vk.com"]
    start_urls = ["https://m.vk.com/id274583833", "https://m.vk.com/id44625516", "https://m.vk.com/id135336811"]

    def parse(self, response: HtmlResponse):

        # Ссылка на страницу с личной информацией пользователя
        page_to_personal_information = response.url + response.xpath(
            "//div[@class='OwnerInfo__row OwnerInfo__row--extraMargin']/a/@href").get()

        # Переход на страницу с личной информацией о человеке
        yield response.follow(page_to_personal_information, self.parse_profile_information)

    def parse_profile_information(self, response: HtmlResponse):

        # Парсинг открытой информации о человеке
        first_name, last_name = self.clear_first_name_last_name(
            response.xpath("//h2[@class = 'op_header']/text()").get())

        city = response.xpath("//div[contains(text(), 'Current city')]/text()").get()
        status = response.xpath("//div[@class = 'pp_full_status']/text()").get()
        birthday = response.xpath("//a[contains(@href, 'bday')]/text()").get()
        birthyear = response.xpath("//a[contains(@href, 'byear')]/text()").get()
        followers = response.xpath("//a[contains(@href, 'act=fans')]//text()").get()
        photo_count = response.xpath(
            "//div[@class = 'Menu__itemTitle'][contains(text(), 'Photos')]/parent::div/div[3]/text()").get()
        video_count = response.xpath(
            "//div[@class = 'Menu__itemTitle'][contains(text(), 'Videos')]/parent::div/div[3]/text()").get()
        communities_count = response.xpath(
            "//div[@class = 'Menu__itemTitle'][contains(text(), 'Communities')]/parent::div/div[3]/text()").get()
        subscription_count = response.xpath(
            "//div[@class = 'Menu__itemTitle'][contains(text(), 'Following')]/parent::div/div[3]/text()").get()
        photo_link = response.xpath("//div[@class='Avatar__image Avatar__image-1']/@style").get()

        # Передача данных в pipeline
        loader = ItemLoader(item=VkontakteItem(), response=response)
        loader.add_value('first_name', self.replace_null_value_if_necessary(first_name))
        loader.add_value('last_name', self.replace_null_value_if_necessary(last_name))
        loader.add_value('status', self.replace_null_value_if_necessary(status))
        loader.add_value('city', self.replace_null_value_if_necessary(city))
        loader.add_value('birthday', self.replace_null_value_if_necessary(birthday))
        loader.add_value('birthyear', self.replace_null_value_if_necessary(birthyear))
        loader.add_value('followers', self.replace_null_value_if_necessary(followers))
        loader.add_value('photo_count', self.replace_null_value_if_necessary(photo_count))
        loader.add_value('video_count', self.replace_null_value_if_necessary(video_count))
        loader.add_value('communities', self.replace_null_value_if_necessary(communities_count))
        loader.add_value('subscriptions', self.replace_null_value_if_necessary(subscription_count))
        loader.add_value('id', self.get_id(response.url))
        loader.add_value('photo_link', self.replace_null_value_if_necessary(photo_link))
        yield loader.load_item()

    # Функция для очистки имени и фамилии от лишней информации (пробелы, \n)
    @staticmethod
    def clear_first_name_last_name(name: str):
        name = name.replace('\n', '')
        name_parts = [el for el in name.split() if el]
        return name_parts[0], name_parts[1]

    # Функция возвращает id - уникальное название папки, в которой будет храниться информация о данном человеке
    @staticmethod
    def get_id(page_url: str):
        return page_url.replace('https://m.vk.com/', '').replace('?act=info', '')

    # Функция обрабатывает Null-значения для возвращения их в scrapy.LoadItem()
    # Scrapy не поддерживает Null-значения в scrapy.LoadItem()
    @staticmethod
    def replace_null_value_if_necessary(value: str, replacement_position=False):
        if value:
            return value
        else:
            return replacement_position
