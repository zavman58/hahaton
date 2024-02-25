import pandas as pd
import json
import pickle
import datetime

categories = {'food': ['AGAMA', 'Delivery Club', 'Elementaree', 'GLOBUS', 'Greenbox Рационы', 'Grow Food', 'Growfood', 'JustFood', 'My Food', 'SPAR', 'Vprok.ru Перекрёсток', 'Wow Food', 'YAMDIET', 'Yamdiet', 'pobo', 'Ашан', 'Бахетле', 'Веселый Водовоз', 'ВкусВилл', 'ВкусВилл Готовит', 'ВкусВилл в Тинькофф', 'ВкусМил', 'ВкусМил от ВкусВилл', 'ВкусМилл от ВкусВилл', 'ВкусНаДом', 'Вкусвилл', 'Все в разделе «ВкусВилл»', 'Гипермаркет Карусель', 'Дикси', 'Доставка питания YAMDIET', 'Доставка питания Yamdiet', 'ЛЕНТА', 'ЛЕНТА Онлайн', 'Лавка Edoque', 'Лента', 'Лента Онлайн', 'Магнит', 'Магнолия', 'Мегамаркет', 'Михайлик Kitchen', 'О’КЕЙ', 'Пан Запекан', 'Перекрёсток', 'Петрович', 'Порядок', 'Порядок.ру', 'Правильная корзинка', 'ПриЕм!', 'Программы питания Level Kitchen', 'Пятёрочка', 'Сhef At Home', 'Самокат', 'Сахар', 'Сеть магазинов «Пятёрочка»', 'Слата', 'Ужин Дома', 'Шефмаркет', 'Яндекс Еда', 'Яндекс Лавка', 'Яндекс.Еда', 'Яндекс.Еда и Лавка', 'Яндекс.Лавка', 'Ярче', 'Ярче!', 'интернет-магазин GLOBUS', 'интернет-магазин ВкусВилл'],
              'education': ['Advance', 'GoPractice Growth', 'LingvaBOOM', 'MyFitlab', 'Puzzle English', 'SKYENG', 'School of Practical Investment', 'Skyeng', 'Skyeng Math', 'Skyeng Премиум', 'Skypro', 'Skysmart', 'Skysmart Premium', 'Smart Reading', 'SmartReading', 'Smartreading', 'Storytel', 'X10 Academy', 'Аудиомания', 'Аудиомания.ру', 'Для студентов ВШЭ', 'Для студентов МГТУ им. Баумана', 'Для студентов МГУ', 'Для студентов НИУ ВШЭ СПб', 'Интернет-магазин «Читай-город»', 'Интернет-магазин Читай-город', 'Испаника', 'Нетология', 'Онлайн школа  LingvaBOOM', 'Онлайн школа Испаника', 'Парусная Академия', 'Республика', 'Сотка', 'Тетрика', 'Умскул', 'Учи.ру', 'Фоксфорд', 'Читай город', 'Читай-город', 'Школа идеального тела'],
              'medicine': ['ADRIA', 'Alter', 'Aravia', 'Armani beauty', 'Delux thai spa', 'Diamarka', 'Doma Beauty Place', 'Elemis', 'Erborian', 'KIKO MILANO', 'KRASOTKAPRO.RU', 'Kiko Milano', 'LETIQUE', 'Lancome.ru', 'Los Brows', 'MIXIT', 'Medalp', 'Noerden', 'Pharmacosmetica', 'SEPHORA', 'Sisley-Paris', 'SmartMed', 'Socolor', 'Soda', 'Well Clinic', 'Yahmur Space', 'Yves Rocher', 'biblioteka aromatov', 'imkosmetik', 'Акушерство.ru', 'Аптека Вита', 'Аптека Низких Цен', 'Библиотека ароматов', 'Галерея косметики', 'Горздрав', 'Государственная Аптека', 'Дентал Бутик', 'ДиаМарка', 'ЕМС', 'Европейский Медицинский Центр', 'ЗдравСити', 'Интернет-бутик «YVES ROCHER»', 'Интернет-магазин Акушерство.ру', 'КрасоткаПро', 'Красоткапро', "Л'Этуаль", 'Лаборатория ДНКОМ', 'Линзмастер', 'Лошадиная Сила', 'Лошадиная сила', 'МЕДСИ', 'МЕДСИ сеть клиник', 'Магнит косметик', 'Медси', 'Миссис Лазер', 'Моя аптека', 'Народная стоматология', 'ОРТЕКА', 'Оазис-спа', 'Огни Олимпа', 'Оптика Точка зрения', 'Ортека', 'Офтальмологическая клиника Спектр', 'Планета Здоровья', 'Сеть аптек «Моя аптека»', 'Сеть аптек Моя аптека', 'Сиблабсервис', 'Телемедицина от МЕДСИ', 'Телемедицина от МЕДСИ ', 'Точка зрения', 'УЗИ студия', 'Улыбка радуги', 'ЦЭЛТ', 'Четыре глаза', 'интернет-бутик Yves Rocher', 'интернет-бутик «YVES ROCHER»'],
              'travel': ['4SEASONS', 'Art Deco Primorsky', 'Art Nuvo Palace', 'Bronevik', 'Bronevik.com', 'Delta Sirius', 'FUN&SUN', 'Grand Wellness', 'Level Travel', 'Level.Travel', 'Level.Travel Туры', 'METRO Cash&Carry', 'Ostrovok.ru', 'QuickMADE', 'S7', 'S7 Airlines', 'SHELL', 'Shell', 'TUI', 'TUI I FUN&SUN', 'Tvil.ru', 'UBER', 'Uber Russia', 'Urent', 'Whoosh', 'tutu Отели', 'Автотека', 'Аква-Вита', 'Аква-Стайл', 'Бизнес-залы РЖД', 'ВелоСклад', 'Делимобиль', 'Купибилет', 'Лукойл', 'Манжерок', 'Манжерок ', 'Петровский Арт Лофт', 'РАМК', 'Русский Авто-Мото Клуб', 'Русский АвтоМотоКлуб (РАМК)', 'СИТИДРАЙВ', 'СЛЕТАТЬ.РУ', 'Сеть автомоек 4SEASONS', 'Ситидрайв', 'Ситимобил', 'Слетать.Ру', 'Спутник', 'Суточно.ру', 'ТВИЛ', 'Такси Maxim', 'Тинькофф Отели', 'Туту Отели', 'Экспресс Точка Ру', 'Юрент', 'Яндекс Такси', 'Яндекс.Такси'],
              'purchase': ['#SEKTA', '1С Интерес', '2MOOD', '585 Золотой', '585*Золотой', 'ATAK', 'AliExpress', 'AllTime', 'AllTime.ru', 'Bluesleep', 'Bonafide', 'Bonafide ', 'CERAMISU', 'COLINS', 'Cheese It', 'Code4game', 'Consul', 'Cеть хобби-гипермаркетов «Леонардо»', 'DKNY', 'Designboom', 'Dr.Head', 'ESET NOD32', 'ESETNOD32', 'Etam', 'FARFETCH', 'Familia', 'Farfetch', 'Fissman', 'Fix Price', 'FloraExpress', 'Futuriqa', 'GFN', 'GRASS', 'Giox', 'Goods', 'Goods.ru', 'Grass', 'Gulliver market', 'HANDWERS', 'Handwers', 'Happywear', 'I am studio', 'ISTNOVA', 'IVI', 'IVI в приложении Тинькофф', 'IVI от Тинькофф', 'Intelinvest', 'Intelinvest ', 'Juicy Couture', 'KANZLER', 'KARI', 'KARI KIDS', 'Kanzler', 'Karcher', 'Kari', 'Kidzania', 'Kraft Flowers', 'Lamoda', 'Lassie', 'Lee', 'MATE flowers', 'MEGOGO', 'MIUZ Diamonds', 'Marc & Andre', 'Marks & Spencer', 'Masar Lingerie', 'Megogo', 'Mon Bon', 'Movavi', 'My Hygge Box', 'NEBBIA', 'Nappyclub', 'OZON', 'OZON.ru', 'Olympus', 'Ozon', 'Ozon.ru', 'PETKIT', 'PREMIER', 'PRO.FINANSY', 'Petshop.ru', 'Petstory', 'Petstory ', 'Reima', 'Respect', 'Rondell', 'Routemark', 'SENAT', 'SOLAR', 'SUPERPET', 'Samsung', 'Seiko Club', 'Shopping live', 'Simple', 'Softline Store', 'SuperStep', 'Svetlov', 'TEZENIS', 'Teboil', 'Tkano', 'VK Музыка', 'Wink', 'World of watch', 'Yves Saint Laurent', 'Zolla', 'adidas', 'e2e4', 'goods.ru', 'ivi', 'kari', 'kari KIDS', 'more.tv', '«Лаборатория Касперского»', 'Аленка', 'Арбатский БаЗар', 'Бетховен', 'Братья Чистовы', 'Бронницкий ювелир', 'Верный', 'Ветеринария онлайн Petstory', 'Ветеринарный центр', 'Газпромнефть', 'Горбилет', 'Деловые Линии', 'Детский Мир', 'Динозаврик', 'Доставка цветов FloraExpress', 'Зелёная лиса', 'Золотое Яблоко', 'Зоомагазин Динозаврик', 'ИВИ', 'Иви в приложении Тинькофф', 'Игры в Тинькофф Городе', 'Интернет - магазин SEPHORA', 'Интернет-магазин 585*Золотой', 'Интернет-магазин Lancome.ru', 'Интернет-магазин SuperStep', 'Интернет-магазин TEZENIS', 'Интернет-магазин «Технопарк»', 'Интернет-магазин Динозаврик', 'Интернет-магазин Технопарк', 'КОД4ГЕЙМ', 'Карат', 'Каток на Кремлёвской набережной', 'Кидзания', 'Кораблик', "Л'Окситан", 'Лаборатория Касперского', 'Леонардо', 'Логомашина', 'МегаФон', 'Мираторг', 'Мокрый нос', 'Монетка', 'Московский ювелирный завод', 'Николаевский', 'Опека', 'ПЕРЕСТРОЙКА', 'Плюс Мульти', 'Полимакс', 'РИВ ГОШ', 'Рив Гош', 'Роснефть', 'Ростелеком', 'Русский остров', 'СЕТЬ СВЯЗНОЙ', 'СТРОЙПЛАТФОРМА', 'СберМаркет', 'СберМегаМаркет', 'Связной', 'Спектр', 'Столото', 'Строительный двор', 'Строительный двор Рассрочка', 'Строительный двор Таргет', 'ТВОЕ', 'Татнефть', 'Технопарк', 'Тинькофф Игры', 'Тинькофф Страхование', 'Тинькофф каток', 'Топливо в Тинькофф', 'Топливо в Тинькофф (FUEL)', 'Тортомастер', 'Точка любви', 'Хобби-гипермаркет Леонардо', 'Хобби-гипермаркеты «Леонардо»', 'Хобби-гипермаркеты Леонардо', 'ЦВЕТЫ НА РАЙОНЕ', 'ЦСКА', 'Цветов.ру', 'Цветы на районе', 'ЧЕТЫРЕ ГЛАЗА', 'Четыре Лапы', 'Чистая линия', 'Чёрное Озеро', 'Яндекс 360', 'Яндекс Заправки', 'Яндекс Плюс', 'Яндекс.Заправки', 'Яркий Фотомаркет', 'Яркий фотомаркет', 'интернет-магазин SuperStep', 'интернет-магазин TEZENIS', 'интернет-магазин Технопарк'],
              'restaurant': ['BB&BURGERS', 'BURGER KING', 'Burger King', 'Cofix', "Domino's Pizza", 'Four', 'Gent', 'KFC', 'Maestrello', 'PIZZASUSHIWOK.RU', 'PhoBo', 'Pizza Maestrello', 'PizzaSushiWok', 'PrimeMeat', 'PrimeMeat.ru', 'Tasty Coffee', 'Бирвайн', 'Бургер Кинг', 'ВьетКафе', 'Гурманика', 'ДОДО Пицца', 'Додо', 'Додо Пицца', 'Кухня на районе', 'НИЯМА', 'Рестораны', 'Сушкоф и Дель Песто', 'Сушкоф и пицца', 'Теремок', 'Теремок ', 'Теремок Спб'],
              'bigpurchase': ['AUTODOC.RU', 'Anytime Prime', 'Braun', 'DNS', 'Don Plafon', 'Fandeco', 'Garlyn', 'Greenbox', 'HOBOT', 'HOFF', 'Haier', 'Inoxtime', 'LAZURIT', 'Lapsi', 'Lavita', 'Leran', 'Level Kitchen', 'Lustron', 'Lustron.ru', 'MELEON', 'Maxwell', 'Pushe', 'SantPrice.ru', 'TESSER', 'TESSER.RU', 'Xcom-shop', 're:Store', 'restore:', 'Гардиан', 'Двери ГАРДИАН', 'Двери Гардиан', 'Дивайн Лайт', 'ЛЮ.ру', 'Леруа Мерлен', 'М.Видео', 'Маркет света', 'Сантехника-Рум', 'Ситилинк', 'Фиссмания', 'Холодильник.ру', 'Эльдорадо']}

