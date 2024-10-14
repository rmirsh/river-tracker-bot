from bot.core.ui_commands import bot_commands

lexicon_ru: dict[str, str | dict] = {"/" + key: value for key, value in {
    "start": "Привет, <b>{name}</b>!\n\n"
             "Вот список моих команд:\n"
             + " - /" + "\n - /".join([f"{command.command}: {command.description}" for command in bot_commands]),

    "donate": "Дорогие друзья! 🌟\n\n"
              "Этот бот создан, чтобы приносить пользу и предупреждать людей об опасности, "
              "а также <b><i>снять тревожность у пожилых людей и владельцев гаражей вдоль рек.</i></b>\n"
              "Его разработкой занимаюсь я один, вкладывая в него много времени и усилий.\n\n"
              "Если вам нравится моя работа и вы хотите поддержать проект, вы можете сделать пожертвование "
              "любой удобной Вам суммы.\n"
              "Ваш вклад поможет мне продолжать развивать проект,"
              "а также оплачивать хостинг для бесперебойной работы бота. 🏘️\n\n"
              "Спасибо вам за вашу поддержку и доверие! 🙏"
              "Вы может пожертвовать, воспользовавшись командой /donate.",

    # TODO: Дописать
}.items()}