from aiogram.dispatcher.filters.state import State, StatesGroup


class TemplateStates(StatesGroup):
    waiting_upper = State()
    waiting_middle = State()
    waiting_bottom = State()


class ChannelStates(StatesGroup):
    waiting_channel = State()
    waiting_delete_one = State()


class AdOrderStates(StatesGroup):
    waiting_text = State()
    waiting_category = State()


class AdminStates(StatesGroup):
    waiting_role_user_id = State()
    waiting_role_name = State()
    waiting_add_staff_user_id = State()
    waiting_add_staff_role = State()
    waiting_remove_staff_user_id = State()


class ScheduleStates(StatesGroup):
    waiting_post_time = State()
    waiting_delete_time = State()



class ClientBotStates(StatesGroup):
    waiting_connect_owner_id = State()
    waiting_bot_token = State()
    waiting_activate_owner_id = State()
    waiting_activate_days = State()
    waiting_deactivate_owner_id = State()
