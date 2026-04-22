from aiogram import types

LANG_NAMES = {'uk': 'Українська', 'ru': 'Русский', 'en': 'English'}

TRANSLATIONS = {'uk': {'btn_menu': '🏠 Меню', 'btn_help': 'ℹ️ Допомога', 'btn_language': '🌐 Мова', 'btn_new_ad': '📝 Створити заявку', 'btn_my_orders': '📦 Мої заявки', 'btn_my_ref': '🔗 Моє реф. посилання', 'btn_set_upper': '✏️ Верх', 'btn_set_middle': '✏️ Середина', 'btn_set_bottom': '✏️ Низ', 'btn_preview': '👁 Перегляд', 'btn_upload_media': '📥 Медіа', 'btn_chat_id': '🆔 Chat ID', 'btn_channels': '📚 Канали', 'btn_add_channel': '➕ Додати канали', 'btn_delete_channels': '🗑 Видалити канали', 'btn_delete_one_channel': '🧹 Видалити 1 канал', 'btn_channels_list': '📋 Список каналів', 'btn_queue_now': '🚀 Опублікувати зараз', 'btn_delete_my_posts': '🗑 Видалити мої пости', 'btn_stats': '📊 Статистика', 'btn_webpanel': '🌍 Веб-панель', 'btn_autopost_on': '▶️ Автопост ON', 'btn_autopost_off': '⏸ Автопост OFF', 'btn_staff': '👥 Співробітники', 'btn_add_staff': '➕ Додати співробітника', 'btn_remove_staff': '🗑 Видалити співробітника', 'btn_staff_list': '📋 Список співробітників', 'btn_schedule': '📅 Графік публікацій', 'btn_tariffs': '💳 Тарифи', 'btn_news': '📰 Новини', 'btn_back': '↩️ Назад', 'btn_cancel': '❌ Скасувати', 'role_owner': 'Власник', 'role_admin': 'Адмін', 'role_moderator': 'Модератор', 'role_user': 'Користувач', 'welcome_user': 'Вітаю! Це бот для заявок та роботи з контентом. Ваша роль: <b>{role}</b>.', 'welcome_staff': 'Вітаю! Ви увійшли як співробітник. Ваша роль: <b>{role}</b>.', 'help_user': 'ℹ️ <b>Довідка для користувача</b>\n\n• <b>Створити заявку</b> — створення рекламної заявки.\n• <b>Мої заявки</b> — перегляд ваших заявок.\n• <b>Тарифи</b> — ціни на розміщення.\n• <b>Новини</b> — оновлення сервісу.\n• <b>Графік публікацій</b> — коли виходять автоматичні пости.\n• <b>Мова</b> — зміна інтерфейсу.', 'help_moderator': 'ℹ️ <b>Довідка для модератора</b>\n\n• <b>Канали</b> — меню керування каналами.\n• <b>Формат додавання</b>: <code>-1001234567890|general|100</code>\n• Перше поле — ID каналу.\n• Друге — категорія: <code>general</code>, <code>vip</code>, <code>news</code>, <code>adult</code>.\n• Третє — ціна в USD за 1 розміщення.\n• <b>Медіа</b> — завантаження фото/відео/документа.\n• <b>Перегляд</b> — попередній перегляд шаблону.\n• <b>Графік публікацій</b> — показує дні, час публікації та видалення.', 'help_admin': 'ℹ️ <b>Довідка для адміністратора</b>\n\n<b>Шаблон поста</b>\n• Верх / Середина / Низ — три частини шаблону.\n• Перегляд — показує зібраний пост.\n\n<b>Канали</b>\n• Додати канали — можна надсилати одразу кілька рядків.\n• Формат: <code>-1001234567890|general|100</code>\n• Категорії: <code>general</code>, <code>vip</code>, <code>news</code>, <code>adult</code>.\n• Ціна — в USD за 1 розміщення.\n\n<b>Співробітники</b>\n• Додати співробітника — видає роль <code>moderator</code> або <code>admin</code>.\n• Видалити співробітника — знімає доступ.\n\n<b>Публікація</b>\n• Опублікувати зараз — ручна публікація у всі додані канали.\n• Видалити мої пости — ручне видалення активних постів.\n• Автопост ON/OFF — увімкнення та вимкнення графіка.\n• Графік публікацій — показує дні, час ранкової публікації та вечірнього видалення.\n\n<b>Інше</b>\n• Тарифи — ціни на розміщення.\n• Новини — зміни та оновлення.\n• Веб-панель — швидке відкриття панелі.', 'choose_language': 'Оберіть мову інтерфейсу:', 'language_changed': 'Мову змінено.', 'no_access': 'Немає доступу до цієї дії.', 'start_first': 'Спочатку надішліть /start.', 'cancelled': 'Дію скасовано.', 'menu_about_user': 'Головне меню користувача. Тут можна створювати заявки, дивитися тарифи, новини та графік публікацій.', 'menu_about_moderator': 'Головне меню модератора. Тут доступні канали, медіа, перегляд поста та графік публікацій.', 'menu_about_admin': 'Головне меню адміністратора. Тут доступні шаблон поста, канали, співробітники, ручна публікація, видалення постів, графік, тарифи, новини та статистика.', 'channels_menu_info': '📚 <b>Меню каналів</b>\n\n• <b>Додати канали</b> — формат: <code>-1001234567890|general|100</code>\n• Можна надіслати відразу кілька рядків.\n• <b>Видалити канали</b> — очищає весь список ваших каналів.\n• <b>Видалити 1 канал</b> — видаляє один канал за ID.\n• <b>Список каналів</b> — показує назву, ID, категорію та ціну.\n\nКатегорії: <code>general</code>, <code>vip</code>, <code>news</code>, <code>adult</code>.\nЦіна вказується в <b>USD</b> за одне розміщення.', 'staff_menu_info': '👥 <b>Меню співробітників</b>\n\n• <b>Додати співробітника</b> — вкажіть ID користувача, потім роль <code>moderator</code> або <code>admin</code>.\n• <b>Видалити співробітника</b> — вкажіть ID користувача, щоб повернути роль <code>user</code>.\n• <b>Список співробітників</b> — покаже всіх співробітників та їх ролі.', 'schedule_info': '📅 <b>Графік публікацій</b>\n\nДні: <code>{weekdays}</code>\nПублікація: <code>{post_time}</code>\nВидалення: <code>{delete_time}</code>\nСтатус: <b>{status}</b>\n\nБот може сам опублікувати пост зранку та видалити його ввечері. Налаштування днів і часу доступне через БД/панель; тут показується поточний графік.', 'schedule_status_on': 'увімкнено', 'schedule_status_off': 'вимкнено', 'tariffs_info': '💳 <b>Тарифи</b>\n\n• <b>general</b> — базове розміщення.\n• <b>vip</b> — преміум-розміщення.\n• <b>news</b> — новинні канали.\n• <b>adult</b> — тематичні 18+ канали.\n\nЦіна вказується в <b>USD</b> за 1 пост. Конкретна вартість кожного каналу задається при додаванні каналу.', 'news_info': '📰 <b>Новини</b>\n\nТут будуть зібрані останні зміни бота: нові функції, патчі, зміни тарифів та оновлення графіка публікацій.', 'ask_upper': 'Надішліть верхній текст шаблону.', 'ask_middle': 'Надішліть середній текст шаблону.', 'ask_bottom': 'Надішліть нижній текст шаблону.', 'saved_upper': 'Верхній текст збережено.', 'saved_middle': 'Середній текст збережено.', 'saved_bottom': 'Нижній текст збережено.', 'template_empty': 'Шаблон поки порожній.', 'upload_hint': 'Надішліть фото, відео або документ у цей чат.', 'photo_saved': 'Фото збережено. ID медіа: {media_id}', 'video_saved': 'Відео збережено. ID медіа: {media_id}', 'document_saved': 'Документ збережено. ID медіа: {media_id}', 'current_chat_info': 'Поточний чат:\nНазва: <b>{title}</b>\nТип: {type}\nID: <code>{id}</code>\nUsername: {username}', 'forward_for_chat_id': 'Перешліть повідомлення з каналу/чату або надішліть рядок: <code>-100...|category|price</code>', 'add_channel_prompt': 'Надішліть один або кілька рядків у форматі:\n<code>-1001234567890|general|100</code>\n\nДе:\n• перше поле — ID каналу\n• друге — категорія\n• третє — ціна в USD за 1 пост\n\nДоступні категорії: <code>general</code>, <code>vip</code>, <code>news</code>, <code>adult</code>.', 'forward_result': 'Знайдено чат:\nНазва: <b>{title}</b>\nТип: {type}\nID: <code>{id}</code>\nUsername: {username}', 'channel_invalid': 'Невірний формат. Потрібно: <code>-100...|category|price</code>', 'channel_saved': 'Канал збережено:\n<b>{title}</b>\nID: <code>{channel_id}</code>\nКатегорія: {category}\nЦіна: {price} USD', 'channels_empty': 'У вас ще немає каналів.', 'channels_title': 'Ваші канали:\n\n{items}', 'channels_deleted_all': 'Усі ваші канали видалено.', 'ask_delete_one_channel': 'Надішліть ID каналу для видалення.', 'channel_deleted_one': 'Канал видалено: <code>{channel_id}</code>', 'new_ad_started': 'Надішліть текст рекламної заявки.', 'ask_ad_category': 'Вкажіть категорію заявки, наприклад: general, vip, premium.', 'ad_saved': 'Заявку створено. ID: <code>{order_id}</code>', 'orders_empty': 'Заявок ще немає.', 'my_orders_title': 'Ваші заявки:\n\n{items}', 'staff_orders_title': 'Останні заявки:\n\n{items}', 'queued_now_empty_channels': 'Спочатку додайте хоча б один канал.', 'queued_now_success': 'Додано в чергу: {count} пост(ів).', 'manual_delete_placeholder': 'Функція видалення постів доступна у сервісі публікації. Кнопка підготовлена в інтерфейсі.', 'autopost_enabled': 'Автопост увімкнено.', 'autopost_disabled': 'Автопост вимкнено.', 'stats': '📊 Статистика\n\nКористувачі: {users}\nСпівробітники: {staff}\nКанали: {channels}\nМедіа: {media_files}\nЗаявки: {ad_orders}\nЧерга: {queue_total}\nВідправлено: {queue_sent}\nПомилки: {queue_failed}\nРеферали: {referrals}', 'my_ref': 'Ваше реферальне посилання:\n{link}\n\nБаланс: {balance}', 'enter_user_id': 'Надішліть ID користувача.', 'need_numeric_user_id': 'Потрібен числовий ID.', 'enter_staff_role': 'Надішліть роль для співробітника: <code>moderator</code> або <code>admin</code>.', 'invalid_staff_role': 'Невірна роль. Доступно: <code>moderator</code> або <code>admin</code>.', 'staff_added': 'Співробітника додано або оновлено.', 'staff_removed': 'Співробітнику скинуто роль до user.', 'staff_empty': 'Список співробітників порожній.', 'staff_denied': 'Лише адміністратор або власник може керувати співробітниками.', 'webpanel_link': 'Веб-панель: {url}'}, 'ru': {'btn_menu': '🏠 Меню', 'btn_help': 'ℹ️ Помощь', 'btn_language': '🌐 Язык', 'btn_new_ad': '📝 Создать заявку', 'btn_my_orders': '📦 Мои заявки', 'btn_my_ref': '🔗 Моя реф. ссылка', 'btn_set_upper': '✏️ Верх', 'btn_set_middle': '✏️ Середина', 'btn_set_bottom': '✏️ Низ', 'btn_preview': '👁 Предпросмотр', 'btn_upload_media': '📥 Медиа', 'btn_chat_id': '🆔 Chat ID', 'btn_channels': '📚 Канали', 'btn_add_channel': '➕ Добавить каналы', 'btn_delete_channels': '🗑 Удалить каналы', 'btn_delete_one_channel': '🧹 Удалить 1 канал', 'btn_channels_list': '📋 Список каналов', 'btn_queue_now': '🚀 Опубликовать сейчас', 'btn_delete_my_posts': '🗑 Удалить мои посты', 'btn_stats': '📊 Статистика', 'btn_webpanel': '🌍 Веб-панель', 'btn_autopost_on': '▶️ Автопост ON', 'btn_autopost_off': '⏸ Автопост OFF', 'btn_staff': '👥 Сотрудники', 'btn_add_staff': '➕ Добавить сотрудника', 'btn_remove_staff': '🗑 Удалить сотрудника', 'btn_staff_list': '📋 Список сотрудников', 'btn_schedule': '📅 График публикаций', 'btn_tariffs': '💳 Тарифы', 'btn_news': '📰 Новости', 'btn_back': '↩️ Назад', 'btn_cancel': '❌ Отмена', 'role_owner': 'Владелец', 'role_admin': 'Адмін', 'role_moderator': 'Модератор', 'role_user': 'Пользователь', 'welcome_user': 'Добро пожаловать! Это бот для заявок и работы с контентом. Ваша роль: <b>{role}</b>.', 'welcome_staff': 'Добро пожаловать! Вы вошли как сотрудник. Ваша роль: <b>{role}</b>.', 'help_user': 'ℹ️ <b>Довідка для користувача</b>\n\n• <b>Створити заявку</b> — створення рекламної заявки.\n• <b>Мої заявки</b> — перегляд ваших заявок.\n• <b>Тарифи</b> — ціни на розміщення.\n• <b>Новини</b> — оновлення сервісу.\n• <b>Графік публікацій</b> — коли виходять автоматичні пости.\n• <b>Мова</b> — зміна інтерфейсу.', 'help_moderator': 'ℹ️ <b>Довідка для модератора</b>\n\n• <b>Канали</b> — меню керування каналами.\n• <b>Формат додавання</b>: <code>-1001234567890|general|100</code>\n• Перше поле — ID каналу.\n• Друге — категорія: <code>general</code>, <code>vip</code>, <code>news</code>, <code>adult</code>.\n• Третє — ціна в USD за 1 розміщення.\n• <b>Медіа</b> — завантаження фото/відео/документа.\n• <b>Перегляд</b> — попередній перегляд шаблону.\n• <b>Графік публікацій</b> — показує дні, час публікації та видалення.', 'help_admin': 'ℹ️ <b>Довідка для адміністратора</b>\n\n<b>Шаблон поста</b>\n• Верх / Середина / Низ — три частини шаблону.\n• Перегляд — показує зібраний пост.\n\n<b>Канали</b>\n• Додати канали — можна надсилати одразу кілька рядків.\n• Формат: <code>-1001234567890|general|100</code>\n• Категорії: <code>general</code>, <code>vip</code>, <code>news</code>, <code>adult</code>.\n• Ціна — в USD за 1 розміщення.\n\n<b>Співробітники</b>\n• Додати співробітника — видає роль <code>moderator</code> або <code>admin</code>.\n• Видалити співробітника — знімає доступ.\n\n<b>Публікація</b>\n• Опублікувати зараз — ручна публікація у всі додані канали.\n• Видалити мої пости — ручне видалення активних постів.\n• Автопост ON/OFF — увімкнення та вимкнення графіка.\n• Графік публікацій — показує дні, час ранкової публікації та вечірнього видалення.\n\n<b>Інше</b>\n• Тарифи — ціни на розміщення.\n• Новини — зміни та оновлення.\n• Веб-панель — швидке відкриття панелі.', 'choose_language': 'Выберите язык интерфейса:', 'language_changed': 'Язык изменён.', 'no_access': 'Нет доступа к этому действию.', 'start_first': 'Сначала отправьте /start.', 'cancelled': 'Действие отменено.', 'menu_about_user': 'Головне меню користувача. Тут можна створювати заявки, дивитися тарифи, новини та графік публікацій.', 'menu_about_moderator': 'Головне меню модератора. Тут доступні канали, медіа, перегляд поста та графік публікацій.', 'menu_about_admin': 'Головне меню адміністратора. Тут доступні шаблон поста, канали, співробітники, ручна публікація, видалення постів, графік, тарифи, новини та статистика.', 'channels_menu_info': '📚 <b>Меню каналів</b>\n\n• <b>Додати канали</b> — формат: <code>-1001234567890|general|100</code>\n• Можна надіслати відразу кілька рядків.\n• <b>Видалити канали</b> — очищає весь список ваших каналів.\n• <b>Видалити 1 канал</b> — видаляє один канал за ID.\n• <b>Список каналів</b> — показує назву, ID, категорію та ціну.\n\nКатегорії: <code>general</code>, <code>vip</code>, <code>news</code>, <code>adult</code>.\nЦіна вказується в <b>USD</b> за одне розміщення.', 'staff_menu_info': '👥 <b>Меню співробітників</b>\n\n• <b>Додати співробітника</b> — вкажіть ID користувача, потім роль <code>moderator</code> або <code>admin</code>.\n• <b>Видалити співробітника</b> — вкажіть ID користувача, щоб повернути роль <code>user</code>.\n• <b>Список співробітників</b> — покаже всіх співробітників та їх ролі.', 'schedule_info': '📅 <b>Графік публікацій</b>\n\nДні: <code>{weekdays}</code>\nПублікація: <code>{post_time}</code>\nВидалення: <code>{delete_time}</code>\nСтатус: <b>{status}</b>\n\nБот може сам опублікувати пост зранку та видалити його ввечері. Налаштування днів і часу доступне через БД/панель; тут показується поточний графік.', 'schedule_status_on': 'включён', 'schedule_status_off': 'выключен', 'tariffs_info': '💳 <b>Тарифи</b>\n\n• <b>general</b> — базове розміщення.\n• <b>vip</b> — преміум-розміщення.\n• <b>news</b> — новинні канали.\n• <b>adult</b> — тематичні 18+ канали.\n\nЦіна вказується в <b>USD</b> за 1 пост. Конкретна вартість кожного каналу задається при додаванні каналу.', 'news_info': '📰 <b>Новини</b>\n\nТут будуть зібрані останні зміни бота: нові функції, патчі, зміни тарифів та оновлення графіка публікацій.', 'ask_upper': 'Надішліть верхній текст шаблону.', 'ask_middle': 'Надішліть середній текст шаблону.', 'ask_bottom': 'Надішліть нижній текст шаблону.', 'saved_upper': 'Верхній текст збережено.', 'saved_middle': 'Середній текст збережено.', 'saved_bottom': 'Нижній текст збережено.', 'template_empty': 'Шаблон поки порожній.', 'upload_hint': 'Надішліть фото, відео або документ у цей чат.', 'photo_saved': 'Фото збережено. ID медіа: {media_id}', 'video_saved': 'Відео збережено. ID медіа: {media_id}', 'document_saved': 'Документ збережено. ID медіа: {media_id}', 'current_chat_info': 'Поточний чат:\nНазва: <b>{title}</b>\nТип: {type}\nID: <code>{id}</code>\nUsername: {username}', 'forward_for_chat_id': 'Перешліть повідомлення з каналу/чату або надішліть рядок: <code>-100...|category|price</code>', 'add_channel_prompt': 'Надішліть один або кілька рядків у форматі:\n<code>-1001234567890|general|100</code>\n\nДе:\n• перше поле — ID каналу\n• друге — категорія\n• третє — ціна в USD за 1 пост\n\nДоступні категорії: <code>general</code>, <code>vip</code>, <code>news</code>, <code>adult</code>.', 'forward_result': 'Знайдено чат:\nНазва: <b>{title}</b>\nТип: {type}\nID: <code>{id}</code>\nUsername: {username}', 'channel_invalid': 'Невірний формат. Потрібно: <code>-100...|category|price</code>', 'channel_saved': 'Канал збережено:\n<b>{title}</b>\nID: <code>{channel_id}</code>\nКатегорія: {category}\nЦіна: {price} USD', 'channels_empty': 'У вас ще немає каналів.', 'channels_title': 'Ваші канали:\n\n{items}', 'channels_deleted_all': 'Усі ваші канали видалено.', 'ask_delete_one_channel': 'Надішліть ID каналу для видалення.', 'channel_deleted_one': 'Канал видалено: <code>{channel_id}</code>', 'new_ad_started': 'Надішліть текст рекламної заявки.', 'ask_ad_category': 'Вкажіть категорію заявки, наприклад: general, vip, premium.', 'ad_saved': 'Заявку створено. ID: <code>{order_id}</code>', 'orders_empty': 'Заявок ще немає.', 'my_orders_title': 'Ваші заявки:\n\n{items}', 'staff_orders_title': 'Останні заявки:\n\n{items}', 'queued_now_empty_channels': 'Спочатку додайте хоча б один канал.', 'queued_now_success': 'Додано в чергу: {count} пост(ів).', 'manual_delete_placeholder': 'Функція видалення постів доступна у сервісі публікації. Кнопка підготовлена в інтерфейсі.', 'autopost_enabled': 'Автопост увімкнено.', 'autopost_disabled': 'Автопост вимкнено.', 'stats': '📊 Статистика\n\nКористувачі: {users}\nСпівробітники: {staff}\nКанали: {channels}\nМедіа: {media_files}\nЗаявки: {ad_orders}\nЧерга: {queue_total}\nВідправлено: {queue_sent}\nПомилки: {queue_failed}\nРеферали: {referrals}', 'my_ref': 'Ваше реферальне посилання:\n{link}\n\nБаланс: {balance}', 'enter_user_id': 'Надішліть ID користувача.', 'need_numeric_user_id': 'Потрібен числовий ID.', 'enter_staff_role': 'Надішліть роль для співробітника: <code>moderator</code> або <code>admin</code>.', 'invalid_staff_role': 'Невірна роль. Доступно: <code>moderator</code> або <code>admin</code>.', 'staff_added': 'Співробітника додано або оновлено.', 'staff_removed': 'Співробітнику скинуто роль до user.', 'staff_empty': 'Список співробітників порожній.', 'staff_denied': 'Лише адміністратор або власник може керувати співробітниками.', 'webpanel_link': 'Веб-панель: {url}'}, 'en': {'btn_menu': '🏠 Menu', 'btn_help': 'ℹ️ Help', 'btn_language': '🌐 Language', 'btn_new_ad': '📝 New Request', 'btn_my_orders': '📦 My Requests', 'btn_my_ref': '🔗 My Referral', 'btn_set_upper': '✏️ Upper', 'btn_set_middle': '✏️ Middle', 'btn_set_bottom': '✏️ Bottom', 'btn_preview': '👁 Preview', 'btn_upload_media': '📥 Media', 'btn_chat_id': '🆔 Chat ID', 'btn_channels': '📚 Channels', 'btn_add_channel': '➕ Add Channels', 'btn_delete_channels': '🗑 Delete Channels', 'btn_delete_one_channel': '🧹 Delete 1 Channel', 'btn_channels_list': '📋 Channel List', 'btn_queue_now': '🚀 Publish Now', 'btn_delete_my_posts': '🗑 Delete My Posts', 'btn_stats': '📊 Statistics', 'btn_webpanel': '🌍 Web Panel', 'btn_autopost_on': '▶️ Автопост ON', 'btn_autopost_off': '⏸ Автопост OFF', 'btn_staff': '👥 Staff', 'btn_add_staff': '➕ Add Staff', 'btn_remove_staff': '🗑 Remove Staff', 'btn_staff_list': '📋 Staff List', 'btn_schedule': '📅 Posting Schedule', 'btn_tariffs': '💳 Tariffs', 'btn_news': '📰 News', 'btn_back': '↩️ Back', 'btn_cancel': '❌ Cancel', 'role_owner': 'Owner', 'role_admin': 'Admin', 'role_moderator': 'Moderator', 'role_user': 'User', 'welcome_user': 'Welcome! This bot is for requests and content management. Your role: <b>{role}</b>.', 'welcome_staff': 'Welcome! You are logged in as staff. Your role: <b>{role}</b>.', 'help_user': 'ℹ️ <b>User guide</b>\n\n• <b>New Request</b> — create an advertising request.\n• <b>My Requests</b> — view your requests.\n• <b>Tariffs</b> — placement prices.\n• <b>News</b> — service updates.\n• <b>Posting Schedule</b> — when automatic posts are published.\n• <b>Language</b> — change interface language.', 'help_moderator': 'ℹ️ <b>Moderator guide</b>\n\n• <b>Channels</b> — channel management menu.\n• <b>Add format</b>: <code>-1001234567890|general|100</code>\n• First field — channel ID.\n• Second — category: <code>general</code>, <code>vip</code>, <code>news</code>, <code>adult</code>.\n• Third — price in USD for 1 placement.\n• <b>Media</b> — upload photo/video/document.\n• <b>Preview</b> — preview the template.\n• <b>Posting Schedule</b> — shows weekdays, publish time and delete time.', 'help_admin': 'ℹ️ <b>Administrator guide</b>\n\n<b>Post template</b>\n• Upper / Middle / Bottom — three parts of the template.\n• Preview — shows the assembled post.\n\n<b>Channels</b>\n• Add Channels — you can send several lines at once.\n• Format: <code>-1001234567890|general|100</code>\n• Categories: <code>general</code>, <code>vip</code>, <code>news</code>, <code>adult</code>.\n• Price — in USD per 1 placement.\n\n<b>Staff</b>\n• Add Staff — assign <code>moderator</code> or <code>admin</code>.\n• Remove Staff — revoke access.\n\n<b>Publishing</b>\n• Publish Now — manual publishing to all added channels.\n• Delete My Posts — manual deletion of active posts.\n• Auto-post ON/OFF — enable or disable the schedule.\n• Posting Schedule — shows weekdays, morning publish time and evening delete time.\n\n<b>Other</b>\n• Tariffs — placement prices.\n• News — changes and updates.\n• Web panel — quick panel link.', 'choose_language': 'Оберіть мову інтерфейсу:', 'language_changed': 'Мову змінено.', 'no_access': 'Немає доступу до цієї дії.', 'start_first': 'Спочатку надішліть /start.', 'cancelled': 'Дію скасовано.', 'menu_about_user': 'Main user menu. Here you can create requests, check tariffs, news and posting schedule.', 'menu_about_moderator': 'Main moderator menu. Here you can manage channels, media, post preview and posting schedule.', 'menu_about_admin': 'Main administrator menu. Here you can manage post template, channels, staff, manual publishing, post deletion, schedule, tariffs, news and stats.', 'channels_menu_info': '📚 <b>Channels menu</b>\n\n• <b>Add Channels</b> — format: <code>-1001234567890|general|100</code>\n• You can send several lines at once.\n• <b>Delete Channels</b> — removes all your channels.\n• <b>Delete 1 Channel</b> — removes one channel by ID.\n• <b>Channel List</b> — shows title, ID, category and price.\n\nCategories: <code>general</code>, <code>vip</code>, <code>news</code>, <code>adult</code>.\nPrice is specified in <b>USD</b> per placement.', 'staff_menu_info': '👥 <b>Staff menu</b>\n\n• <b>Add Staff</b> — send user ID, then role <code>moderator</code> or <code>admin</code>.\n• <b>Remove Staff</b> — send user ID to reset role to <code>user</code>.\n• <b>Staff List</b> — shows all staff members and roles.', 'schedule_info': '📅 <b>Posting schedule</b>\n\nWeekdays: <code>{weekdays}</code>\nPublish time: <code>{post_time}</code>\nDelete time: <code>{delete_time}</code>\nStatus: <b>{status}</b>\n\nThe bot can publish a post in the morning and delete it in the evening. Days and time can be adjusted via DB/panel; this section shows the current schedule.', 'schedule_status_on': 'enabled', 'schedule_status_off': 'disabled', 'tariffs_info': '💳 <b>Tariffs</b>\n\n• <b>general</b> — base placement.\n• <b>vip</b> — premium placement.\n• <b>news</b> — news channels.\n• <b>adult</b> — thematic 18+ channels.\n\nPrice is specified in <b>USD</b> per 1 post. The exact price of each channel is set when adding the channel.', 'news_info': '📰 <b>News</b>\n\nThis section is for the latest bot changes: new features, patches, tariff changes and schedule updates.', 'ask_upper': 'Send the upper text of the template.', 'ask_middle': 'Send the middle text of the template.', 'ask_bottom': 'Send the bottom text of the template.', 'saved_upper': 'Upper text saved.', 'saved_middle': 'Middle text saved.', 'saved_bottom': 'Bottom text saved.', 'template_empty': 'Template is empty for now.', 'upload_hint': 'Send photo, video or document to this chat.', 'photo_saved': 'Photo saved. Media ID: {media_id}', 'video_saved': 'Video saved. Media ID: {media_id}', 'document_saved': 'Document saved. Media ID: {media_id}', 'current_chat_info': 'Current chat:\nTitle: <b>{title}</b>\nType: {type}\nID: <code>{id}</code>\nUsername: {username}', 'forward_for_chat_id': 'Forward a message from a channel/chat or send a row: <code>-100...|category|price</code>', 'add_channel_prompt': 'Send one or several rows in the format:\n<code>-1001234567890|general|100</code>\n\nWhere:\n• first field — channel ID\n• second — category\n• third — price in USD per 1 post\n\nAvailable categories: <code>general</code>, <code>vip</code>, <code>news</code>, <code>adult</code>.', 'forward_result': 'Chat found:\nTitle: <b>{title}</b>\nType: {type}\nID: <code>{id}</code>\nUsername: {username}', 'channel_invalid': 'Invalid format. Required: <code>-100...|category|price</code>', 'channel_saved': 'Channel saved:\n<b>{title}</b>\nID: <code>{channel_id}</code>\nCategory: {category}\nPrice: {price} USD', 'channels_empty': 'You have no channels yet.', 'channels_title': 'Your channels:\n\n{items}', 'channels_deleted_all': 'All your channels were deleted.', 'ask_delete_one_channel': 'Send the channel ID to delete.', 'channel_deleted_one': 'Channel deleted: <code>{channel_id}</code>', 'new_ad_started': 'Send the advertising request text.', 'ask_ad_category': 'Specify request category, for example: general, vip, premium.', 'ad_saved': 'Request created. ID: <code>{order_id}</code>', 'orders_empty': 'No requests yet.', 'my_orders_title': 'Your requests:\n\n{items}', 'staff_orders_title': 'Latest requests:\n\n{items}', 'queued_now_empty_channels': 'Add at least one channel first.', 'queued_now_success': 'Queued: {count} post(s).', 'manual_delete_placeholder': 'Post deletion logic is handled by the posting service. The UI button is ready.', 'autopost_enabled': 'Auto-post enabled.', 'autopost_disabled': 'Auto-post disabled.', 'stats': '📊 Statistics\n\nUsers: {users}\nStaff: {staff}\nChannels: {channels}\nMedia: {media_files}\nRequests: {ad_orders}\nQueue: {queue_total}\nSent: {queue_sent}\nErrors: {queue_failed}\nReferrals: {referrals}', 'my_ref': 'Your referral link:\n{link}\n\nBalance: {balance}', 'enter_user_id': 'Send the user ID.', 'need_numeric_user_id': 'Numeric ID required.', 'enter_staff_role': 'Send staff role: <code>moderator</code> or <code>admin</code>.', 'invalid_staff_role': 'Invalid role. Available: <code>moderator</code> or <code>admin</code>.', 'staff_added': 'Staff member added or updated.', 'staff_removed': 'Staff member role reset to user.', 'staff_empty': 'Staff list is empty.', 'staff_denied': 'Only admin or owner can manage staff.', 'webpanel_link': 'Web panel: {url}'}}

