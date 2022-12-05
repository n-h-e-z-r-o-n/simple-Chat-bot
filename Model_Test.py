import chatbot_functions_library as Chat_Bot

while True:
    message = input("User :")
    ints = Chat_Bot.predict_class(message)
    res = Chat_Bot.get_response(ints)
    print("Bot :", res)
    #print(ints)

