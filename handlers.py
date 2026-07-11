from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database import (
    get_user,
    add_user,
    start_break,
    get_active_break,
    finish_break,
    get_today_breaks,
    clear_breaks
)

from keyboards import (
    main_menu,
    comment_menu,
    confirm_menu,
    clear_confirm_menu
)


router = Router()


class Registration(StatesGroup):
    waiting_name = State()


class CustomComment(StatesGroup):
    waiting_comment = State()


selected_comments = {}


@router.message(F.text == "/start")
async def start_command(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)

    if not user:
        await message.answer(
            "👋 Добро пожаловать!\n\nВведите ваше имя:"
        )
        await state.set_state(Registration.waiting_name)
        return

    await message.answer(
        "📖 Журнал выходов\n\nВыберите действие:",
        reply_markup=main_menu()
    )


@router.message(Registration.waiting_name)
async def save_name(message: Message, state: FSMContext):
    await add_user(
        message.from_user.id,
        message.text
    )

    await state.clear()

    await message.answer(
        "✅ Регистрация завершена\n\n📖 Журнал выходов",
        reply_markup=main_menu()
    )


@router.callback_query(F.data == "start_break")
async def start_break_handler(callback: CallbackQuery):
    active = await get_active_break(callback.from_user.id)

    if active:
        await callback.answer(
            "❌ У вас уже есть активный выход",
            show_alert=True
        )
        return

    time = await start_break(callback.from_user.id)

    await callback.message.edit_text(
        f"🔴 Выход зафиксирован\n\n🕒 {time}",
        reply_markup=main_menu()
    )
@router.callback_query(F.data == "end_break")
async def end_break_handler(callback: CallbackQuery):
    active = await get_active_break(callback.from_user.id)

    if not active:
        await callback.answer(
            "❌ Нет активного выхода",
            show_alert=True
        )
        return

    await callback.message.edit_text(
        "Выберите комментарий:",
        reply_markup=comment_menu()
    )


@router.callback_query(F.data.startswith("comment_"))
async def choose_comment(callback: CallbackQuery):
    comments = {
        "comment_none": "",
        "comment_delay": "задержка",
        "comment_lunch": "обед",
        "comment_delay_lunch": "задержка + обед",
        "comment_product": "товар"
    }

    if callback.data == "comment_custom":
        await callback.message.edit_text(
            "✏️ Введите комментарий:"
        )

        await callback.bot.get_current().fsm.set_state(
            callback.from_user.id,
            callback.from_user.id,
            CustomComment.waiting_comment
        )

        return

    selected_comments[callback.from_user.id] = comments.get(
        callback.data,
        ""
    )

    text = selected_comments[callback.from_user.id]

    if text:
        preview = text
    else:
        preview = "без комментария"

    await callback.message.edit_text(
        f"Вы выбрали:\n\n{preview}\n\nПодтвердить?",
        reply_markup=confirm_menu()
    )


@router.callback_query(F.data == "confirm")
async def confirm_break(callback: CallbackQuery):
    comment = selected_comments.get(
        callback.from_user.id,
        ""
    )

    time = await finish_break(
        callback.from_user.id,
        comment
    )

    selected_comments.pop(
        callback.from_user.id,
        None
    )

    await callback.message.edit_text(
        f"🟢 Возвращение зафиксировано\n\n🕒 {time}",
        reply_markup=main_menu()
    )


@router.callback_query(F.data == "change")
async def change_comment(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите комментарий:",
        reply_markup=comment_menu()
    )


@router.callback_query(F.data == "cancel")
async def cancel_comment(callback: CallbackQuery):
    selected_comments.pop(
        callback.from_user.id,
        None
    )

    await callback.message.edit_text(
        "📖 Журнал выходов\n\nВыберите действие:",
        reply_markup=main_menu()
    )
@router.message(CustomComment.waiting_comment)
async def save_custom_comment(
    message: Message,
    state: FSMContext
):
    selected_comments[message.from_user.id] = message.text

    await state.clear()

    await message.answer(
        f"Вы выбрали:\n\n{message.text}\n\nПодтвердить?",
        reply_markup=confirm_menu()
    )


@router.callback_query(F.data == "report")
async def report_handler(callback: CallbackQuery):
    breaks = await get_today_breaks(
        callback.from_user.id
    )

    if not breaks:
        await callback.answer(
            "📄 За сегодня записей нет",
            show_alert=True
        )
        return

    text = "📄 Отчет за сегодня:\n\n"

    for item in breaks:
        start, end, comment = item

        line = f"{start}–{end}"

        if comment:
            line += f" {comment}"

        text += line + "\n"

    await callback.message.edit_text(
        text,
        reply_markup=main_menu()
    )


@router.callback_query(F.data == "clear")
async def clear_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Удалить все выходы за сегодня?",
        reply_markup=clear_confirm_menu()
    )


@router.callback_query(F.data == "clear_yes")
async def clear_yes_handler(callback: CallbackQuery):
    await clear_breaks(
        callback.from_user.id
    )

    await callback.message.edit_text(
        "✅ Записи очищены",
        reply_markup=main_menu()
    )


@router.callback_query(F.data == "clear_no")
async def clear_no_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "📖 Журнал выходов\n\nВыберите действие:",
        reply_markup=main_menu()
    )
