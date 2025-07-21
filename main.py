import os

from dotenv import load_dotenv
import telebot
from telebot import types
from telebot.types import ReplyKeyboardRemove
import requests

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# File to store card number
CARD_FILE = 'card.txt'

def get_card_number():
    if not os.path.exists(CARD_FILE):
        return None
    with open(CARD_FILE, 'r') as f:
        return f.read().strip()

def set_card_number(number: str):
    with open(CARD_FILE, 'w') as f:
        f.write(number)

ADMIN_ID = 7659986817
# Crypto payment support
CRYPTO_CURRENCIES = ['BTC', 'ETH', 'LTC', 'SOL', 'TON', 'USDT trc20', 'USDT erc20']
CRYPTO_IDS = {
    'BTC': 'bitcoin', 'ETH': 'ethereum', 'LTC': 'litecoin',
    'SOL': 'solana', 'TON': 'the-open-network', 'USDT trc20': 'tether',
    'usdt erc20': 'tether'
}
CRYPTO_ADDRESSES = {
    'BTC': os.getenv('BTC_ADDRESS'),
    'ETH': os.getenv('ETH_ADDRESS'),
    'LTC': os.getenv('LTC_ADDRESS'),
    'SOL': os.getenv('SOL_ADDRESS'),
    'TON': os.getenv('TON_ADDRESS'),
    'USDT trc20': os.getenv('TRC_ADDRESS'),
    'USDT erc20': os.getenv('ERC_ADDRESS')
}
bot = telebot.TeleBot(TOKEN)

# Данные по городам
CITIES = [
    # Беларусь
    {'country': '🇧🇾', 'name': 'Минск'},
    {'country': '🇧🇾', 'name': 'Витебск'},
    {'country': '🇧🇾', 'name': 'Гродно'},
    {'country': '🇧🇾', 'name': 'Брест'},
    # Украина
    {'country': '🇺🇦', 'name': 'Киев'},
    {'country': '🇺🇦', 'name': 'Одесса'},
    {'country': '🇺🇦', 'name': 'Львов'},
    # Россия (примерно 25 городов)
    {'country': '🇷🇺', 'name': 'Москва'},
    {'country': '🇷🇺', 'name': 'Санкт-Петербург'},
    {'country': '🇷🇺', 'name': 'Новосибирск'},
    {'country': '🇷🇺', 'name': 'Екатеринбург'},
    {'country': '🇷🇺', 'name': 'Казань'},
    {'country': '🇷🇺', 'name': 'Нижний Новгород'},
    {'country': '🇷🇺', 'name': 'Челябинск'},
    {'country': '🇷🇺', 'name': 'Самара'},
    {'country': '🇷🇺', 'name': 'Омск'},
    {'country': '🇷🇺', 'name': 'Ростов-на-Дону'},
    {'country': '🇷🇺', 'name': 'Уфа'},
    {'country': '🇷🇺', 'name': 'Красноярск'},
    {'country': '🇷🇺', 'name': 'Воронеж'},
    {'country': '🇷🇺', 'name': 'Пермь'},
    {'country': '🇷🇺', 'name': 'Волгоград'},
    {'country': '🇷🇺', 'name': 'Краснодар'},
    {'country': '🇷🇺', 'name': 'Саратов'},
    {'country': '🇷🇺', 'name': 'Тюмень'},
    {'country': '🇷🇺', 'name': 'Тольятти'},
    {'country': '🇷🇺', 'name': 'Ижевск'},
    {'country': '🇷🇺', 'name': 'Барнаул'},
    {'country': '🇷🇺', 'name': 'Ульяновск'},
    {'country': '🇷🇺', 'name': 'Иркутск'},
    {'country': '🇷🇺', 'name': 'Хабаровск'},
    {'country': '🇷🇺', 'name': 'Ярославль'},
    {'country': '🇷🇺', 'name': 'Владивосток'},
    {'country': '🇷🇺', 'name': 'Махачкала'},
    {'country': '🇷🇺', 'name': 'Томск'},
    {'country': '🇷🇺', 'name': 'Оренбург'},
    {'country': '🇷🇺', 'name': 'Кемерово'},
    {'country': '🇷🇺', 'name': 'Новокузнецк'},
]

CITIES_PER_PAGE = 10

# Словарь для хранения рефералов (user_id: [ref_ids])
user_referrals = {}

# Словарь для хранения пользователей (user_id: referrer_id)
user_referrers = {}

# Список товаров как объектов
GOODS = [
    {'name': 'Кристаллы', 'price': 1000},
    {'name': 'Монеты', 'price': 1500},
    {'name': 'Энергия', 'price': 2000},
    {'name': 'Бустер', 'price': 2500},
    {'name': 'VIP-статус', 'price': 3000},
]

