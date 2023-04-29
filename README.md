# Краулер

---

### [Описание](docs/description.md)

Crawler - производит обход вэб ресурса по указанным правила, и скачивает файлы согласно условиям.
Crawler принимает 4 параметра из них 2 обязательных.

1. __url__ - начальнй url с которого начинается обход ресурса, пример: https://github.com/VIVERA83?tab=repositories
2. __rules__ - правила, по которым ищется следующие ссылки для обхода и скачивание файла

   пример:

```commandline
 rules = [
           # 1 правело (оно отвечает за перемещение по ремурсу)
           ["turbo-frame", # имя тега в котором идет поиск тегов а
            "a",  имя тега "a",
            {"href", атрибуты только которые должны присутствовать
            "itemprop" атрибуты только которые должны присутствовать
            }
            ],
           # 2 правело, по которому производится скачивание файла
           ["tab-container", "a",
             {"class",
              "rel",
              "data-hydro-click",
              "data-ga-click",
              "data-hydro-click-hmac",
              "data-open-app",
              "data-turbo",
              "href"
              }
           ]
         ]
```

3. __count_worker__ - количество запущенных воркеров которые будут работать, по умолчанию 3
4. __count_requests__ - максимальное единовременное обращение в единицу времени к ресурсу, по умолчанию 40

Создание экземпляра класса:

```commandline
   crawler = Crawler(url = "https://github.com/VIVERA83?tab=repositories",
                     rules = [
           # 1 правело (оно отвечает за перемещение по ремурсу)
           ["turbo-frame", # имя тега в котором идет поиск тегов а
            "a",  # имя тега "a",
            {"href", # атрибуты только которые должны присутствовать
            "itemprop" # атрибуты только которые должны присутствовать
            }
            ],
           # 2 правело, по которому производится скачивание файла
           ["tab-container", "a",
             {"class",
              "rel",
              "data-hydro-click",
              "data-ga-click",
              "data-hydro-click-hmac",
              "data-open-app",
              "data-turbo",
              "href"
              }
           ]
         ]
   )
```

Запуск на исполнение:

```commandline
    await crawler.get_result()
```

В результате по кончанию работы будет выведена примерно следующая информация:

```
INFO:Crawler: Creating crawler:  https://gitea.radium.group/radium/project-configuration/
INFO:Crawler: Started crawler:   2023-04-22 00:21:26.853300
INFO:Crawler: Checking:          is_done: False visited: 1 total: 4 queue: 0
INFO:Crawler: Checking:          is_done: False visited: 6 total: 14 queue: 5
INFO:Crawler: Checking:          is_done: False visited: 12 total: 20 queue: 5
INFO:Crawler: Checking:          is_done: False visited: 20 total: 22 queue: 0
INFO:Crawler: Checking:          is_done: True visited: 22 total: 22 queue: 0
INFO:Crawler: Stopped crawler:   2023-04-22 00:21:36.866910
INFO:Crawler: Total time works:  0:00:10.013610
INFO:Crawler: Visited:           22
INFO:Crawler: Total:             22
INFO:Crawler: Downloaded files:  10
8cf77a685a9b2b729f3b3ff4941e5efdbd07888ccfa96923fd1036dffe25314f
f2ec607f67bb0dd3053b49835b02110d5cd0f8eb6da3aac4dc0b142a6b299be9
700f111c1037259067f406c063c3286d1a32e76b9106931bd931ead61975c100
c6c1eaf9d2a84a02474221969810f8485278eaef4653e9db2f1220f0989d556d
7e94c7f4bdfb46be0781c3d734da8389b921254b8fbaad261297cf09d4120383
3f9995629450d6c4d40abd79c5be785cf6a665de48b7688994f17135e03562ae
e9d9941a4f06cacbfb2df1c9ede98db32177ef2a1c641324a46f573a8953ff64
92441118662c296b3a385be8950681bbf0a6795ccd7d854106f3c69dd39c6234
3830c00d8141fa6b3409abffd357a9caaab54953f0dbacafc3a9fc9b9ceaae98
ef2258e7bbbbf51e3bd1012c23a0006233babca23d5c6bf38bad689d8f2f92e1
```

Скаченные фаллы будут храниться в папке __downloads__ в коревом каталоге проекта

### Принцип действия

Crawler(...).get_result() - после вызова данного метода, формируются и запускаются 3 волкера которые отвечают за
обкачку сайта и один воркер отвечает за остановку работы воркеров после окончания обкачки и воркер который занимается
выявлением новых ссылок со скаченных html страниц (работает в отдельном потоке).

В обязанности воркеров на обкачку входит

1. скачавание html html и помещение их в очередь на выявление не помещенных ссылок
2. Скачивание файлов, через [aiofiles](https://pypi.org/project/aiofiles/)
3. подсчет кэша файлов.

В обязанности воркера конролирующего работу входит

1. каждые 2 секунды проверять не пора ли заканчивать работу. Условия остановки: количество осмотерных ссылок равно
   общему количеству

В оркер который занимается выявлением новых

1. берет из очереди страницы и вытаскивать ссылки согласно правилам, после помещать из в очередь для обхода

### Запуск

исполняемый файл находится в app/main.py
---
### Примеры для использования
1. Скачать все открытые репозитории пользователя __vivera83__
```
rules = [
    ["turbo-frame", "a", {"href", "itemprop"}],
    ["li", "a",
     {"class","href", "rel", "data-hydro-click", "data-hydro-click-hmac", "data-ga-click", "data-open-app", "data-turbo"}],
]
URL = "https://github.com/VIVERA83?tab=repositories"
```
