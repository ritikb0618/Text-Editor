def speech_to_text():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source)
#         print("Listening...")
#         try:
#             audio = recognizer.listen(source, timeout=5)  # Set a timeout to stop listening after 5 seconds of silence
#             print("Stopped listening...")
#             recognized_text = recognizer.recognize_google(audio)
#             text_editor.insert(tk.END, recognized_text)
#         except sr.WaitTimeoutError:
#             print("No speech detected within the timeout period")
#         except sr.UnknownValueError:
#             print("Speech recognition could not understand audio")
#         except sr.RequestError as e:
#             print("Could not request results from Google Speech Recognition service; {0}".format(e))


# speech_to_text_btn.configure(command=speech_to_text)