# --- Каталог с категориями, подкатегориями и товарами ---
CATALOG_TREE = [
    {
        'name': 'Стимуляторы',
        'subcategories': [
            {
                'name': 'Кокаин',
                'products': [
                    {
                        'name': 'VHQ Кокаин (Колумбия)',
                        'amounts': [{'caption': '1г | 7900₽ | Прикоп', 'price': 7900}, {'caption': '2г | 15500₽ | Прикоп', 'price': 15500}, {'caption': '5г | 31000₽ | Магнит', 'price': 31000}],
                        'img': 'кокаин.jpg',
                        'description': 'Глянец, качество, блаженство. Разве стоит проходить мимо такого продукта?\n\nВАЖНО:\nПри соблюдении рекомендуемой дозировки, лишней мокроты в носу не будет, а отход ко сну будет лёгким и приятным уже через час - полтора с последнего применения.',
                        'reviews': [{
                            'name': 'Аноним',
                            'stars': 5,
                            'caption': 'охуенно'
                        }]
                    },
                    {
                        'name': 'Кокаин VHQ FishScale Prada',
                        'amounts': [{'caption': '4г | 39400₽ | Тайник', 'price': 39400}, {'caption': '5г | 49900₽ | Тайник', 'price': 49900}, {'caption': '8г | 77000₽ | Магнит', 'price': 77000}],
                        'img': 'кокаин2.jpg',
                        'description': 'Фишскейл импортного производства. Любое мероприятие, вечеринка или же ночь романтики со второй половинкой заиграют новыми красками в ваших глазах, оставив уйму приятных воспоминаний. Прикоснись к прекрасному вместе с нами!\n\nНазально - 30-60 мг. Ожидание составляет в среднем 3-5 минут.',
                        'reviews': [{
                            'name': 'Аноним',
                            'stars': 5,
                            'caption': 'охуенно'
                        }]
                    },
                    {
                        'name': 'Кокаин F1 ',
                        'amounts': [{'caption': '1г | 10900₽ | Прикоп', 'price': 10900}, {'caption': '10г | 89000₽ | Тайник', 'price': 89000}],
                        'img': 'кокаин3.jpg',
                        'description': 'Кокаин F1 - это мощь сверхбыстрых спортивных тачек, приятная кокейновая эйфория и высочайшая надежность кладов. Прибавьте к этому поддержку уровня “мечта” - и получите лучшую кокаиновую сделку из возможных!\n\nНадо отметить, что продукт настолько чистый и правильный, что он идеально подходит для варки крека как на аммиаке, так и на соде.',
                        'reviews': [{
                            'name': 'Аноним',
                            'stars': 5,
                            'caption': 'охуенно'
                        }]
                    },
                ]
            },
            {
                'name': 'Амфетамин',
                'products': [
                    {
                        'name': 'Амфетамин WHITE',
                        'amounts': [{'caption': '5г | 5900₽ | Тайник', 'price': 5900}, {'caption': '6г | 6500₽ | Прикоп', 'price': 6500}, {'caption': '10г | 8900₽ | Магнит', 'price': 8900}],
                        'img': 'амф2.jpg',
                        'description': 'Топовое качество. Цвет - белый.',
                        'reviews': [{
                            'name': 'Аноним',
                            'stars': 5,
                            'caption': 'охуенно'
                        }]
                    },
                    {
                        'name': 'Амфетамин PREMIUM',
                        'amounts': [{'caption': '3г | 5000₽ | Тайник', 'price': 5000}, {'caption': '5г | 7800₽ | Тайник', 'price': 7800}, {'caption': '10г | 14000₽ | Магнит', 'price': 14000}],
                        'img': 'амф.jpg',
                        'description': 'Представляем амфетамин 99.9% еще с тех 2000-х годов! Лучшая версия классического стимулятора для тех, кто ищет максимальный стим и эйфорию! Центральное стимулирующее действие амфетамина выражается в улучшении настроения, повышении внимания и способности к концентрации, а также в появлении чувства уверенности и комфорта. повышает двигательную и речевую активность, уменьшает сонливость и аппетит, повышает работоспособность. Производится с использованием только химически чистых, безопасных реагентов и растворителей. Обеспечивает приятное и долгое действие',
                        'reviews': [{
                            'name': 'Аноним',
                            'stars': 5,
                            'caption': 'охуенно'
                        }]
                    }
                ]
            },
            {
                'name': 'Метамфетамин',
                'products': [
                    {
                        'name': 'Метамфетамин VHQ+ Декстра',
                        'amounts': [{'caption': '3г | 9900₽ | Магнит', 'price': 9900}, {'caption': '1г | 3500₽ | Магнит', 'price': 3500}, {'caption': '7г | 22700₽ | Магнит', 'price': 22700}],
                        'img': 'амф.jpg',
                        'description': 'Представляем амфетамин 99.9% еще с тех 2000-х годов! Лучшая версия классического стимулятора для тех, кто ищет максимальный стим и эйфорию! Центральное стимулирующее действие амфетамина выражается в улучшении настроения, повышении внимания и способности к концентрации, а также в появлении чувства уверенности и комфорта. повышает двигательную и речевую активность, уменьшает сонливость и аппетит, повышает работоспособность. Производится с использованием только химически чистых, безопасных реагентов и растворителей. Обеспечивает приятное и долгое действие',
                        'reviews': [{
                            'name': 'Аноним',
                            'stars': 5,
                            'caption': 'охуенно'
                        }]
                    },
                    {
                        'name': 'Метамфетамин D-изомер',
                        'amounts': [{'caption': '2г | 27900₽ | Магнит', 'price': 27900}, {'caption': '4г | 53900₽ | Магнит', 'price': 53900}, {'caption': '9г | 109000₽ | Магнит', 'price': 109000}],
                        'img': 'амф.jpg',
                        'description': 'Метамфетамин D-изомер который вы давно ждали!',
                        'reviews': [{
                            'name': 'Аноним',
                            'stars': 5,
                            'caption': 'охуенно'
                        }]
                    },
                    {
                        'name': 'Метамфетамин L-изомер',
                        'amounts': [{'caption': '1г | 2300₽ | Прикоп', 'price': 2300}, {'caption': '6г | 12000₽ | Магнит', 'price': 1200}],
                        'img': 'мет.jpg',
                        'description': 'Классический стимулятор с хорошо изученным воздействием на организм. Продукт с уклоном в чистую стимуляцию, замечательно подходит для работы. Также можно использовать как более долгую и безопасную АЛЬТЕРНАТИВУ A-PVP. Отличная возможность вырваться из апвп-марафона и вернуть контроль над ситуацией, комфортные трипы без солевой шизы',
                        'reviews': [{
                            'name': 'Аноним',
                            'stars': 5,
                            'caption': 'Давно хотел мет! Соль и амф уже не те, что были несколько лет назад а амф из нулевых и начала десятых и вообще думаю сложно найти. Услышал про лёд и вот через полтора года он у меня. Взял на пробу именно этот, чтоб было с чем сравнивать потом. Клад исполнен пушка, с первого раза я и не нашёл, постоял подумал и вот они две колбы в кармане а до дома изнурительные почти четыре часа... Фото стафа соответствует содержимому колб👍 . Небольшой крис выпил и попробовал курить пока ждал прилива, Стимуляция определённо есть, попробовал нюхнуть, стимуляция есть а вот с эйфой походу тяжеловато  Видимо надо больше или вв. буду сейчас питть опять. вв не умею... Благодарю. Может позже дополню, что получилось'
                        }]
                    },
                ]
            },
            {
                'name': 'A-PVP кристаллы',
                'products': [
                    {
                        'name': 'A-PVP VHQ',
                        'amounts': [{'caption': '2г | 4100₽ | Прикоп', 'price': 4100}, {'caption': '5г | 7500₽ | Тайник', 'price': 7500}, {'caption': '7г | 10700₽ | Магнит', 'price': 10700}],
                        'img': 'апвп.jpg',
                        'description': 'Максимум эффекта, эйфория и сверхтрезвость ума обеспечены. Будьте готов удивиться качеству этого простого и действенного продукта, поехали! Альфа PVP способствует выработке норадреналина и дофамина. В результате возникают крайне яркие психические реакции (необычайное чувство радости и веселья, сильное стимулирующие действие на весь организм) и незабываемые ощущения.\n\nАльфа-PVP повышает вашу физическую активность. Желание двигаться, танцевать, не стоять на месте. Сразу после употребления обостряется тактильность, зрение становится четким и острым, повышается сексуальное возбуждение и обостренная реакция на прикосновения.',
                        'reviews': [{
                            'name': 'Аноним',
                            'stars': 5,
                            'caption': 'Давно хотел мет! Соль и амф уже не те, что были несколько лет назад а амф из нулевых и начала десятых и вообще думаю сложно найти. Услышал про лёд и вот через полтора года он у меня. Взял на пробу именно этот, чтоб было с чем сравнивать потом. Клад исполнен пушка, с первого раза я и не нашёл, постоял подумал и вот они две колбы в кармане а до дома изнурительные почти четыре часа... Фото стафа соответствует содержимому колб👍 . Небольшой крис выпил и попробовал курить пока ждал прилива, Стимуляция определённо есть, попробовал нюхнуть, стимуляция есть а вот с эйфой походу тяжеловато  Видимо надо больше или вв. буду сейчас питть опять. вв не умею... Благодарю. Может позже дополню, что получилось'
                        }]
                    }
                ]
            },
            {
                'name': 'A-PVP мука',
                'products': [
                    {
                        'name': 'A-PVP VHQ+',
                        'amounts': [{'caption': '2г | 3300₽ | Магнит', 'price': 3300}, {'caption': '4г | 6500₽ | Прикоп', 'price': 6500}, {'caption': '10г | 11300₽ | Магнит', 'price': 11300}],
                        'img': 'апвп2.jpg',
                        'description': 'Максимум эффекта, эйфория и сверхтрезвость ума обеспечены. Будьте готов удивиться качеству этого простого и действенного продукта, поехали! Альфа PVP способствует выработке норадреналина и дофамина. В результате возникают крайне яркие психические реакции (необычайное чувство радости и веселья, сильное стимулирующие действие на весь организм) и незабываемые ощущения.\n\nАльфа-PVP повышает вашу физическую активность. Желание двигаться, танцевать, не стоять на месте. Сразу после употребления обостряется тактильность, зрение становится четким и острым, повышается сексуальное возбуждение и обостренная реакция на прикосновения.',
                        'reviews': [{
                            'name': 'Аноним',
                            'stars': 5,
                            'caption': 'Давно хотел мет! Соль и амф уже не те, что были несколько лет назад а амф из нулевых и начала десятых и вообще думаю сложно найти. Услышал про лёд и вот через полтора года он у меня. Взял на пробу именно этот, чтоб было с чем сравнивать потом. Клад исполнен пушка, с первого раза я и не нашёл, постоял подумал и вот они две колбы в кармане а до дома изнурительные почти четыре часа... Фото стафа соответствует содержимому колб👍 . Небольшой крис выпил и попробовал курить пока ждал прилива, Стимуляция определённо есть, попробовал нюхнуть, стимуляция есть а вот с эйфой походу тяжеловато  Видимо надо больше или вв. буду сейчас питть опять. вв не умею... Благодарю. Может позже дополню, что получилось'
                        }]
                    },
                    {
                        'name': 'Альфа пудра Cloud',
                        'amounts': [{'caption': '3г | 3900₽ | Прикоп', 'price': 3900}, {'caption': '4г | 4800₽ | Тайник', 'price': 4800}, {'caption': '8г | 8900₽ | Прикоп', 'price': 8900}],
                        'img': 'апвп3.jpg',
                        'description': 'Максимум эффекта, эйфория и сверхтрезвость ума обеспечены. Будьте готов удивиться качеству этого простого и действенного продукта, поехали! Альфа PVP способствует выработке норадреналина и дофамина. В результате возникают крайне яркие психические реакции (необычайное чувство радости и веселья, сильное стимулирующие действие на весь организм) и незабываемые ощущения.\n\nАльфа-PVP повышает вашу физическую активность. Желание двигаться, танцевать, не стоять на месте. Сразу после употребления обостряется тактильность, зрение становится четким и острым, повышается сексуальное возбуждение и обостренная реакция на прикосновения.',
                    }
                ]
            },
        ]
    },
    {
        'name': 'Психоделики',
        'subcategories': [
            {
                'name': 'Грибы ЛСД',
                'products': [
                    {
                        'name': 'Псилоцибиновые грибы Golden teacher',
                        'amounts': [{'caption': '6г | 4400₽ | Магнит', 'price': 4400}, {'caption': '7г | 4900₽ | Магнит', 'price': 4900}, {'caption': '9г | 5700₽ | Магнит', 'price': 5700}],
                        'img': 'грибы.jpg',
                        'description': ''
                    },
                    {
                        'name': 'Грибы Lizard King',
                        'amounts': [{'caption': '5г | 2400₽ | Тайник', 'price': 2400}, {'caption': '10г | 9000₽ | Магнит', 'price': 9000}],
                        'img': 'грибы2.jpg',
                        'description': ''
                    },
                    {
                        'name': 'Грибы Lipa Thai',
                        'amounts': [{'caption': '100г | 29900₽ | Прикоп', 'price': 29900}],
                        'img': 'грибы3.jpg',
                        'description': ''
                    },
                ]
            }
        ]
    },
    {
        'name': 'Эйфоретики',
        'subcategories': [
            {
                'name': 'Экстази',
                'products': [
                    {
                        'name': 'Экстази AUDI',
                        'amounts': [{'caption': '1шт | 1600₽ | Прикоп', 'price': 1600}, {'caption': '2шт | 2900₽ | Тайник', 'price': 2900}, {'caption': '6шт | 7700₽ | Прикоп', 'price': 7700}],
                        'img': 'экстазиауди.jpg',
                        'description': ''
                    },
                    {
                        'name': 'Экстази Louis Vuitton',
                        'amounts': [{'caption': '5шт | 4900₽ | Тайник', 'price': 4900}, {'caption': '7шт | 6700₽ | Магнит', 'price': 6700}],
                        'img': 'экстазилв.jpg',
                        'description': ''
                    }
                ]
            },
            {
                'name': 'MDMA',
                'products': [
                    {
                        'name': 'MDMA Нидерланды',
                        'amounts': [{'caption': '4г | 12100₽ | Тайник', 'price': 12100}, {'caption': '5г | 13900₽ | Магнит', 'price': 13900}, {'caption': '7г | 18900₽ | Магнит', 'price': 18900}],
                        'img': 'экстазилв.jpg',
                        'description': ''
                    },
                    {
                        'name': 'MDMA WHITE',
                        'amounts': [{'caption': '3г | 7900₽ | Тайник', 'price': 7900}, {'caption': '6г | 14400₽ | Прикоп', 'price': 14400}, {'caption': '9г | 19600₽ | Тайник', 'price': 19600}],
                        'img': 'мдма2.jpg',
                        'description': 'Чистые кристаллы любви без примесей и недостатков. Подарит Вам ощущение эйфории и беззаботность, желание общаться, опираясь на уверенное чувство самодостаточности уберет любую тревожность, ощущение доверия к окружающим позволит легко и свобоно формулировать ваши чувства и желания, а повышенная харизма спроецирует ваше чувство любви и эмпатии на вас самих, принося умиротворение и принятие себя и окружающих.'
                    },
                    {
                        'name': 'MDMA Кристаллы Molly VHQ',
                        'amounts': [{'caption': '1г | 3800₽ | Прикоп', 'price': 3800}, {'caption': '3г | 9600₽ | Прикоп', 'price': 9600}, {'caption': '8г | 24400₽ | Магнит', 'price': 24400}],
                        'img': 'мдма.jpg',
                        'description': 'Кристалл чудесный, волшебство в себе таит, силу эйфоретическую да любовную дарует. Хорош для утех любовных, да времени хорошего провождения в компании али без. Хорош для потех танцевальных равно как и для лежания во подушках да перинах мягких.'
                    }
                ]
            },
            {
                'name': 'Мефедрон кристаллы',
                'products': [
                    {
                        'name': 'Мефедрон PREMIUM',
                        'amounts': [{'caption': '4г | 5400₽ | Тайник', 'price': 5400}, {'caption': '7г | 8100₽ | Прикоп', 'price': 8100}, {'caption': '10г | 11300₽ | Тайник', 'price': 11300}]
                    },
                    {
                        'name': 'Мефедрон кристаллы VHQ',
                        'amounts': [{'caption': '2г | 3900₽ | Тайник', 'price': 3900}, {'caption': '5г | 8000₽ | Прикоп', 'price': 8000}, {'caption': '9г | 11600₽ | Магнит', 'price': 11600}]
                    }
                ]
            },
            {
                'name': 'Мефедрон мука',
                'products': [
                    {
                        'name': 'Мефедрон мука VHQ',
                        'amounts': [{'caption': '1г | 1400₽ | Прикоп', 'price': 1400}, {'caption': '2г | 2500₽ | Прикоп', 'price': 2500}, {'caption': '10г | 10200₽ | Тайник', 'price': 10200}]
                    },
                    {
                        'name': 'Мефедрон мука VIP VHQ',
                        'amounts': [{'caption': '3г | 4500₽ | Тайник', 'price': 4500}, {'caption': '8г | 8900₽ | Магнит', 'price': 8900}, {'caption': '10г | 10500₽ | Магнит', 'price': 10500}]
                    }
                ]
            },
        ]
    },
     {
                'name': 'Марихуана',
                'subcategories': [
                    {
                        'name': 'Гашиш',
                        'products': [
                        {
                            'name': 'Гашиш ICE-O-LATOR ORANGE',
                            'amounts': [{'caption': '1г | 2100₽ | Тайник', 'price': 2100}, {'caption': '2г | 3500₽ | Прикоп', 'price': 3500}, {'caption': '8г | 9800₽ | Тайник', 'price': 9800}]
                        },
                        {
                            'name': 'Гашиш ICE-O-LATOR Gorilla Glue',
                            'amounts': [{'caption': '3г | 3800₽ | Магнит', 'price': 3800}, {'caption': '6г | 6900₽ | Магнит', 'price': 6900}]
                        },
                        {
                            'name': 'HASH Bolivia',
                            'amounts': [{'caption': '1г | 1800₽ | Прикоп', 'price': 1800}, {'caption': '2г | 3200₽ | Прикоп', 'price': 3200}, {'caption': '10г | 11200₽ | Прикоп', 'price': 11200}]
                        },
                    ]
                    },
                    {
                        'name': 'Шишки',
                        'products': [
                        {
                            'name': 'Шишки White Widow',
                            'amounts': [{'caption': '1г | 2100₽ | Тайник', 'price': 2100}, {'caption': '4г | 7600₽ | Прикоп', 'price': 7600}, {'caption': '7г | 12100₽ | Тайник', 'price': 12100}]
                        },
                        {
                            'name': 'Бошечки АК-47',
                            'amounts': [{'caption': '4г | 7200₽ | Магнит', 'price': 7200}, {'caption': '6г | 9900₽ | Тайник', 'price': 9900}, {'caption': '10г | 17500₽ | Магнит', 'price': 17500}]
                        },
                        {
                            'name': 'Шишки Mimosa Evo +',
                            'amounts': [{'caption': '3г | 5300₽ | Прикоп', 'price': 5300}, {'caption': '6г | 10500₽ | Тайник', 'price': 10500}, {'caption': '8г | 13900₽ | Магнит', 'price': 13900}]
                        },
                    ]
                    },
                    {
                        'name': 'План',
                        'products': [
                        {
                            'name': 'Трим Blue Sunset Sherbert',
                            'amounts': [{'caption': '2г | 1200₽ | Прикоп', 'price': 1200}, {'caption': '5г | 4400₽ | Прикоп', 'price': 4400}, {'caption': '9г | 7700₽ | Магнит', 'price': 7700}]
                        },
                        {
                            'name': 'Трим Caramelo',
                            'amounts': [{'caption': '1г | 850₽ | Тайник', 'price': 850}, {'caption': '3г | 2500₽ | Тайник', 'price': 2500}, {'caption': '7г | 5800₽ | Прикоп', 'price': 5800}]
                        }
                    ]
                    },
                ]
            },
]

