"""In this phase it loads emotion recognition model from a file,
shows a webcam image, recognizes face, and it's emotion and draw emotion on the image.
"""

import cv2
from face_detect import find_faces
from image_commons import nparray_as_image, draw_with_alpha


def _load_emoticons(emotions):
    """
    Loads emotions images from graphics folder.
    - emotions: Array of emotions names.
     Array of emotions graphics is returned
    """
    return [nparray_as_image(cv2.imread('graphics/%s.png' % emotion, -1), mode=None) for emotion in emotions]


def show_webcam_and_run(model, emoticons, window_size=None, window_name='webcam', update_time=10):
    """
    Shows webcam image, detects faces and its emotions in real time and draw emoticons over those faces.
    - model: Learnt emotion detection model.
    - emoticons: List of emotions images.
    - window_size: Size of webcam image window.
    - window_name: Name of webcam image window.
    - update_time: Image update time interval.
    """
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    if window_size:
        width, height = window_size
        cv2.resizeWindow(window_name, width, height)

    vc = cv2.VideoCapture(0)
    if vc.isOpened():
        read_value, webcam_image = vc.read()
    else:
        print("webcam not found")
        return

    while read_value:
        for normalized_face, (x, y, w, h) in find_faces(webcam_image):
            normalized_face = cv2.resize(normalized_face, (1000, 1000), fx=5.5, fy=5.5,
                                         interpolation=cv2.INTER_LINEAR)
            prediction = model.predict(normalized_face)  # predict the facial expression
            prediction = prediction[0]

            image_to_draw = emoticons[prediction]
            draw_with_alpha(webcam_image, image_to_draw, (x, y, w, h))

        cv2.imshow(window_name, webcam_image)
        read_value, webcam_image = vc.read()
        key = cv2.waitKey(update_time)

        if key == 27:  # ESC to quit
            break

    cv2.destroyWindow(window_name)



if __name__ == '__main__':
    emotions = ['neutral', 'anger', 'disgust', 'happy', 'sadness', 'fear', 'surprise']
    emoticons = _load_emoticons(emotions)

    # load model
    fisher_face = cv2.face.FisherFaceRecognizer_create()
    fisher_face.read('models/emotion_detection_model.xml')

    # use learnt model
    window_name = 'WEBCAM (press ESC to exit)'
    show_webcam_and_run(fisher_face, emoticons, window_size=(1000, 1000), window_name=window_name, update_time=8)