ROLE_LAYOUTS = {'user': [['btn_menu', 'btn_help'], ['btn_new_ad', 'btn_my_orders'], ['btn_my_ref', 'btn_language'], ['btn_tariffs', 'btn_news'], ['btn_schedule']], 'moderator': [['btn_menu', 'btn_help'], ['btn_channels', 'btn_upload_media'], ['btn_preview', 'btn_queue_now'], ['btn_chat_id', 'btn_language'], ['btn_tariffs', 'btn_news'], ['btn_schedule']], 'admin': [['btn_menu', 'btn_help'], ['btn_set_upper', 'btn_set_middle', 'btn_set_bottom'], ['btn_preview', 'btn_upload_media'], ['btn_chat_id', 'btn_channels'], ['btn_staff', 'btn_schedule'], ['btn_queue_now', 'btn_delete_my_posts'], ['btn_autopost_on', 'btn_autopost_off'], ['btn_stats', 'btn_webpanel'], ['btn_tariffs', 'btn_news'], ['btn_language']], 'owner': [['btn_menu', 'btn_help'], ['btn_set_upper', 'btn_set_middle', 'btn_set_bottom'], ['btn_preview', 'btn_upload_media'], ['btn_chat_id', 'btn_channels'], ['btn_staff', 'btn_schedule'], ['btn_queue_now', 'btn_delete_my_posts'], ['btn_autopost_on', 'btn_autopost_off'], ['btn_stats', 'btn_webpanel'], ['btn_tariffs', 'btn_news'], ['btn_language']]}