# FSM для каталога и корзины
user_catalog_state = {}
user_cart = {}
# Переменная состояния для ввода адреса
user_states = {}

# --- Каталог: корень ---
def get_category_markup(path):
    markup = types.InlineKeyboardMarkup(row_width=1)
    node = get_catalog_node(path)
    # Категории, подкатегории, товары
    if 'subcategories' in node:
        for i, subcat in enumerate(node['subcategories']):
            markup.add(types.InlineKeyboardButton(subcat['name'], callback_data=f'cat:{path_str(path+["subcategories",i])}'))
    if 'products' in node:
        for i, prod in enumerate(node['products']):
            markup.add(types.InlineKeyboardButton(f"{prod['name']}", callback_data=f'prod:{path_str(path+["products",i])}'))
    if not ('subcategories' in node or 'products' in node):
        for i, cat in enumerate(CATALOG_TREE):
            markup.add(types.InlineKeyboardButton(cat['name'], callback_data=f'cat:{i}'))
    # Кнопка назад
    if path:
        markup.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'back:{path_str(path)}'))
    return markup

def get_catalog_node(path):
    node = {'subcategories': CATALOG_TREE}
    for p in path:
        if isinstance(p, str) and p == 'subcategories':
            node = node['subcategories']
        elif isinstance(p, str) and p == 'products':
            node = node['products']
        else:
            node = node[p]
    return node

