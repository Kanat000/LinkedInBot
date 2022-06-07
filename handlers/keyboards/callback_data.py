from aiogram.utils.callback_data import CallbackData

industry_callback = CallbackData("industry", "index")
control_callback = CallbackData("control", "status", "page_num")
pageNum_callback = CallbackData("page", "page_num")
edit_account_callback = CallbackData('edit_account', 'field')