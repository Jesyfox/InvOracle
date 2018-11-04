HEADERS = {
    'MTS':'mts',
    'SKU':'sku',
    'Активный':'active',
    'Название':'name',
    'Склад':'warehouse',
    'Поставщик':'suplayer',
    'MOQ':'moq',
    'Буфер':'bufer',
    'Остаток':'leftover',
    'Название ассортиментной матрицы':'matrix',
    'ОБ показатель':'ob_index',
    'В пути':'on_the_way',
    'ОПБ показатель':'opb_index',
    'Дата следующего заказа':'next_order',
    'ADU':'adu',
    'Дата буфера':'bufer_date',
    'Movers':'movers',
    'ББ-2 Дополнительное оборудование':'bb_2',
    'ББ-3 Паллета':'bb_3',
    'ББ-4 Акционный запас на 2-3 недели':'bb_4',
    'Буфер безопасности':'bb',
    'Признак разделения':'splt_grp',
    'Группа номенклатуры 1':'nomenclature_1',
    'Код склада':'warehouse_code',
    'Код поставщика':'supler_code',
    'Автоотправка':'autosend',
    'Вес':'weight',
    'USQ':'usq',
    'Цена закупки':'buy',
    'Цена продажи':'sell',
    'Ед.измерения':'measure_unit',
    'Количество к заказу':'order_amount',
    'Буфер безопасности в днях продаж':'bb_in_days',
    'Группа номенклатуры 2':'nomenclature_2',
    'Группа номенклатуры 3':'nomenclature_3',
    'Период':'periode',
    'Мин буфер':'min_bufer',
    'Макс буфер':'max_bufer',
    'Буфер в днях продаж':'b_in_days',
    'Активный поставщик':'active_suplayer',
    'Ср.продажи в периоде':'average_sales',
    'Единоразовый заказ':'send_once',
    'Акцизный/неакцизный':'exciseOrNot_exise',
    'Категория цены в зависимости от магазина':'price_category',
    'RD':'RD',
    'GD':'GD',
    'PTO':'PTO',
    'Тип цены':'type_price'
    }

HEADERS_TYPE = {
    'mts':'I',
    'sku':'I',
    'active':'I',
    'name':'S',
    'warehouse':'S',
    'suplayer':'S',
    'moq':'F',
    'bufer':'F',
    'leftover':'F',
    'matrix':'S',
    'ob_index':'I', # HMMMMMM
    'on_the_way':'F',
    'opb_index':'I', # HMMMMMM
    'next_order':'S', # date
    'adu':'F',
    'bufer_date':'S', # date
    'movers':'S',
    'bb_2':'F',
    'bb_3':'F',
    'bb':'F',
    'splt_grp':'S',
    'nomenclature_1':'S',
    'warehouse_code':'I',
    'supler_code':'S',
    'autosend':'I',
    'weight':'F',
    'usq':'F',
    'buy':'F',
    'sell':'F',
    'measure_unit':'S',
    'order_amount':'F',
    'bb_in_days':'F',
    'nomenclature_2':'S',
    'nomenclature_3':'S',
    'periode':'S',
    'min_bufer':'F',
    'max_bufer':'F',
    'b_in_days':'F',
    'average_sales':'F',
    'active_suplayer':'S',
    'bb_4':'F',
    'send_once':'S',
    'exciseOrNot_exise':'S',
    'price_category':'S',
    'RD':'I',
    'GD':'I',
    'PTO':'F',
    'type_price':'S'
    }

NOT_ACTIVE = [
    'АКЦІЯ',
    #'Быт.Химия,косметика,парфюмерия',
    #'Вино',
    #'Водка,ликеры,настойки, бальзами',
    #'Дитяче харчування',
    #'Жевательная резинка',
    'Замороженное,охлажденное мясо',
    #'Кетчуп,соус,майонез',
    'Колбасные и мясные изделия',
    'Конд.изделия (выпечка)',
    #'Конд.изделия (шок,конфеты,печ)',
    #'Консервация овощная фруктовая грибы',
    #'Концентраты',
    #'Коньяк',
    #'Корма для тварин',
    #'Кофе,чай',
    #'Крупы',
    #'Макароны',
    #'Мин.вода и напитки',
    'Молочная продукция',
    'Мороженое',
    #'Мясные и рыбные консервы',
    'Мясо замороженное',
    'Мясо охлажденное',
    #'Оливкове,рослинне масло',
    #'Пиво',
    'Полуфабрикаты ,заморож овощи,фрукты',
    'Рыба и рыбная продукция',
    #'Слабоалк.напитки',
    'Собственная продукция',
    #'Соки',
    #'Сопутств.товары не прод.группы',
    #'Сыпучие (сахар, соль, мука)',
    'Сыры',
    'Табачные изделия',
    #'Товар сопутств.группы, снеки',
    'Фрукты и овощи',
    'Хлебобулочные изделия',
    #'Шампанское Игристые вина',
    #'Элитные напитки и товары',
    'Яйце'
    ]
    
NOT_IN_INVENTORY = [
    #'Моторостроителей 54а',
    #'Бульвар Шевченко',
    'Бульвар Шевч Алко',
    #'Зестафонская',
    #'Авраменко',
    #'Олимпийская',
    #'Комсомольская',
    #'Новгородская',
    #'Комарова',
    #'Грязнова',
    #'Малиновского',
    #'Радиаторная',
    #'Космическая',
    #'Орджоникидзе',
    #'пр. Соборный 167',
    #'Акимовка',
    #'Веселое ул Молодежная 2',
    #'Веселое 2 ул.Московская,21',
    #'Приморск',
    #'Тепличный',
    #'Токмак',
    #'Буча',
    #'Украинка',
    #'БЦ Петра Запорожца',
    #'БЦ Победы 20',
    #'Триполье',
    #'Бабенцы',
    #'8 Марта 3',
    #'Анголенко',
    #'Гуляйполе',
    #'Орехов',
    #'Змиев',
    #'Чумаченко',
    #'Кирилловка',
    #'Мелитополь 1',
    #'Ладожская',
    #'Цитрусовая',
    #'Орехов 2',
    #'Михайловка',
    #'БЦ Бул. Александр.',
    #'Токмак 2',
    '8 Марта 58 (Алко)',
    #'Запорожская',
    'Васильевка Алко',
    #'Пологи',
    #'Мачухи',
    #'Гаврилова',
    'пр. Соборный 224 (Алко)',
    'Северокольцевая (Алко)',
    #'Бельфорский',
    'Запорожская Алко',
    #'Товарищеская',
    'пр. Соборный 58 (Алко)',
    'Бердянск (Алко)'
    ]