def path_str(path):
    return ','.join(str(x) for x in path)

def path_from_str(s):
    if not s:
        return []
    return [int(x) if x.isdigit() else x for x in s.split(',')]

@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()
    user_id = str(message.from_user.id)
    username = message.from_user.first_name
    referrer_id = None
    if len(args) > 1:
        referrer_id = args[1]
    is_new_user = user_id not in user_referrers
    # Если пользователь новый и есть реферер, записываем
    if is_new_user and referrer_id and referrer_id != user_id:
        user_referrers[user_id] = referrer_id
        # Добавляем к рефералам
        user_referrals.setdefault(referrer_id, []).append(user_id)
        # Уведомляем владельца ссылки
        try:
            bot.send_message(referrer_id, f'У вас новый реферал: {username} (id: {user_id})!')
        except Exception:
            pass
    elif not is_new_user and referrer_id and referrer_id != user_id:
        # Если пользователь уже был
        try:
            bot.send_message(user_id, 'Вы уже зарегистрированы в боте!')
            bot.send_message(referrer_id, f'Пользователь {username} (id: {user_id}) уже был зарегистрирован ранее!')
        except Exception:
            pass
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Выбрать город', callback_data='choose_city:0')
    markup.add(btn)
    with open('welcome.png', 'rb') as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption=f'Привет, {username}! Добро пожаловать!\nПожалуйста, выберите город.',
            reply_markup=markup
        )

