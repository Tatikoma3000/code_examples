# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import os
import shutil
import wget

# Класс для парсинга данных к необходимому формату
class VkontaktePipeline:

    # Директория, где будет располагаться хранилище
    starting_directory_for_storage = os.getcwd()

    # Макрос парсинга данных к нужному формату
    def process_item(self, item, spider):

        # Извлечение названия папки для каждого человека, в котором будет храниться информация о нем
        id_folder_name = item['id'][0].split('/')[0]
        path_to_storage_folder = self.create_check_storage_folder_for_each_person(id_folder_name)

        # Парсинг имени и фамилии человека
        if item["last_name"][0] != False:
            txt_name = item["first_name"][0] + ' ' + item["last_name"][0]
        else:
            txt_name = item["first_name"][0]
        path_to_txt_file = os.path.join(path_to_storage_folder, txt_name + '.txt')

        # Парсинг даты рождения
        if item["birthday"][0] != False and item["birthyear"][0] != False:
            birthday = f'{item["birthday"][0]} {item["birthyear"][0]}'
        elif item["birthday"][0] == False and item["birthyear"][0] != False:
            birthday = f'{item["birthyear"][0]} year'
        elif item["birthday"][0] != False and item["birthyear"][0] == False:
            birthday = f'{item["birthday"][0]}'
        else:
            birthday = 'No information'

        # Парсинг статуса
        if item["status"][0] != False:
            status = item["status"][0]
        else:
            status = 'Currently has no status'

        # Парсинг текущего города
        if item["city"][0] != False:
            city = item["city"][0].replace('Current city: ', '')
        else:
            city = 'Currently has no city'

        # Парсинг количества фотографий
        if item["photo_count"][0] != False:
            photos = item["photo_count"][0].replace(',', '')
        else:
            photos = 'Currently has no photos'

        # Парсинг количества видеофайлов
        if item["video_count"][0] != False:
            videos = item["video_count"][0].replace(',', '')
        else:
            videos = 'Currently has no videos'

        # Парсинг количества сообществ
        if item["communities"][0] != False:
            communities = item["communities"][0].replace(',', '')
        else:
            communities = 'Currently has no communities'

        # Парсинг количества подписок
        if item["subscriptions"][0] != False:
            subscriptions = item["subscriptions"][0].replace(',', '')
        else:
            subscriptions = 'Currently has no subscriptions'

        # Парсинг количества подписчиков
        if item["followers"][0] != False:
            followers = item["followers"][0].replace(',', '').replace(' followers', '')
        else:
            followers = 'Currently has no followers'

        # Парсинг ссылки на фотографию профиля
        if item['photo_link'][0] != False:
            path_to_profile_photo = os.path.join(path_to_storage_folder, 'profile_photo.jpg')
            wget.download(item['photo_link'][0][23:-2], out=path_to_profile_photo)
        else:
            path_to_profile_photo = 'Currently has no photo'

        # Запись спаршенных данных в файл
        with open(path_to_txt_file, 'w', encoding='utf-8') as f:
            f.write(f'id: {id_folder_name}\n')
            f.write(f'Name: {txt_name}\n')
            f.write(f'Birthday: {birthday}\n')
            f.write(f'current status: {status}\n')
            f.write(f'current city: {city}\n')
            f.write(f'path_to_profile_photo: {path_to_profile_photo}\n')
            f.write('\n')
            f.write('Current profile status:\n')
            f.write(f'Photos: {photos}\n')
            f.write(f'Videos: {videos}\n')
            f.write(f'Communities: {communities}\n')
            f.write(f'Subscriptions: {subscriptions}\n')
            f.write(f'Followers: {followers}\n')

    # Функция отвечает за создание структуры хранилища.
    # Функция создает папку хранения информации от каждого id и возвращает полный путь к папке
    # Если папка с названием id существует - удаляет все содержимое папки (чтобы в дальнейшем информация обновилась)
    # В качестве альтернативы к данной функции можно развернуть MongoDB и работать через PyMongo.
    def create_check_storage_folder_for_each_person(self, folder_name):

        # Название головной папки - хранилища
        name_for_storage_folder = 'storage_information'

        # Полный путь до головной папки - хранилища
        full_path_to_storage_folder = os.path.join(self.starting_directory_for_storage, name_for_storage_folder)

        # Проверка, существует ли головная папка -хранилище. Если нет, создает ее
        if not os.path.exists(full_path_to_storage_folder):
            os.mkdir(full_path_to_storage_folder)

        # Полный путь к папке - хранилищу информации для каждого пользователя
        full_path_to_storage_folder_for_each_person = os.path.join(full_path_to_storage_folder, folder_name)

        # Если папка с пользователем существует - удаляет содержимое папки, если не существует - создает пустую папку
        if not os.path.exists(full_path_to_storage_folder_for_each_person):
            os.mkdir(full_path_to_storage_folder_for_each_person)
        else:
            self.clear_folder(full_path_to_storage_folder_for_each_person)

        # Возвращает полный путь к папке пользователя
        return full_path_to_storage_folder_for_each_person

    # Функция для очистки содержимого папки (обнуление содержимого)
    @staticmethod
    def clear_folder(path_to_folder: str):
        for element in os.listdir(path_to_folder):
            path_to_element = os.path.join(path_to_folder, element)
            try:
                if os.path.isdir(path_to_element):
                    shutil.rmtree(path_to_element)
                elif os.path.isfile(path_to_element):
                    os.remove(path_to_element)
                else:
                    print(f"Can't remove: {path_to_element}")
            except Exception as e:
                print(f"Failed to delete: {path_to_element}. Reason: {e}")
