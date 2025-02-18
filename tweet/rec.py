import cv2
import pandas as pd
from ultralytics import YOLO
from paddleocr import PaddleOCR
from datetime import datetime
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PlateRecognition:
    def __init__(self, model_path='tweet/best.pt', class_file='tweet/coco1.txt'):
        # Load the YOLO model
        self.model = YOLO(model_path)

        # Load class names
        with open(class_file, "r") as f:
            self.class_list = f.read().split("\n")

        # Initialize PaddleOCR
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

    def recognize_text(self, crop):
        # Convert to grayscale for better OCR performance
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        # Optional preprocessing (can be fine-tuned based on your images)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # Perform OCR
        result = self.ocr.ocr(gray, cls=True)

        # Handle cases where OCR doesn't find any text
        if not result or not result[0]:
            logging.warning("No text detected by OCR.")
            return ""

        # Extract text from the result
        text = "".join([line[1][0] for line in result[0]]).strip()

        # Clean up the detected text
        text = text.replace("IND", "").strip()
        return text

    def process_frame(self, frame, processed_numbers):
        frame = cv2.resize(frame, (1020, 500))
        results = self.model.predict(frame)
        boxes = results[0].boxes.data if results and hasattr(results[0].boxes, 'data') else None

        if boxes is None or boxes.numel() == 0:  # Check if tensor is empty
            logging.warning("No objects detected in the frame.")
            return []

        px = pd.DataFrame(boxes.cpu().numpy()).astype("float")  # Convert to DataFrame for processing

        detected_data = []

        for _, row in px.iterrows():
            x1, y1, x2, y2 = map(int, row[:4])
            d = int(row[5])
            c = self.class_list[d]

            # Crop the detected object
            crop = frame[y1:y2, x1:x2]

            # Display the cropped plate image
            cv2.imshow('Cropped Plate Image', crop)

            text = self.recognize_text(crop)
            logging.info(f"Detected Text: {text}")

            # Avoid duplicate entries
            if text and text not in processed_numbers:
                processed_numbers.add(text)
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                detected_data.append((text, current_datetime))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("RGB", frame)
        return detected_data

    def process_input_file(self, input_file):
        is_image = input_file.lower().endswith((".jpg", ".jpeg", ".png"))
        processed_numbers = set()
        all_detected_data = []

        if is_image:
            # Process the image
            frame = cv2.imread(input_file)
            if frame is None:
                logging.error("Error: Unable to read the image file.")
                return []
            detected_data = self.process_frame(frame, processed_numbers)
            all_detected_data.extend(detected_data)
            cv2.waitKey(0)  # Wait for key press to close the image window
        else:
            # Process the video
            cap = cv2.VideoCapture(input_file)
            if not cap.isOpened():
                logging.error("Error: Unable to open video file.")
                return []

            count = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break  # Exit loop when the video ends

                count += 1
                if count % 3 != 0:  # Process every third frame to reduce computation
                    continue

                detected_data = self.process_frame(frame, processed_numbers)
                all_detected_data.extend(detected_data)

                if cv2.waitKey(1) & 0xFF == 27:  # Break on pressing 'ESC'
                    break

            cap.release()

        cv2.destroyAllWindows()
        return all_detected_data

    def save_results(self, detected_plates, output_file="tweet/car_plate_data.txt"):
        if detected_plates:
            with open(output_file, "a") as file:
                if os.stat(output_file).st_size == 0:  # Check if file is empty and write headers
                    file.write("NumberPlate\tDate\tTime\n")
                for plate, timestamp in detected_plates:
                    file.write(f"{plate}\t{timestamp}\n")
            logging.info(f"Results saved to {output_file}")


# Example usage
if __name__ == "__main__":
    input_file = "car_video1.mp4"  # Replace with your input file (.mp4 or .jpeg)
    plate_recognition = PlateRecognition()
    detected_plates = plate_recognition.process_input_file(input_file)
    plate_recognition.save_results(detected_plates)
    logging.info("Detection complete.")
