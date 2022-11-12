from telegram import ReplyKeyboardRemove
from access import token
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


board = list(range(1,10))
CHOICE = 0


def image_board():
    global board
    field = ''
    field += f'{"-" * 17}'
    for i in range(3):
        field += f'\n| {board[0+i*3]} | {board[1+i*3]} | {board[2+i*3]} |\n'
        field += f'{"-" * 17}'
    return field


def take_input(update, _):
    win = False
    counter = 0
    while not win:
        if counter % 2 == 0:
            player_token = "X"
        else:
            player_token = "O"
        valid = False
        while not valid:
            update.message.reply_text(f'Куда поставим "{player_token}" ? ')
            player_answer = update.message.text
            try:
                player_answer = int(player_answer)
            except:
                update.message.reply_text('Некорректный ввод. Вы уверены, что ввели число?')
                continue
            if player_answer >= 1 and player_answer <= 9:
                if (str(board[player_answer-1]) not in "XO"):
                    board[player_answer-1] = player_token
                    valid = True
                else:
                    update.message.reply_text ("Эта клеточка уже занята.")
            else:
                update.message.reply_text ("Некорректный ввод. Введите число от 1 до 9 чтобы походить.")
            counter += 1
            update.message.reply_text(image_board())
            if counter > 4:
                temp = check_win(board)
                if temp:
                    update.message.reply_text (f'"{temp}" выиграл!')
                    win = True
                    return ConversationHandler.END
            if counter == 9:
                update.message.reply_text ('Ничья! Может лучше в "Глобальную термоядерную войну"?')
                return ConversationHandler.END


def check_win():
    global board
    win_coord = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    for each in win_coord:
        if board[each[0]] == board[each[1]] == board[each[2]]:
            return board[each[0]]
    return False


def start(update, _):
    update.message.reply_text ("Давай сыграем в крестики-нолики")
    update.message.reply_text (image_board())
    return CHOICE


def cancel(update, _):
    update.message.reply_text('Чао!', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

if __name__ == '__main__':
    updater = Updater(token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={CHOICE: [MessageHandler(Filters.text, take_input)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    print('start bot')

    updater.start_polling()
    updater.idle()