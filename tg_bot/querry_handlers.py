"""
Handlers for all callback queries (clicking on inline buttons)
"""
# import ast
#
# from tg_bot import (
#     bot, dict_text, db,
# )
# from tg_bot import reply_markup as rm
# from tg_bot import config


# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     user_id = call.from_user.id
#
#     call_data_list = call.data.split('_')
#
#     if call.data == 'mainmenu':
#         ...
#     elif call.data[:9] == 'countries':
#         ...
#     elif call_data_list[0] == 'cid':
#         ...