def normalize_lang(raw: str | None) -> str:
    if not raw:
        return 'ru'
    raw = raw.lower()
    if raw.startswith('uk'): return 'uk'
    if raw.startswith('ru'): return 'ru'
    return 'en'

def get_text(lang: str, key: str, **kwargs) -> str:
    bucket = TRANSLATIONS.get(lang, TRANSLATIONS['ru'])
    text = bucket.get(key, TRANSLATIONS['ru'].get(key, key))
    return text.format(**kwargs)

def get_role_label(lang: str, role: str) -> str:
    return get_text(lang, f'role_{role}')

def build_language_menu(lang: str = 'ru') -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(types.KeyboardButton(LANG_NAMES['uk']), types.KeyboardButton(LANG_NAMES['ru']), types.KeyboardButton(LANG_NAMES['en']))
    kb.row(types.KeyboardButton(get_text(lang, 'btn_menu')), types.KeyboardButton(get_text(lang, 'btn_cancel')))
    return kb

def _build_by_keys(lang: str, rows: list[list[str]]) -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for row in rows:
        kb.row(*[types.KeyboardButton(get_text(lang, key)) for key in row])
    return kb

def build_main_menu(lang: str, role: str, mode: str = 'service') -> types.ReplyKeyboardMarkup:
    layouts = TENANT_ROLE_LAYOUTS if mode == 'tenant' else SERVICE_ROLE_LAYOUTS
    return _build_by_keys(lang, layouts.get(role, layouts['user']))

