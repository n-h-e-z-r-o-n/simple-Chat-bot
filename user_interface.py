# ============================= Libraries ==============================================================================================================
import tkinter as tk
import chatbot_functions_library as Chat_Bot
from PIL import ImageTk,Image
from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3
import time

# ============================== Variables ==============================================================================================================
background_color = 'black' # User Interface Background Color
bot_responses = [] # Bot responses list
user_query = [] # User Query list
Conver_widget = [] # Keep Track Of the chat widget
Full_Conversation = [] # Full Conversation list
k_u = 0  # Keep Track Of User query
k_b = 0 # Keep Track Of Bot Response
i = 0.01 # Keep Track Of the Widget
blink_c = 0 # Keep Track of Color chang

# ================================= Functions ============================================================================================================
def color_flashing(widget): # Color Flush
    global blink_c
    if blink_c == 0:
        widget.config(fg = 'red')
        blink_c = 1
    else:
        widget.config(fg='green')
        blink_c = 0
    root.after(1000, lambda: color_flashing(widget))

def chat(message):  # chat Bot function
        statistics = Chat_Bot.predict_class(message)
        bot_response =  Chat_Bot.get_response(statistics)
        print(bot_response)
        return bot_response

def UserQuery(question): # Get User query and Bot Response
            User_Query_Entry.set('')
            print(question)
            bot_r = chat(question)
            bot_responses.append(bot_r)
            user_query.append(question)
            Full_Conversation.append(question)
            Full_Conversation.append(bot_r)
            display_conversation()


def clear_display(): # Clear chat display automatically
            global Conver_widget
            global bot_responses
            global user_query
            for i in range(len(Conver_widget)):
                  Conver_widget[i].destroy()
                  bot_responses.clear()
                  user_query.clear()


def display_conversation(): # display chat conversation
        global i, k_u, k_b
        global bot_responses
        global user_query
        global Conver_widget
        print(i)
        if i > 0.8:
            i = 0.01
            k_u = 0
            k_b = 0
            clear_display()
        while k_u < len(user_query) or k_b < len(bot_responses):
            height = 0.06
            if len(user_query) != k_u:
                        if 75 < len(user_query[k_u]) < 150:
                            height = 0.06 * 2
                        if 150 < len(user_query[k_u]) < 225:
                            height = 0.06 * 3
                        # tk.Button(show_v, text=f'USER: {len(user_query[k])}', anchor='e').place(relwidth=0.7,relheight=height, relx=0.295, rely=i)
                        u = tk.Text(show_v, height=5, width=52, wrap=tk.WORD, fg='green',bg=background_color,font='-family {Georgia} -size 10 -weight bold',borderwidth=0, border=0 )
                        u.place(relwidth=0.7, relheight=height, relx=0.295, rely=i)
                        u.tag_configure('tag-right', justify='right')
                        u.insert(tk.END, user_query[k_u], 'tag-right')
                        u['state'] = 'disabled'
                        Conver_widget.append(u)
                        i = i + height
                        k_u += 1
            height = 0.06
            if len(bot_responses) != k_b:
                        if 75 < len(bot_responses[k_b]) < 150:
                            height = 0.06 * 2
                        if 150 < len(bot_responses[k_b]) < 225:
                            height = 0.06 * 3
                        # tk.Button(show_v, text=f"{len(bot_response)}", anchor='w' ).place(relwidth=0.7,relheight=height, relx=0.01, rely=i)
                        T = tk.Text(show_v, height=5, width=52, wrap=tk.WORD, fg='red', bg=background_color,font='-family {Georgia} -size 10 -weight bold', borderwidth=0, border=0)
                        T.place(relwidth=0.7, relheight=height, relx=0.01, rely=i)
                        T.insert(tk.END, bot_responses[k_b])
                        T['state'] = 'disabled'
                        Conver_widget.append(T)
                        i = i + height
                        k_b += 1

def view_chat():  # Save Full Chat in Pdf Format
    global Full_Conversation
    k = 0
    import webbrowser
    from fpdf import FPDF
    class PDF(FPDF):
        pass

    pdf = PDF('P', 'mm')  # pdf object
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font('helvetica', '', 16)
    pdf.cell(0, 10, 'Chat Bot Conversation', ln=True, align='C')
    pdf.ln(15)  # line break
    pdf.page_no()
    pdf.set_font('helvetica', 'UB', 16)
    pdf.cell(90, 10, ' o o o ', align='R', ln=True)
    while k < len(Full_Conversation)-1:
        pdf.set_font('times', 'B', 10)
        pdf.cell(195, 10, f'User  : {Full_Conversation[k]}', align='L', border=1, ln=True)
        pdf.cell(195, 10, f'Bot  : {Full_Conversation[k+1]}', align='L', border=1, ln=True)
        k = k + 1

    pdf_file_name = f'Chat_Conversation.pdf'
    pdf.output(pdf_file_name)
    webbrowser.get('windows-default').open(pdf_file_name)