def get_cities_markup(page=0):
    markup = types.InlineKeyboardMarkup(row_width=2)
    start = page * CITIES_PER_PAGE
    end = start + CITIES_PER_PAGE
    cities = CITIES[start:end]
    for i in range(0, len(cities), 2):
        row = []
        for j in range(2):
            if i + j < len(cities):
                city = cities[i + j]
                row.append(types.InlineKeyboardButton(f"{city['country']} {city['name']}", callback_data=f"city_{city['name']}"))
        markup.row(*row)
    nav_buttons = []
    if page > 0:
        nav_buttons.append(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'choose_city:{page-1}'))
    if end < len(CITIES):
        nav_buttons.append(types.InlineKeyboardButton('Вперед ➡️', callback_data=f'choose_city:{page+1}'))
    if nav_buttons:
        markup.row(*nav_buttons)
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith('choose_city'))
def choose_city(call):
    page = 0
    if ':' in call.data:
        try:
            page = int(call.data.split(':')[1])
        except:
            page = 0
    bot.answer_callback_query(call.id)
    # Пытаемся изменить только кнопки, если сообщение текстовое
    try:
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=get_cities_markup(page)
        )
    except Exception:
        # Если не получилось (например, сообщение не текстовое), удаляем старое и отправляем новое
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        bot.send_message(
            call.message.chat.id,
            'Выберите город:',
            reply_markup=get_cities_markup(page)
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('city_'))
def city_selected(call):
    city_name = call.data[5:]
    bot.answer_callback_query(call.id, text=f'Вы выбрали: {city_name}')
    # Сначала отправляем сообщение об успешном выборе города с меню
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row('👤 Профиль', '👥 Рефералы')
    menu.row('💬 Связь', '🔄 Поменять город')
    menu.row('🛒 Каталог')
    bot.send_message(call.message.chat.id, f'Город {city_name} успешно выбран!', reply_markup=menu)
    # Затем отправляем фото каталога с подписью и инлайн-кнопками
    catalogue_root(call.message)