def build_channels_menu(lang: str) -> types.ReplyKeyboardMarkup:
    return _build_by_keys(lang, [['btn_add_channel','btn_delete_channels'],['btn_delete_one_channel','btn_channels_list'],['btn_back']])

def build_staff_menu(lang: str) -> types.ReplyKeyboardMarkup:
    return _build_by_keys(lang, [['btn_add_staff','btn_remove_staff'],['btn_staff_list'],['btn_back']])


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

SCHEDULE_EXTRA = {
    'uk': {
        'schedule_title': '📅 <b>Графік публікацій</b>',
        'schedule_selected_days': 'Обрані дні: {days}',
        'schedule_post_time_line': 'Час публікації: <code>{post_time}</code>',
        'schedule_delete_time_line': 'Час видалення: <code>{delete_time}</code>',
        'schedule_status_line': 'Статус: <b>{status}</b>',
        'schedule_hint': 'Натискай дні тижня, змінюй час кнопками нижче.',
        'schedule_day_1': 'Пн', 'schedule_day_2': 'Вт', 'schedule_day_3': 'Ср', 'schedule_day_4': 'Чт', 'schedule_day_5': 'Пт', 'schedule_day_6': 'Сб', 'schedule_day_7': 'Нд',
        'schedule_btn_post_time': '🕘 Час публікації',
        'schedule_btn_delete_time': '🕙 Час видалення',
        'schedule_btn_enable': '✅ Увімкнути',
        'schedule_btn_disable': '⛔ Вимкнути',
        'schedule_btn_done': '✔️ Готово',
        'schedule_set_post_time_prompt': 'Надішліть час публікації у форматі <code>10:00</code>.',
        'schedule_set_delete_time_prompt': 'Надішліть час видалення у форматі <code>22:00</code>.',
        'schedule_time_saved': 'Час оновлено: <code>{value}</code>',
        'schedule_invalid_time': 'Невірний формат часу. Приклад: <code>10:00</code>.',
        'schedule_saved': 'Графік оновлено.',
    },
    'ru': {
        'schedule_title': '📅 <b>График публикаций</b>',
        'schedule_selected_days': 'Выбранные дни: {days}',
        'schedule_post_time_line': 'Время публикации: <code>{post_time}</code>',
        'schedule_delete_time_line': 'Время удаления: <code>{delete_time}</code>',
        'schedule_status_line': 'Статус: <b>{status}</b>',
        'schedule_hint': 'Нажимай дни недели и меняй время кнопками ниже.',
        'schedule_day_1': 'Пн', 'schedule_day_2': 'Вт', 'schedule_day_3': 'Ср', 'schedule_day_4': 'Чт', 'schedule_day_5': 'Пт', 'schedule_day_6': 'Сб', 'schedule_day_7': 'Вс',
        'schedule_btn_post_time': '🕘 Время публикации',
        'schedule_btn_delete_time': '🕙 Время удаления',
        'schedule_btn_enable': '✅ Включить',
        'schedule_btn_disable': '⛔ Выключить',
        'schedule_btn_done': '✔️ Готово',
        'schedule_set_post_time_prompt': 'Отправьте время публикации в формате <code>10:00</code>.',
        'schedule_set_delete_time_prompt': 'Отправьте время удаления в формате <code>22:00</code>.',
        'schedule_time_saved': 'Время обновлено: <code>{value}</code>',
        'schedule_invalid_time': 'Неверный формат времени. Пример: <code>10:00</code>.',
        'schedule_saved': 'График обновлён.',
    },
    'en': {
        'schedule_title': '📅 <b>Posting schedule</b>',
        'schedule_selected_days': 'Selected days: {days}',
        'schedule_post_time_line': 'Post time: <code>{post_time}</code>',
        'schedule_delete_time_line': 'Delete time: <code>{delete_time}</code>',
        'schedule_status_line': 'Status: <b>{status}</b>',
        'schedule_hint': 'Tap weekdays and change times with the buttons below.',
        'schedule_day_1': 'Mon', 'schedule_day_2': 'Tue', 'schedule_day_3': 'Wed', 'schedule_day_4': 'Thu', 'schedule_day_5': 'Fri', 'schedule_day_6': 'Sat', 'schedule_day_7': 'Sun',
        'schedule_btn_post_time': '🕘 Post time',
        'schedule_btn_delete_time': '🕙 Delete time',
        'schedule_btn_enable': '✅ Enable',
        'schedule_btn_disable': '⛔ Disable',
        'schedule_btn_done': '✔️ Done',
        'schedule_set_post_time_prompt': 'Send the post time in <code>10:00</code> format.',
        'schedule_set_delete_time_prompt': 'Send the delete time in <code>22:00</code> format.',
        'schedule_time_saved': 'Time updated: <code>{value}</code>',
        'schedule_invalid_time': 'Invalid time format. Example: <code>10:00</code>.',
        'schedule_saved': 'Schedule updated.',
    },
}
for _lang, _vals in SCHEDULE_EXTRA.items():
    TRANSLATIONS.setdefault(_lang, {}).update(_vals)

