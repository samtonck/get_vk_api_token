# get_vk_api_token

перед запуском необходимо установить зависимости
```
pip install flask requests
```

запуск осуществляется командой
```
python app.py
```

---

![image](https://github.com/user-attachments/assets/5ef09e27-dc65-40b6-9816-ae4ee7025090)

после завершения авторизации быдет получен токен который можно скопировать через кнопку

![image](https://github.com/user-attachments/assets/1b813620-c790-42bf-82a2-5439f46bc147)


---

Для получения токена понадобится 

###### 1)ID приложения
###### 2)Защищённый ключ


###### * - Доверенный Redirect URL = `http://localhost/api/v1/auth/vk/callback`
![image](https://github.com/user-attachments/assets/dabf75f7-78c6-48e0-ab05-4bf83db37a53)

# *ВАЖНО так же не забудьте, (если требуется) открыть расширеные доступы на странице доступов, например "Видеозаписи"*
по умолчанию в файле ![app.py](https://github.com/samtonck/get_vk_api_token/blob/main/app.py) прописаны все виды доступов 
```
scopes = 'notify,friends,photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,messages,email,notifications,stats,ads,market,offline'
```
![image](https://github.com/user-attachments/assets/3a9694f4-2c10-4bc4-9101-4844f3beb059)


---
---