@bot.message_handler(commands=['catalogue'])
@bot.message_handler(func=lambda message: message.text == '🛒 Каталог')
def catalogue_root(message):
    user_catalog_state[message.from_user.id] = []
    markup = get_category_markup([])
    with open('catalogue.png', 'rb') as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption='Выберите категорию:',
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('cat:'))
def catalogue_category(call):
    path = path_from_str(call.data[4:])
    user_catalog_state[call.from_user.id] = path
    markup = get_category_markup(path)
    # Update caption based on level: root shows prompt, deeper shows category name
    caption_text = 'Выберите категорию:' if not path else get_catalog_node(path).get('name', 'Выберите категорию:')
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=caption_text,
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('back:'))
def catalogue_back(call):
    path = path_from_str(call.data[5:])
    # Determine new path: root clears, else go up one level
    if not path:
        new_path = []
    else:
        new_path = path[:-2] if isinstance(path[-2], str) else path[:-1]
    user_catalog_state[call.from_user.id] = new_path
    markup = get_category_markup(new_path)
    # Always reset caption to selection prompt
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption='Выберите категорию:',
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('prod:'))
def catalogue_product(call):
    path = path_from_str(call.data[5:])
    node = get_catalog_node(path)
    # Формируем caption с описанием
    caption = f"{node['name']}\n\nОписание: {node.get('description', '')}"
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i, amount in enumerate(node['amounts']):
        markup.add(types.InlineKeyboardButton(amount['caption'], callback_data=f'amount2:{path_str(path)}:{i}'))
    markup.add(
        types.InlineKeyboardButton('Показать фото', callback_data=f'prod_photo:{path_str(path)}'),
        types.InlineKeyboardButton('Показать отзывы', callback_data=f'prod_reviews:{path_str(path)}')
    )
    markup.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'back:{path_str(path[:-2])}'))
    # Меняем caption и кнопки у сообщения с фото
    try:
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=caption,
            reply_markup=markup
        )
    except Exception:
        # fallback: только кнопки
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('prod_photo:'))
def catalogue_product_photo(call):
    path = path_from_str(call.data.split(':', 1)[1])
    node = get_catalog_node(path)
    img = node.get('img')
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'prod_back:{path_str(path)}'))
    if img:
        img_path = f"img/{img}"
        with open(img_path, 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=node.get('name', ''), reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, 'Фото не найдено.', reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('prod_reviews:'))
def catalogue_product_reviews(call):
    path = path_from_str(call.data.split(':', 1)[1])
    node = get_catalog_node(path)
    reviews = node.get('reviews', [])
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'prod_back:{path_str(path)}'))
    if not reviews:
        bot.send_message(call.message.chat.id, 'Отзывов пока нет.', reply_markup=markup)
        bot.answer_callback_query(call.id)
        return
    text = 'Отзывы:\n\n'
    for review in reviews:
        name = review.get('name', '-')
        stars = int(review.get('stars', 0))
        stars_str = '⭐' * stars
        caption = review.get('caption', '-')
        text += f"<b>{name} {stars_str}</b>\n<blockquote>{caption}</blockquote>\n\n"
    bot.send_message(call.message.chat.id, text, parse_mode='HTML', reply_markup=markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('prod_back:'))