def _format_weekdays(lang: str, weekdays: str) -> str:
    ids = [x.strip() for x in (weekdays or '').split(',') if x.strip()]
    if not ids:
        ids = ['1','2','3','4','5','6','7']
    return ', '.join(get_text(lang, f'schedule_day_{i}') for i in ids)

def build_schedule_text(lang: str, data: dict) -> str:
    status = get_text(lang, 'schedule_status_on' if data.get('enabled') else 'schedule_status_off')
    return '\n'.join([
        get_text(lang, 'schedule_title'),
        get_text(lang, 'schedule_selected_days', days=_format_weekdays(lang, data.get('weekdays', '1,2,3,4,5,6,7'))),
        get_text(lang, 'schedule_post_time_line', post_time=data.get('post_time', '10:00')),
        get_text(lang, 'schedule_delete_time_line', delete_time=data.get('delete_time', '22:00')),
        get_text(lang, 'schedule_status_line', status=status),
        '',
        get_text(lang, 'schedule_hint'),
    ])

def build_schedule_keyboard(lang: str, data: dict) -> InlineKeyboardMarkup:
    selected = set(x.strip() for x in (data.get('weekdays') or '1,2,3,4,5,6,7').split(',') if x.strip())
    kb = InlineKeyboardMarkup(row_width=4)
    day_buttons = []
    for i in range(1, 8):
        prefix = '✅ ' if str(i) in selected else '▫️ '
        day_buttons.append(InlineKeyboardButton(prefix + get_text(lang, f'schedule_day_{i}'), callback_data=f'sched:day:{i}'))
    kb.row(*day_buttons[:4])
    kb.row(*day_buttons[4:])
    kb.row(
        InlineKeyboardButton(get_text(lang, 'schedule_btn_post_time'), callback_data='sched:set_post_time'),
        InlineKeyboardButton(get_text(lang, 'schedule_btn_delete_time'), callback_data='sched:set_delete_time'),
    )
    if data.get('enabled'):
        kb.row(InlineKeyboardButton(get_text(lang, 'schedule_btn_disable'), callback_data='sched:disable'))
    else:
        kb.row(InlineKeyboardButton(get_text(lang, 'schedule_btn_enable'), callback_data='sched:enable'))
    kb.row(InlineKeyboardButton(get_text(lang, 'schedule_btn_done'), callback_data='sched:done'))
    return kb


