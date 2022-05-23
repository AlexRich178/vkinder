from vk_api.keyboard import VkKeyboard, VkKeyboardColor


# Настройки клавиатур
settings = dict(one_time=False, inline=False)

# Клавиатура №0 спрятать клавиатуру
keyboard_0 = VkKeyboard.get_empty_keyboard()

# Клавиатура №1 Меню 1
keyboard_1 = VkKeyboard(**settings)
keyboard_1.add_callback_button(label='Найти пару❤', color=VkKeyboardColor.POSITIVE,
                               payload={"type": "start_search"})

# Клавиатура №9 Меню2
keyboard_9 = VkKeyboard(**settings)
keyboard_9.add_callback_button(label='Найти пару❤', color=VkKeyboardColor.POSITIVE,
                               payload={"type": "start_search"})
keyboard_9.add_line()
keyboard_9.add_callback_button(label='Посмотреть избранное👀', color=VkKeyboardColor.POSITIVE,
                               payload={"type": "show_favorite"})
keyboard_9.add_line()
keyboard_9.add_callback_button(label='Очистить избранное', color=VkKeyboardColor.NEGATIVE,
                               payload={"type": "del_favorite"})
keyboard_9.add_line()
keyboard_9.add_callback_button(label='Завершить общение', color=VkKeyboardColor.NEGATIVE,
                               payload={"type": "end"})

# Клавиатура №2 Выбор пола
keyboard_2 = VkKeyboard(**settings)
keyboard_2.add_callback_button(label='Парень🕺️', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "male"})
keyboard_2.add_callback_button(label='Девушка💃', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "female"})
# Клавиатура №3 Выбор возраста
keyboard_3 = VkKeyboard(**settings)
keyboard_3.add_callback_button(label='18-25', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "age1"})
keyboard_3.add_callback_button(label='25-35', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "age2"})
keyboard_3.add_line()

keyboard_3.add_callback_button(label='35-45', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "age3"})
keyboard_3.add_callback_button(label='45-55', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "age4"})
keyboard_3.add_line()

keyboard_3.add_callback_button(label='55-65', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "age5"})
keyboard_3.add_callback_button(label='65-75', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "age6"})
keyboard_3.add_line()

keyboard_3.add_callback_button(label='75-85', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "age7"})
keyboard_3.add_callback_button(label='85-95', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "age8"})
keyboard_3.add_line()
keyboard_3.add_callback_button(label='Меню', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "restart"})

# Клавиатура №4 Результаты поиска
keyboard_4 = VkKeyboard(**settings)
keyboard_4.add_callback_button(label='Показать результаты!', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "res"})
keyboard_4.add_line()
keyboard_4.add_callback_button(label='Меню', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "restart"})
# Клавиатура №5 Кнопки вперед назад
keyboard_5 = VkKeyboard(**settings)
keyboard_5.add_callback_button(label='⬅Назад', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "back"})
keyboard_5.add_callback_button(label='Вперед➡', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "next"})
keyboard_5.add_line()
keyboard_5.add_callback_button(label='Добавить в избранное⭐', color=VkKeyboardColor.POSITIVE,
                               payload={"type": "add_favorite"})
keyboard_5.add_line()
keyboard_5.add_callback_button(label='Посмотреть избранное👀', color=VkKeyboardColor.POSITIVE,
                               payload={"type": "show_favorite"})
keyboard_5.add_line()
keyboard_5.add_callback_button(label='Меню', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "restart"})

# Клавиатура №6 Кнопка вперед
keyboard_6 = VkKeyboard(**settings)
keyboard_6.add_callback_button(label='Вперед➡', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "next"})
keyboard_6.add_line()
keyboard_6.add_callback_button(label='Добавить в избранное⭐', color=VkKeyboardColor.POSITIVE,
                               payload={"type": "add_favorite"})
keyboard_6.add_line()
keyboard_6.add_callback_button(label='Посмотреть избранное👀', color=VkKeyboardColor.POSITIVE,
                               payload={"type": "show_favorite"})
keyboard_6.add_line()
keyboard_6.add_callback_button(label='Меню', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "restart"})
# Клавиатура №7 Кнопка назад
keyboard_7 = VkKeyboard(**settings)
keyboard_7.add_callback_button(label='⬅Назад', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "back"})
keyboard_7.add_line()
keyboard_7.add_callback_button(label='Добавить в избранное⭐', color=VkKeyboardColor.POSITIVE,
                               payload={"type": "add_favorite"})
keyboard_7.add_line()
keyboard_7.add_callback_button(label='Посмотреть избранное👀', color=VkKeyboardColor.POSITIVE,
                               payload={"type": "show_favorite"})
keyboard_7.add_line()
keyboard_7.add_callback_button(label='Меню', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "restart"})

# Клавиатура №8 да/нет
keyboard_8 = VkKeyboard(**settings)
keyboard_8.add_callback_button(label='Да, очистить избранное', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "yes"})
keyboard_8.add_line()
keyboard_8.add_callback_button(label='Нет, я передумал', color=VkKeyboardColor.PRIMARY,
                               payload={"type": "no"})

# ToDO: на отдельном сервере можно будет сделать авторизацию вк по кнопке
# keyboard_1.add_openlink_button(label='Предоставить свой Токен',
#                                link=f"https://oauth.vk.com/authorize?client_id=8169690&scope=1073737727"
#                                     f"&redirect_uri= "
#                                     f"адрес сервера/callback&display=page&response_type=code"
#                                     f"&revoke=1&state={user_id}",
#                                payload={"type": "link"})