def catalogue_product_back(call):
    path = path_from_str(call.data.split(':', 1)[1])
    node = get_catalog_node(path)
    caption = f"{node['name']}\n\nОписание: {node.get('description', '')}"
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i, amount in enumerate(node['amounts']):
        markup.add(types.InlineKeyboardButton(amount['caption'], callback_data=f'amount2:{path_str(path)}:{i}'))
    markup.add(
        types.InlineKeyboardButton('Показать фото', callback_data=f'prod_photo:{path_str(path)}'),
        types.InlineKeyboardButton('Показать отзывы', callback_data=f'prod_reviews:{path_str(path)}')
    )
    markup.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'back:{path_str(path[:-2])}'))
    try:
        bot.send_photo(
            call.message.chat.id,
            open(node.get('img', 'catalogue.png'), 'rb'),
            caption=caption,
            reply_markup=markup
        )
    except Exception:
        bot.send_message(
            call.message.chat.id,
            caption,
            reply_markup=markup
        )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('amount2:'))
def catalogue_amount2(call):
    _, path_str_val, idx = call.data.split(':', 2)
    path = path_from_str(path_str_val)
    node = get_catalog_node(path)
    amount = node['amounts'][int(idx)]
    user_id = call.from_user.id
    # Добавляем в корзину
    user_cart.setdefault(user_id, []).append({
        'name': node['name'],
        'amount': amount['caption'],
        'price': amount['price'],
    })
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('➕ Добавить ещё', callback_data='add_more'),
        types.InlineKeyboardButton('🛒 Посмотреть корзину', callback_data='show_cart'),
        types.InlineKeyboardButton('❌ Отменить', callback_data='cancel_cart'),
        types.InlineKeyboardButton('✅ Заказать', callback_data='checkout')
    )
    text_to_send = f'Товар "{node["name"]}" в варианте "{amount["caption"]}" добавлен в корзину.'
    safe_edit_message_text(bot, call.message.chat.id, call.message.message_id, text_to_send, markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'add_more')
def add_more_to_cart(call):
    # Возврат к корню каталога
    user_catalog_state[call.from_user.id] = []
    markup = get_category_markup([])
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'show_cart')
def show_cart(call):
    user_id = call.from_user.id
    cart = user_cart.get(user_id, [])
    if not cart:
        text = 'Ваша корзина пуста.'
    else:
        text = 'Ваша корзина:\n'
        total = 0
        refs = user_referrals.get(str(user_id), [])
        has_discount = len(refs) > 0
        for item in cart:
            price = item['price'] // 2 if has_discount else item['price']
            text += f"{item['name']} x {item['amount']} — {price}₽\n"
            total += price
        if has_discount:
            text += f'\n🎉 У вас скидка 50% на все товары!'
        text += f'\nИтого: {total}₽'
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('Оформить', callback_data='checkout'),
        types.InlineKeyboardButton('⬅️ Назад', callback_data='add_more'),
        types.InlineKeyboardButton('❌ Отменить', callback_data='cancel_cart')
    )
    safe_edit_message_text(bot, call.message.chat.id, call.message.message_id, text, markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'cancel_cart')
def cancel_cart(call):
    user_cart[call.from_user.id] = []
    safe_edit_message_text(bot, call.message.chat.id, call.message.message_id, 'Корзина очищена.', None)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'checkout')
def checkout_cart(call):
    user_id = call.from_user.id
    user_catalog_state[user_id] = []
    markup = types.ForceReply()
    bot.send_message(chat_id=call.message.chat.id, text='Пожалуйста, напишите сообщением более точный ориентир или адрес в вашем городе для доставки (район, метро, улица):', reply_markup=markup)
    user_states[user_id] = 'awaiting_address'
    bot.answer_callback_query(call.id)
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'awaiting_address')
def process_address(message):
    user_id = message.from_user.id
    address = message.text
    cart = user_cart.get(user_id, [])
    refs = user_referrals.get(str(user_id), [])
    has_discount = len(refs) > 0
    total = 0
    text = 'Ваш заказ:\n'
    for item in cart:
        price = item['price'] // 2 if has_discount else item['price']
        text += f"{item['name']} x {item['amount']} — {price}₽\n"
        total += price
    user_orders[user_id] = total
    # Отправляем пользователю итог заказа и кнопки оплаты
    if has_discount:
        text += f'\n🎉 У вас скидка 50% на все товары!'
    text += f'\nИтого: {total}₽\n\nАдрес доставки: {address}\n\nВыберите способ оплаты:'
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('Крипта', callback_data='pay_crypto'),
        types.InlineKeyboardButton('Картой', callback_data='pay_card')
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)
    user_states.pop(user_id, None)
# --- Crypto payment handlers ---
@bot.callback_query_handler(func=lambda call: call.data == 'pay_crypto')
def choose_crypto(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    for symbol in CRYPTO_CURRENCIES:
        markup.add(types.InlineKeyboardButton(symbol, callback_data=f'crypto:{symbol}'))
    bot.send_message(call.message.chat.id, 'Выберите валюту для оплаты', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('crypto:'))
def process_crypto(call):
    user_id = call.from_user.id
    parts = call.data.split(':', 1)
    symbol = parts[1]
    total = user_orders.get(user_id)
    if total is None:
        bot.answer_callback_query(call.id, 'Нет данных о заказе', show_alert=True)
        return
    coin_id = CRYPTO_IDS.get(symbol)
    try:
        resp = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=rub')
        resp.raise_for_status()
        price = resp.json()[coin_id]['rub']
        amount = round(total / price, 7)
    except Exception:
        bot.answer_callback_query(call.id, 'Ошибка получения курса', show_alert=True)
        return
    address = CRYPTO_ADDRESSES.get(symbol)
    text = f'Отправьте ровно указанное количество на указанный кошелёк. Кол-во и адрес можно скопировать. \n\nКоличество: `{amount}` {symbol}\nАдрес: `{address}`'
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='MARKDOWN')
    except Exception as e:
        print(f'Ошибка при изменении сообщения: {e}')
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'pay')
def choose_payment_method(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('Крипта', callback_data='pay_crypto'),
        types.InlineKeyboardButton('Картой', callback_data='pay_card')
    )