CLIENT_BOT_EXTRA = {
    'uk': {
        'btn_my_bot': '🤖 Мій бот',
        'btn_connect_bot': '🔑 Підключити токен',
        'btn_rental_status': '📄 Статус оренди',
        'btn_client_bots': '🤖 Клієнтські боти',
        'client_bot_intro_user': 'Тут керування вашим орендованим ботом: підключення токена, перевірка статусу оренди та даних бота.',
        'client_bot_intro_admin': 'Тут ви керуєте клієнтськими ботами: перегляд підключених токенів, статусів та активація оренди.',
        'connect_bot_prompt': 'Надішліть токен вашого бота з BotFather. Формат токена: <code>123456:ABC...</code>',
        'connect_bot_success': '✅ Бота підключено.\n\nІмʼя: <b>{bot_name}</b>\nUsername: @{bot_username}\nBot ID: <code>{bot_id}</code>\nСтатус: <b>{status}</b>',
        'connect_bot_invalid': '❌ Токен не пройшов перевірку. Переконайтесь, що ви скопіювали його з BotFather без зайвих пробілів.',
        'my_bot_empty': 'У вас ще не підключено жодного клієнтського бота.',
        'my_bot_card': '🤖 <b>Ваш бот</b>\n\nІмʼя: <b>{bot_name}</b>\nUsername: @{bot_username}\nBot ID: <code>{bot_id}</code>\nСтатус: <b>{status}</b>\nТариф: <code>{plan_type}</code>\nОренда до: <code>{rent_until}</code>',
        'rental_status_empty': 'Статус оренди поки недоступний: бот ще не підключено.',
        'rental_status_text': '📄 <b>Статус оренди</b>\n\nСтатус: <b>{status}</b>\nТариф: <code>{plan_type}</code>\nАктивно до: <code>{rent_until}</code>',
        'client_bots_empty': 'Клієнтських ботів поки немає.',
        'client_bots_title': '🤖 <b>Клієнтські боти</b>\n\n{items}',
        'client_bot_item': '<code>{owner_user_id}</code> | <b>{status}</b> | @{bot_username} | до <code>{rent_until}</code>',
        'activate_rental_prompt_user': 'Надішліть Telegram ID клієнта, якому потрібно активувати оренду.',
        'activate_rental_days_prompt': 'Надішліть кількість днів оренди, наприклад: <code>30</code>',
        'activate_rental_success': '✅ Оренду активовано на <b>{days}</b> дн. для користувача <code>{owner_user_id}</code>.',
        'activate_rental_no_bot': 'У цього користувача ще не підключено клієнтського бота.',
        'need_positive_days': 'Потрібне додатне число днів.',
    },
    'ru': {
        'btn_my_bot': '🤖 Мой бот',
        'btn_connect_bot': '🔑 Подключить токен',
        'btn_rental_status': '📄 Статус аренды',
        'btn_client_bots': '🤖 Клиентские боты',
        'client_bot_intro_user': 'Здесь управление вашим арендованным ботом: подключение токена, проверка статуса аренды и данных бота.',
        'client_bot_intro_admin': 'Здесь вы управляете клиентскими ботами: просмотр подключённых токенов, статусов и активация аренды.',
        'connect_bot_prompt': 'Отправьте токен вашего бота из BotFather. Формат токена: <code>123456:ABC...</code>',
        'connect_bot_success': '✅ Бот подключён.\n\nИмя: <b>{bot_name}</b>\nUsername: @{bot_username}\nBot ID: <code>{bot_id}</code>\nСтатус: <b>{status}</b>',
        'connect_bot_invalid': '❌ Токен не прошёл проверку. Убедитесь, что вы скопировали его из BotFather без лишних пробелов.',
        'my_bot_empty': 'У вас ещё не подключен ни один клиентский бот.',
        'my_bot_card': '🤖 <b>Ваш бот</b>\n\nИмя: <b>{bot_name}</b>\nUsername: @{bot_username}\nBot ID: <code>{bot_id}</code>\nСтатус: <b>{status}</b>\nТариф: <code>{plan_type}</code>\nАренда до: <code>{rent_until}</code>',
        'rental_status_empty': 'Статус аренды пока недоступен: бот ещё не подключён.',
        'rental_status_text': '📄 <b>Статус аренды</b>\n\nСтатус: <b>{status}</b>\nТариф: <code>{plan_type}</code>\nАктивно до: <code>{rent_until}</code>',
        'client_bots_empty': 'Клиентских ботов пока нет.',
        'client_bots_title': '🤖 <b>Клиентские боты</b>\n\n{items}',
        'client_bot_item': '<code>{owner_user_id}</code> | <b>{status}</b> | @{bot_username} | до <code>{rent_until}</code>',
        'activate_rental_prompt_user': 'Отправьте Telegram ID клиента, которому нужно активировать аренду.',
        'activate_rental_days_prompt': 'Отправьте количество дней аренды, например: <code>30</code>',
        'activate_rental_success': '✅ Аренда активирована на <b>{days}</b> дн. для пользователя <code>{owner_user_id}</code>.',
        'activate_rental_no_bot': 'У этого пользователя ещё не подключён клиентский бот.',
        'need_positive_days': 'Нужно положительное число дней.',
    },
    'en': {
        'btn_my_bot': '🤖 My bot',
        'btn_connect_bot': '🔑 Connect token',
        'btn_rental_status': '📄 Rental status',
        'btn_client_bots': '🤖 Client bots',
        'client_bot_intro_user': 'Manage your rented bot here: connect a token, check rental status and bot details.',
        'client_bot_intro_admin': 'Manage client bots here: view connected tokens, statuses and activate rentals.',
        'connect_bot_prompt': 'Send your bot token from BotFather. Token format: <code>123456:ABC...</code>',
        'connect_bot_success': '✅ Bot connected.\n\nName: <b>{bot_name}</b>\nUsername: @{bot_username}\nBot ID: <code>{bot_id}</code>\nStatus: <b>{status}</b>',
        'connect_bot_invalid': '❌ Token validation failed. Make sure you copied it from BotFather without extra spaces.',
        'my_bot_empty': 'You have not connected any client bot yet.',
        'my_bot_card': '🤖 <b>Your bot</b>\n\nName: <b>{bot_name}</b>\nUsername: @{bot_username}\nBot ID: <code>{bot_id}</code>\nStatus: <b>{status}</b>\nPlan: <code>{plan_type}</code>\nRent until: <code>{rent_until}</code>',
        'rental_status_empty': 'Rental status is not available yet: no client bot connected.',
        'rental_status_text': '📄 <b>Rental status</b>\n\nStatus: <b>{status}</b>\nPlan: <code>{plan_type}</code>\nActive until: <code>{rent_until}</code>',
        'client_bots_empty': 'No client bots yet.',
        'client_bots_title': '🤖 <b>Client bots</b>\n\n{items}',
        'client_bot_item': '<code>{owner_user_id}</code> | <b>{status}</b> | @{bot_username} | until <code>{rent_until}</code>',
        'activate_rental_prompt_user': 'Send the client Telegram ID whose rental should be activated.',
        'activate_rental_days_prompt': 'Send the number of rental days, for example: <code>30</code>',
        'activate_rental_success': '✅ Rental activated for <b>{days}</b> day(s) for user <code>{owner_user_id}</code>.',
        'activate_rental_no_bot': 'This user has not connected a client bot yet.',
        'need_positive_days': 'A positive number of days is required.',
    },
}
for _lang, _vals in CLIENT_BOT_EXTRA.items():
    TRANSLATIONS.setdefault(_lang, {}).update(_vals)

