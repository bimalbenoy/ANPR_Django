from tweet.rec import PlateRecognition
import logging
def process_video_file(input_file):
    recognizer = PlateRecognition()
    result = recognizer.process_input_file(input_file)
    recognizer.save_results(result)
    logging.info("Detection complete.")

