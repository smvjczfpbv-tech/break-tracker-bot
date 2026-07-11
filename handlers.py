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
