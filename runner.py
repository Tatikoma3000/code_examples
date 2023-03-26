import os
import sys
os.environ['PYTHONASYNCIODEBUG'] = '1'
import scrapy
scrapy.utils.reactor.install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from vkontakte.spiders.vk import VkSpider

'''
Программа реализует сохранение открытой информации о пользователях сети vk.com и их профильной фотографий на локальный 
диск.
Ссылки на интересующие профили необходимо сохранить в файл url_for_search.txt через разделитель \n
Перед выполнением кода программа ищет файл url_for_search.txt. Если его нет - программа завершает работу

В качестве способа сохранения материалов можно использовать NoSQL решения - например, MongoDB, но в таком случае 
у Вас, как у пользователя, у которого отсутствует MongoDB, данная программа не запустится

Для запуска скрипта необходимо запустить runner.py
'''

# Считывание сыылок для парсинга из файла url_for_search.txt
# Если такого файла нет, программа завершает работу
def get_url_for_search():
    path_to_file_with_urls_for_search = os.path.join(os.getcwd(), "url_for_search.txt")
    try:
        with open(path_to_file_with_urls_for_search, 'r', encoding='utf-8') as f:
            urls = f.read().split('\n')
        return urls
    except:
        print('Something wront with file url_for_search.txt')
        input('Нажмите Enter: ')
        sys.exit()


if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()

    process = CrawlerProcess(settings=settings)
    VkSpider.start_urls = get_url_for_search()
    process.crawl(VkSpider)
    process.start()

    print('\n*****************\nDone\n*****************')
