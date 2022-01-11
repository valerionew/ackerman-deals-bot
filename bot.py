
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import logging
import secrets

"""
BotFather commands:

start - Starts the bot
buy - Sets Ackerman scheme to buy
sell - Sets Ackerman scheme to sell
"""

class AckermanBot:
    def __init__(self):
        """Start the bot."""
        self._values = {"buy": [65, 85, 95, 100], "sell": [135, 115, 105, 100]}
        # Create the Updater and pass it your bot's token.
        self._updater = Updater(secrets.TOKEN)

        # Get the dispatcher to register handlers
        self._dispatcher = self._updater.dispatcher

        # on different commands - answer in Telegram
        self._dispatcher.add_handler(CommandHandler("start", self._startCommand))
        self._dispatcher.add_handler(CommandHandler("help", self._helpCommand))
        self._dispatcher.add_handler(CommandHandler("buy", self._buyCommand))
        self._dispatcher.add_handler(CommandHandler("sell", self._sellCommand))
        # error handler function
        self._dispatcher.add_error_handler(self._errorHandler)

        # on non command i.e message - echo the message on Telegram
        self._dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self._replyCommand))

    def start(self):
        logging.info("Bot started")
        # Start the Bot
        self._updater.start_polling()
        # init the user to buy mode

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self._updater.idle()

    def _formatMessage(self, val: float, mode: int = 0) -> str:
        # sadly, I had to partially un fuck this function
        # source values
        computed = [str(round(float (val * v / 100), 2)).replace(".", "\.") for v in self._values[mode]]
        return (
            f"_*Ackerman deal {mode} scheme*_: \n\n" +
            "\n".join(f"_*{self._values[mode][x]}*_%: {computed[x]}" for x in range(len(computed)))
            )

    def _errorHandler(self, update: Update, context: CallbackContext) -> None:
        logging.error(f"Update {update} caused error {context.error}")

    def _setMode(self, context: CallbackContext, mode: str) -> str:
        """Set Ackerman scheme mode and returns formatted message"""
        if mode not in self._values:
            raise ValueError

        context.user_data["mode"] = mode
        return f"*_Bot is now in {mode} mode_*"

    def _startCommand(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        update.message.reply_markdown_v2(
            'Hi {user.mention_markdown_v2()}\! Send me a number to create your _*Ackerman deal scheme*_\!',
        )
        # udpdate current version
        context.user_data["mode"] = "buy"


    def _helpCommand(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /help is issued."""
        update.message.reply_markdown_v2('Send me a number to create your _*Ackerman deal scheme*_!')


    def _replyCommand(self, update: Update, context: CallbackContext) -> None:
        """Send the message"""
        mode = context.user_data.get("mode", "buy")
        try:
            num = float(update.message.text)
        except ValueError:
            update.message.reply_text("I'd need a number, not a string")
        else:
        # lorenzo took a bit of pride in this
            update.message.reply_markdown_v2(
                self._formatMessage(num, mode=mode),
                reply_to_message_id=update.message.message_id
            )

    def _buyCommand(self, update: Update, context: CallbackContext) -> None:
        """Set Ackerman scheme to buy"""
        message = self._setMode(context, "buy")
        update.message.reply_markdown_v2(message)

    def _sellCommand(self, update: Update, context: CallbackContext) -> None:
        """Set Ackerman scheme to buy"""
        message = self._setMode(context, "sell")
        update.message.reply_markdown_v2(message)
