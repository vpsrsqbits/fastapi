import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

audio_file_path = "fHb_WalkThrough_audio.wav"
transcript_file_path = "./fHb_WalkThrough_text.txt"
# Transcribe the extracted audio to text
with sr.AudioFile(audio_file_path) as source:
    audio_data = recognizer.record(source)
    try:
        transcript = recognizer.recognize_google(audio_data)
        # Save the transcript to a text file
        with open(transcript_file_path, 'w') as file:
            file.write(transcript)
        transcript_success = True
    except Exception as e:
        transcript = str(e)
        transcript_success = False

transcript_success, transcript_file_path