ROLE_LAYOUTS['user'] = [['btn_menu', 'btn_help'], ['btn_new_ad', 'btn_my_orders'], ['btn_my_bot', 'btn_connect_bot'], ['btn_rental_status', 'btn_pay_stars'], ['btn_my_ref', 'btn_language'], ['btn_tariffs', 'btn_news'], ['btn_schedule']]
ROLE_LAYOUTS['moderator'] = [['btn_menu', 'btn_help'], ['btn_channels', 'btn_upload_media'], ['btn_preview', 'btn_queue_now'], ['btn_my_bot', 'btn_connect_bot'], ['btn_rental_status', 'btn_pay_stars'], ['btn_chat_id', 'btn_language'], ['btn_tariffs', 'btn_news'], ['btn_schedule']]
ROLE_LAYOUTS['admin'] = [['btn_menu', 'btn_help'], ['btn_set_upper', 'btn_set_middle', 'btn_set_bottom'], ['btn_preview', 'btn_upload_media'], ['btn_chat_id', 'btn_channels'], ['btn_staff', 'btn_schedule'], ['btn_queue_now', 'btn_delete_my_posts'], ['btn_my_bot', 'btn_connect_bot'], ['btn_rental_status', 'btn_pay_stars'], ['btn_client_bots', 'btn_language'], ['btn_autopost_on', 'btn_autopost_off'], ['btn_stats', 'btn_webpanel'], ['btn_tariffs', 'btn_news']]
ROLE_LAYOUTS['owner'] = ROLE_LAYOUTS['admin']

SERVICE_ROLE_LAYOUTS = ROLE_LAYOUTS

TENANT_ROLE_LAYOUTS = {
    'user': [['btn_menu', 'btn_help'], ['btn_new_ad', 'btn_my_orders'], ['btn_language'], ['btn_tariffs', 'btn_news'], ['btn_schedule']],
    'moderator': [['btn_menu', 'btn_help'], ['btn_channels', 'btn_upload_media'], ['btn_preview', 'btn_queue_now'], ['btn_chat_id', 'btn_language'], ['btn_tariffs', 'btn_news'], ['btn_schedule']],
    'admin': [['btn_menu', 'btn_help'], ['btn_set_upper', 'btn_set_middle', 'btn_set_bottom'], ['btn_preview', 'btn_upload_media'], ['btn_chat_id', 'btn_channels'], ['btn_staff', 'btn_schedule'], ['btn_queue_now', 'btn_delete_my_posts'], ['btn_autopost_on', 'btn_autopost_off'], ['btn_stats'], ['btn_tariffs', 'btn_news'], ['btn_language']],
    'owner': [['btn_menu', 'btn_help'], ['btn_set_upper', 'btn_set_middle', 'btn_set_bottom'], ['btn_preview', 'btn_upload_media'], ['btn_chat_id', 'btn_channels'], ['btn_staff', 'btn_schedule'], ['btn_queue_now', 'btn_delete_my_posts'], ['btn_autopost_on', 'btn_autopost_off'], ['btn_stats'], ['btn_tariffs', 'btn_news'], ['btn_language']],
}


CLIENT_BOT_MENU_EXTRA = {
    'uk': {
        'client_bots_manage_title': '🤖 <b>Клієнтські боти</b>\n\nОберіть дію.',
        'btn_client_bot_activate': '✅ Активувати',
        'btn_client_bot_deactivate': '⛔ Деактивувати',
        'btn_client_bot_refresh': '🔄 Оновити список',
        'btn_duration_30': '30 дн.',
        'btn_duration_60': '60 дн.',
        'btn_duration_90': '90 дн.',
        'btn_duration_180': '180 дн.',
        'enter_client_owner_id': 'Надішліть Telegram ID власника клієнтського бота.',
        'client_bot_duration_choose': 'Оберіть строк активації для <code>{owner_user_id}</code>.',
        'client_bot_not_found': 'Клієнтський бот для цього користувача не знайдено.',
        'client_bot_activated': '✅ Бот @{bot_username} активовано на <b>{days}</b> дн.\nВласник: <code>{owner_user_id}</code>',
        'client_bot_paused': '⛔ Бот @{bot_username} деактивовано.\nВласник: <code>{owner_user_id}</code>',
        'tenant_owner_welcome': 'Ви керуєте власним ботом як адміністратор. Тут ваші шаблони, канали, медіа, графік і черга публікацій.',
        'tenant_user_welcome': 'Це бот клієнта. Тут можна створювати заявки та працювати з контентом цього бота.',
    },
    'ru': {
        'client_bots_manage_title': '🤖 <b>Клиентские боты</b>\n\nВыберите действие.',
        'btn_client_bot_activate': '✅ Активировать',
        'btn_client_bot_deactivate': '⛔ Деактивировать',
        'btn_client_bot_refresh': '🔄 Обновить список',
        'btn_duration_30': '30 дн.',
        'btn_duration_60': '60 дн.',
        'btn_duration_90': '90 дн.',
        'btn_duration_180': '180 дн.',
        'enter_client_owner_id': 'Отправьте Telegram ID владельца клиентского бота.',
        'client_bot_duration_choose': 'Выберите срок активации для <code>{owner_user_id}</code>.',
        'client_bot_not_found': 'Клиентский бот для этого пользователя не найден.',
        'client_bot_activated': '✅ Бот @{bot_username} активирован на <b>{days}</b> дн.\nВладелец: <code>{owner_user_id}</code>',
        'client_bot_paused': '⛔ Бот @{bot_username} деактивирован.\nВладелец: <code>{owner_user_id}</code>',
        'tenant_owner_welcome': 'Вы управляете своим ботом как администратор. Здесь ваши шаблоны, каналы, медиа, график и очередь публикаций.',
        'tenant_user_welcome': 'Это клиентский бот. Здесь можно создавать заявки и работать с контентом этого бота.',
    },
    'en': {
        'client_bots_manage_title': '🤖 <b>Client bots</b>\n\nChoose an action.',
        'btn_client_bot_activate': '✅ Activate',
        'btn_client_bot_deactivate': '⛔ Deactivate',
        'btn_client_bot_refresh': '🔄 Refresh list',
        'btn_duration_30': '30 days',
        'btn_duration_60': '60 days',
        'btn_duration_90': '90 days',
        'btn_duration_180': '180 days',
        'enter_client_owner_id': 'Send the Telegram ID of the client bot owner.',
        'client_bot_duration_choose': 'Choose the activation term for <code>{owner_user_id}</code>.',
        'client_bot_not_found': 'Client bot not found for this user.',
        'client_bot_activated': '✅ Bot @{bot_username} activated for <b>{days}</b> day(s).\nOwner: <code>{owner_user_id}</code>',
        'client_bot_paused': '⛔ Bot @{bot_username} deactivated.\nOwner: <code>{owner_user_id}</code>',
        'tenant_owner_welcome': 'You manage your own bot as an administrator. Your templates, channels, media, schedule and queue live here.',
        'tenant_user_welcome': 'This is a client bot. You can create requests and work with this bot content here.',
    },
}
for _lang, _vals in CLIENT_BOT_MENU_EXTRA.items():
    TRANSLATIONS.setdefault(_lang, {}).update(_vals)


