import cv2


def detectar_rostro():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    
    frames_detectados = 0
    detectado = False

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostros = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        if len(rostros) > 0:
            frames_detectados += 1
            for (x, y, w, h) in rostros:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.imshow('Validacion Biometrica - AM Sound', frame)

        if frames_detectados > 10:
            detectado = True
            break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return detectado