# Secret command to set card number
@bot.message_handler(commands=['card'])
def cmd_card(message):
    if message.from_user.id != ADMIN_ID:
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, 'Укажи номер карты: /card <номер>')
        return
    number = parts[1].strip()
    set_card_number(number)
    bot.send_message(message.chat.id, f'Номер карты установлен: {number}')

# Handler for card payment selection
@bot.callback_query_handler(func=lambda call: call.data == 'pay_card')
def pay_with_card(call):
    user_id = call.from_user.id
    amount = sum(item['price'] for item in user_cart.get(user_id, []))
    card = get_card_number()
    if not card:
        bot.send_message(call.message.chat.id, "Номер карты не задан. Обратитесь к администратору.")
    else:
        bot.send_message(call.message.chat.id, f"Чек на оплату\n\n💰 Сумма: {amount}₽ \n💳 Карта: `{card}`", parse_mode='MARKDOWN')
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 'Выберите способ оплаты', reply_markup=markup)
    bot.answer_callback_query(call.id)
@bot.message_handler(commands=['profile'])
@bot.message_handler(func=lambda message: message.text == '👤 Профиль')
def profile_page(message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    refs = user_referrals.get(str(user_id), [])
    ref_count = len(refs)
    bot_username = bot.get_me().username
    ref_link = f'https://t.me/{bot_username}?start={user_id}'
    with open('profile.png', 'rb') as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption=f'👤 Профиль: {username}\n\n👥 Рефералов: {ref_count}\n🔗 Реферальная ссылка (скопируйте):\n{ref_link}'
        )

# Удаляю обработчик, который перехватывает все сообщения и мешает работе других кнопок
# @bot.message_handler(func=lambda message: True)
# def show_menu_keyboard(message):
#     menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     menu.row('👤 Профиль', '👥 Рефералы')
#     menu.row('💬 Связь', '🔄 Поменять город')
#     menu.row('🛒 Каталог')
#     bot.send_chat_action(message.chat.id, 'typing')
#     bot.reply_to(message, ' ', reply_markup=menu)

# Рефералы (👥 Рефералы)
@bot.message_handler(commands=['ref'])
@bot.message_handler(func=lambda message: message.text == '👥 Рефералы')
def referrals_page(message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    refs = user_referrals.get(str(user_id), [])
    ref_count = len(refs)
    bot_username = bot.get_me().username
    ref_link = f'https://t.me/{bot_username}?start={user_id}'
    with open('ref.png', 'rb') as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption=f'Реферальная программа\n\n👥 Ваши рефералы: {ref_count}\n🔗 Ваша реферальная ссылка: {ref_link}\n\n⚠️ Скопируйте и отправьте своим друзьям ссылку сверху. Каждый новый приведённый вами друг, будет засчитан как реферал. При получении 3 рефералов, вы получаете скидку 50% на все товары!'
        )

# Связь (💬 Связь)
user_orders = {}

@bot.message_handler(commands=['contact'])
@bot.message_handler(func=lambda message: message.text == '💬 Связь')
def contact_start(message):
    user_states[message.from_user.id] = 'awaiting_contact_message'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('❌ Отменить')
    bot.send_message(
        message.chat.id,
        'Напишите ваше сообщение для менеджера. После отправки оно будет доставлено. Для отмены нажмите "❌ Отменить".',
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'awaiting_contact_message')
def contact_process(message):
    if message.text == '❌ Отменить':
        user_states.pop(message.from_user.id, None)
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        menu.row('👤 Профиль', '👥 Рефералы')
        menu.row('💬 Связь', '🔄 Поменять город')
        menu.row('🛒 Каталог')
        bot.send_message(message.chat.id, 'Отправка сообщения отменена.', reply_markup=menu)
        return
    # Отправляем сообщение менеджеру
    manager_id = 5864245473
    try:
        bot.send_message(manager_id, f'Новое сообщение от пользователя {message.from_user.first_name} (id: {message.from_user.id}):\n{message.text}')
    except Exception:
        pass
    user_states.pop(message.from_user.id, None)
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row('👤 Профиль', '👥 Рефералы')
    menu.row('💬 Связь', '🔄 Поменять город')
    menu.row('🛒 Каталог')
    bot.send_message(message.chat.id, 'Ваше сообщение успешно доставлено менеджеру!', reply_markup=menu)

# Поменять город (🔄 Поменять город)
@bot.message_handler(commands=['city'])
@bot.message_handler(func=lambda message: message.text == '🔄 Поменять город')
def change_city(message):
    bot.send_message(
        message.chat.id,
        'Выберите город:',
        reply_markup=get_cities_markup(0)
    )

def safe_edit_message_text(bot, chat_id, message_id, text, reply_markup=None):
    try:
        if text:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=reply_markup
            )
            return
    except Exception:
        pass  # Просто игнорируем ошибку
    if text:
        bot.send_message(chat_id, text, reply_markup=reply_markup)

if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling() 