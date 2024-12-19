import cv2
import easyocr

def preprocess_image(image):
    """Preprocess the image for better OCR."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    return gray

def detect_number_plate(image):
    """Detect number plate text using EasyOCR."""
    reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader for English
    results = reader.readtext(image)

    # Extract text
    plate_text = " ".join([res[1] for res in results])
    return plate_text

def capture_and_process_image():
    print("Initializing camera...")

    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

    if not cap.isOpened():
        print("Error: Unable to access the camera")
        return

    print("Press 'c' to capture an image and extract number plate text or 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from the camera")
            break

        cv2.imshow("Camera Feed", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            image_path = "captured_image.jpg"
            cv2.imwrite(image_path, frame)
            print(f"Image saved as {image_path}")

            # Preprocess image and extract text
            print("Processing image to extract number plate text...")
            preprocessed_image = preprocess_image(frame)
            text = detect_number_plate(preprocessed_image)
            print(f"Extracted Text: {text}")
            break
        elif key == ord('q'):
            print("Exiting without capturing.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_process_image()