def resize(file_location):
    img = (Image.open(file_location))
    Resized_image = img.resize((200, 200), Image.ANTIALIAS)
    new_image = ImageTk.PhotoImage(Resized_image)
    return new_image


Frame_Rate = 16000
Channels = 1
Speech_Model = Model(r"C:\Users\HEZRON WEKESA\Desktop\AI group project\Speech Recognition\speech_to_text_model\vosk-model-small-en-us-0.15") #
recognizer = KaldiRecognizer(Speech_Model, Frame_Rate) # PASS MODEL AND FREQUENCY 16000
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=Channels, rate=Frame_Rate, input=True, frames_per_buffer=8192)
stream.start_stream()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def changeOnHover(button, colorOnHover, colorOnLeave): # Color change on Mouse Hover
    button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))
    button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))

def speak(say = 'Yes, am listening'): # Text to Speach Function
    engine.say(say)
    engine.runAndWait()

def voice_chat(): # voice chat bot
    Chat_Bot_Status.config(text='Listening')
    speak('Hello, How May I help you. Any Time You Need Me, just call My Name')

    """
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            if 'purity' in text[14:-3]:
                speak()

                time.sleep(1)
                while True:
                    data = stream.read(4096, exception_on_overflow=False)
                    if recognizer.AcceptWaveform(data):
                        text = recognizer.Result()
                        if text[14:-3] != '':
                            print(text[14:-3])
                            chat(text[14:-3])
                        time.sleep(2)
        """

# ======================================================== User Interface ============================================================================================

root = tk.Tk()  # UI
root.title("CHAT BOT")
root.minsize(900, 850)
root.maxsize(901, 851)
root.config(bg=background_color)

frame_img1 = tk.Label(root, bg=background_color)
frame_img1.place(height=200, width=200, rely=0.02, relx=0.2 )
new_image1 = resize('Assets/bot_icon.png')
frame_img1.config(image=new_image1)


frame_img2 = tk.Label(root, bg=background_color)
frame_img2.place(height=200, width=200, rely=0.02, relx=0.6 )
new_image2 = resize('Assets/bot_icon.png')
frame_img2.config(image=new_image2)


speaker_button = tk.Button(root, bg=background_color, activebackground='green', borderwidth=0,  command=voice_chat)
speaker_button.place(height=50, width=50, rely=0.02, relx=0.94)
img = (Image.open('Assets/speaker.png'))
speaker_image = img.resize((50, 50), Image.ANTIALIAS)
speaker_image = ImageTk.PhotoImage(speaker_image)
speaker_button.config(image=speaker_image)


Chat_Bot_Status = tk.Label(root, bg=background_color, text="Chat Mode", font='-family {Georgia} -size 10 -weight bold')
Chat_Bot_Status.place(height=50, width=200, rely=0.26, relx=0.4 )
root.after(1000, lambda :color_flashing(Chat_Bot_Status))


frame1 = tk.Frame(root, bg=background_color)
frame1.place(relheight=0.6, relwidth=0.77, rely=0.39, relx=0.1 )

show_v = tk.Frame(frame1, bg=background_color)
show_v.place(relheight=0.9, relwidth=0.94, relx=0.03, rely=0.01)


User_Query_Entry = tk.StringVar()
user_Query_entry = tk.Entry(frame1, bg='#FAF4D4',font='-family {Courier New} -size 12 -weight bold', borderwidth=1, textvariable=User_Query_Entry)
user_Query_entry.place(relwidth=0.85, relheight=0.06, rely=0.93, relx=0.05)
changeOnHover(user_Query_entry, '#FAF4D4', 'white')

E_Button = tk.Button(frame1, borderwidth=0, text='➤', bg='gray', font='-size 24 ', command= lambda: UserQuery(User_Query_Entry.get()) )
E_Button.place(relwidth=0.064, relheight=0.06, rely=0.93, relx=0.905)
changeOnHover(E_Button, '#FAF4D4', 'gray')

Pdf_Button = tk.Button(root, borderwidth=0, text='View\nChat',bg = background_color, activebackground=background_color, activeforeground='green', fg='yellow', font='-family {Courier New} -size 12', command=view_chat)
Pdf_Button.place(relwidth=0.074, relheight=0.07, rely=0.92, relx=0.905)


root.mainloop()
# =================================== End =======================================================================================================================================