def get_predict(name, budget, id):
    date_end = pd.to_datetime('2023-02-28')
    
    with open('predictions.json', 'r') as json_file:
        json_data = json.load(json_file)

    category = None
  
    for key_cat, val_cat in categories.items():
        if name in val_cat:
            category = key_cat
          
    assert category is not None, "Не нашлась категория..."
        
    full_df = {name: date_end}

    name_model = f'fit-model/model_fit_{category}.pkl'
    with open(name_model, 'rb') as pkl:
        model = pickle.load(pkl)

    periods = (date_end - pd.to_datetime('2023-01-01')).days
    predict = model.predict(n_periods=periods)

    dates = pd.date_range(pd.to_datetime('2023-01-01'), date_end)
    predict = predict.to_frame(name='pred_cash')
    df_pred = pd.concat([dates, predict], axis=1)
    
    sum_cash = 0
    for i in range(df_pred.shape[0]):
        sum_cash += df_pred.iloc[i, -1] 
        if sum_cash >= budget:
            plan_time = pd.to_datetime(full_df[name])
            now_time = pd.to_datetime(df_pred.iloc[i, 0])
            if plan_time > now_time:
                full_df[name] = f'{now_time.year}-{now_time.month}-{now_time.day}'
            else:
                full_df[name] = f'{plan_time.year}-{plan_time.month}-{plan_time.day}'
    
    json_data[str(id)] = full_df[name]
    with open('predictions.json', 'w') as f:    
        json.dump(json_data, f)
