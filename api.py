import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """API-библиотека к веб-приложению 'Pet Friends'"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"
        """Магическая функция '__init__' присваивает всем экземплярам класса 'PetFriends' базовый URL"""

    # ЗАДАНИЕ 24.4.1
    def get_api_key(self, email: str, password: str) -> json:
        """Функция делает запрос к API и возвращает статус запроса и результат в формате JSON
        с уникальным ключом пользователя, найденного по указанным email и паролю"""

        headers = {
            "email": email,
            "password": password
        }

        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = '') -> json:
        """Функция делает запрос к API и возвращает статус запроса и результат в формате JSON
        со списком найденных питомцев по указанному фильтру. На данный момент фильтр может иметь либо пустое значение -
        получить список всех питомцев, либо 'my_pets' - получить список собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Функция отправляет на сервер данные о добавляемом питомце
        и возвращает статус запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Функция отправляет на сервер запрос на удаление питомца по указанному id
        и возвращает статус запроса и результат в формате JSON с текстом уведомления об успешном удалении.
        На сегодняшний день тут есть баг - в 'result' приходит пустая строка, но 'status' при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: str) -> json:
        """Функция отправляет запрос на сервер об обновлении данных питомца по указанному id
        и возвращает статус запроса и 'result' в формате JSON с обновленными данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # ИТОГОВОЕ ЗАДАНИЕ 24.7.2
    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Функция добавляет информацию о новом питомце без фото и возвращает информацию в формате JSON"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def set_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Функция добавляет фото питомца к информации о существующем питомце и возвращает информацию в формате JSON"""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result