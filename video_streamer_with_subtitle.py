import cv2

def stream_from_camera():
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from camera.")
            break

        cv2.imshow('Camera Stream', frame)

        # Press 'q' to exit the camera stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def stream_from_file(file_path):
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Reached end of video or error occurred.")
            break

        cv2.imshow('Video File Stream', frame)

        # Press 'q' to exit the video file stream
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    print("Select streaming option:")
    print("1. Stream from Camera")
    print("2. Stream from Video File")

    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        stream_from_camera()
    elif choice == '2':
        file_path = input("Enter the path to the video file: ")
        stream_from_file(file_path)
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
