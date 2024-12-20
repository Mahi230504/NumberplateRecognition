import cv2
import pytesseract

# Configure Tesseract executable path if necessary
# Uncomment the following line if tesseract isn't in PATH
# pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"

def preprocess_image(image):
    """Preprocess the image for better OCR."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Binarize
    return thresh

def detect_number_plate(image):
    """Detect number plate region and extract text."""
    # Preprocess image
    preprocessed = preprocess_image(image)

    # Use pytesseract to extract text
    text = pytesseract.image_to_string(preprocessed, config="--psm 8")  # PSM 8 assumes a single word (ideal for plates)
    return text

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

            # Extract text from the image
            print("Processing image to extract number plate text...")
            text = detect_number_plate(frame)
            print(f"Extracted Text: {text}")
            break
        elif key == ord('q'):
            print("Exiting without capturing.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_process_image()
