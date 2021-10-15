### Регистрация
POST-запрос /api/clients/create/
```
{
    "email": "example@example.ru",
    "password": "string",
    "first_name": "String",
    "last_name": "String",
    "gender": "male",
    "image": image
}
```
Ответ
```
{
    "id": 1,
    "email": "example@example.ru",
    "first_name": "String",
    "last_name": "String",
    "gender": "male",
    "image": "/media/users/example%40example.ru.png"
}
```

### Получение токена
POST-запрос /api/clients/token/
```
{
    "email": "example@example.ru",
    "password": "string"
}
```
Ответ
```
{
    "token": "string"
}
```
Этот токен необходимо передавать в заголовке каждого запроса, в поле 
Authorization. Перед токеном должно стоять ключевое слово Bearer и пробел

### Оценка участника
POST-запрос /api/clients/{id}/match/

Варианты ответов
```
{
    "follower": 1,
    "following": 2
}
```
```
{
    "message": "Вы тоже понравились <имя>! Почта участника: <почта>"
}
```
```
{
    "following": [
        "Ошибка: невозможно понравится самому себе"
    ]
}
```
```
{
    "following": [
        "Ошибка: Вы уже оценивали этого пользователя"
    ]
}
```

### Просмотр списка участников 
GET-запрос /api/list/ (дополнительные параметры поиска 
/?dist=1&first_name=String&last_name=String&gender=female)

Ответ
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "first_name": "String",
            "last_name": "String",
            "gender": "female",
            "image": "/media/users/example%40example.ru.png"
        },
        ...
    ]
}
```