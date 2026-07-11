from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔴 Вышел",
                    callback_data="start_break"
                ),
                InlineKeyboardButton(
                    text="🟢 Пришел",
                    callback_data="end_break"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📄 Отчет",
                    callback_data="report"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🗑 Очистить",
                    callback_data="clear"
                )
            ]
        ]
    )


def comment_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Без комментария",
                    callback_data="comment_none"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🕒 Задержка",
                    callback_data="comment_delay"
                ),
                InlineKeyboardButton(
                    text="🍽 Обед",
                    callback_data="comment_lunch"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🕒🍽 Задержка + Обед",
                    callback_data="comment_delay_lunch"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📦 Товар",
                    callback_data="comment_product"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✏️ Свой комментарий",
                    callback_data="comment_custom"
                )
            ]
        ]
    )


def confirm_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить",
                    callback_data="confirm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Изменить",
                    callback_data="change"
                ),
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data="cancel"
                )
            ]
        ]
    )


def clear_confirm_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Да",
                    callback_data="clear_yes"
                ),
                InlineKeyboardButton(
                    text="❌ Нет",
                    callback_data="clear_no"
                )
            ]
        ]
    )