CONNECT_OWNER_EXTRA = {
    'uk': {
        'connect_bot_owner_prompt': 'Надішліть Telegram ID клієнта, для якого потрібно підключити токен бота.',
        'connect_bot_prompt_for_owner': 'Надішліть токен бота для клієнта <code>{owner_user_id}</code>.',
        'connect_bot_success_for_owner': '✅ Бота підключено для клієнта <code>{owner_user_id}</code>.\n\nІмʼя: <b>{bot_name}</b>\nUsername: @{bot_username}\nBot ID: <code>{bot_id}</code>\nСтатус: <b>{status}</b>',
    },
    'ru': {
        'connect_bot_owner_prompt': 'Отправьте Telegram ID клиента, для которого нужно подключить токен бота.',
        'connect_bot_prompt_for_owner': 'Отправьте токен бота для клиента <code>{owner_user_id}</code>.',
        'connect_bot_success_for_owner': '✅ Бот подключён для клиента <code>{owner_user_id}</code>.\n\nИмя: <b>{bot_name}</b>\nUsername: @{bot_username}\nBot ID: <code>{bot_id}</code>\nСтатус: <b>{status}</b>',
    },
    'en': {
        'connect_bot_owner_prompt': 'Send the client Telegram ID for whom the bot token should be connected.',
        'connect_bot_prompt_for_owner': 'Send the bot token for client <code>{owner_user_id}</code>.',
        'connect_bot_success_for_owner': '✅ Bot connected for client <code>{owner_user_id}</code>.\n\nName: <b>{bot_name}</b>\nUsername: @{bot_username}\nBot ID: <code>{bot_id}</code>\nStatus: <b>{status}</b>',
    },
}
for _lang, _vals in CONNECT_OWNER_EXTRA.items():
    TRANSLATIONS.setdefault(_lang, {}).update(_vals)



STARS_EXTRA = {
    'uk': {
        'btn_pay_stars': '⭐ Оплатити в Stars',
        'stars_disabled': 'Оплата в Telegram Stars зараз вимкнена.',
        'stars_need_connected_bot': 'Спочатку підключіть токен вашого бота через кнопку «🔑 Підключити токен».',
        'stars_intro': (
            '⭐ <b>Оплата оренди в Telegram Stars</b>\n\n'
            'Ваш бот: @{bot_username}\n\n'
            'Оберіть строк оренди:\n'
            '• 30 дн. — <b>{price_30} XTR</b>\n'
            '• 60 дн. — <b>{price_60} XTR</b>\n'
            '• 90 дн. — <b>{price_90} XTR</b>\n'
            '• 180 дн. — <b>{price_180} XTR</b>\n\n'
            'Після успішної оплати оренда активується автоматично.'
        ),
        'stars_plan_button': '{days} дн. — {amount} XTR',
        'stars_invoice_title': 'Оренда бота на {days} дн.',
        'stars_invoice_description': 'Активація оренди для @{bot_username} на {days} днів.',
        'stars_invoice_failed': 'Не вдалося створити інвойс: <code>{error}</code>',
        'stars_unknown_plan': 'Невідомий тариф.',
        'stars_precheckout_denied': 'Не вдалося перевірити оплату. Спробуйте ще раз.',
        'stars_payment_success': (
            '✅ Оплату отримано: <b>{amount} XTR</b>\n'
            'Оренду активовано на <b>{days}</b> дн. для @{bot_username}.\n'
            'Активно до: <code>{rent_until}</code>'
        ),
        'stars_payment_owner_mismatch': 'Цей платіж прив’язаний до іншого користувача.',
        'stars_payment_already_processed': 'Цей платіж уже оброблено.',
        'pay_support_text': 'Підтримка з питань оплати: {support_text}',
    },
    'ru': {
        'btn_pay_stars': '⭐ Оплатить в Stars',
        'stars_disabled': 'Оплата в Telegram Stars сейчас выключена.',
        'stars_need_connected_bot': 'Сначала подключите токен вашего бота через кнопку «🔑 Подключить токен».',
        'stars_intro': (
            '⭐ <b>Оплата аренды в Telegram Stars</b>\n\n'
            'Ваш бот: @{bot_username}\n\n'
            'Выберите срок аренды:\n'
            '• 30 дн. — <b>{price_30} XTR</b>\n'
            '• 60 дн. — <b>{price_60} XTR</b>\n'
            '• 90 дн. — <b>{price_90} XTR</b>\n'
            '• 180 дн. — <b>{price_180} XTR</b>\n\n'
            'После успешной оплаты аренда активируется автоматически.'
        ),
        'stars_plan_button': '{days} дн. — {amount} XTR',
        'stars_invoice_title': 'Аренда бота на {days} дн.',
        'stars_invoice_description': 'Активация аренды для @{bot_username} на {days} дней.',
        'stars_invoice_failed': 'Не удалось создать инвойс: <code>{error}</code>',
        'stars_unknown_plan': 'Неизвестный тариф.',
        'stars_precheckout_denied': 'Не удалось проверить оплату. Попробуйте ещё раз.',
        'stars_payment_success': (
            '✅ Оплата получена: <b>{amount} XTR</b>\n'
            'Аренда активирована на <b>{days}</b> дн. для @{bot_username}.\n'
            'Активно до: <code>{rent_until}</code>'
        ),
        'stars_payment_owner_mismatch': 'Этот платеж привязан к другому пользователю.',
        'stars_payment_already_processed': 'Этот платеж уже обработан.',
        'pay_support_text': 'Поддержка по оплате: {support_text}',
    },
    'en': {
        'btn_pay_stars': '⭐ Pay with Stars',
        'stars_disabled': 'Telegram Stars payments are currently disabled.',
        'stars_need_connected_bot': 'Connect your bot token first using the “🔑 Connect token” button.',
        'stars_intro': (
            '⭐ <b>Pay rental in Telegram Stars</b>\n\n'
            'Your bot: @{bot_username}\n\n'
            'Choose rental term:\n'
            '• 30 days — <b>{price_30} XTR</b>\n'
            '• 60 days — <b>{price_60} XTR</b>\n'
            '• 90 days — <b>{price_90} XTR</b>\n'
            '• 180 days — <b>{price_180} XTR</b>\n\n'
            'After successful payment the rental will be activated automatically.'
        ),
        'stars_plan_button': '{days} days — {amount} XTR',
        'stars_invoice_title': 'Bot rental for {days} days',
        'stars_invoice_description': 'Activate rental for @{bot_username} for {days} days.',
        'stars_invoice_failed': 'Could not create invoice: <code>{error}</code>',
        'stars_unknown_plan': 'Unknown plan.',
        'stars_precheckout_denied': 'Payment verification failed. Please try again.',
        'stars_payment_success': (
            '✅ Payment received: <b>{amount} XTR</b>\n'
            'Rental activated for <b>{days}</b> day(s) for @{bot_username}.\n'
            'Active until: <code>{rent_until}</code>'
        ),
        'stars_payment_owner_mismatch': 'This payment belongs to another user.',
        'stars_payment_already_processed': 'This payment has already been processed.',
        'pay_support_text': 'Payment support: {support_text}',
    },
}
for _lang, _vals in STARS_EXTRA.items():
    TRANSLATIONS.setdefault(_lang, {}).update(_vals)

