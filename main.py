import sys
from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QFileDialog 
from PySide6.QtGui import QPixmap, QPalette, QColor, QImage
from ui_mainwindow import Ui_MainWindow
import tensorflow as tf
import os
import cv2
import numpy as np


class ImageRecognitionApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Conectar botones a funciones
        self.load_image_button.clicked.connect(self.load_image)
        self.recognize_button.clicked.connect(self.recognize)

        # Inicializar variables
        self.image_path = None
        self.image_scene = QGraphicsScene()
        self.image_view.setScene(self.image_scene)

        # Cargar el modelo de TensorFlow
        model_path = os.path.join("PixelDetect\ssd_mobilenet_v2_320x320_coco17_tpu-8\saved_model")
        self.model = tf.saved_model.load(model_path)
        self.categories = ["background", "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Cargar Imagen", "", "Archivos de Imagen (*.png *.jpg *.jpeg *.bmp);;Todos los Archivos (*)", options=options)
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(self.image_path)
            self.image_scene.clear()
            self.image_scene.addItem(QGraphicsPixmapItem(pixmap))
            self.image_view.fitInView(self.image_scene, Qt.IgnoreAspectRatio)  # Modificado aquí

    def recognize(self):
        if self.image_path:
            recognition_type = self.recognition_type.currentText()

            # Leer la imagen utilizando OpenCV
            image = cv2.imread(self.image_path)

            # Convertir la imagen de BGR a RGB (OpenCV utiliza BGR, TensorFlow espera RGB)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Convertir la imagen a un tensor
            input_tensor = tf.convert_to_tensor(image_rgb)

            # Agregar una dimensión extra ya que el modelo espera un lote de imágenes
            input_tensor = input_tensor[tf.newaxis, ...]

            # Reconocimiento de Objetos
            if recognition_type == "Objetos":
                # Obtener las detecciones del modelo
                detections = self.model(input_tensor)

                # Convertir las detecciones a arrays de NumPy
                num_detections = int(detections.pop("num_detections"))
                detections = {key: value[0, :num_detections].numpy() 
                              for key, value in detections.items()}
                detections["num_detections"] = num_detections

                # Obtener las categorías y los puntajes de confianza de las detecciones
                categories = detections["detection_classes"].astype(np.int32)
                scores = detections["detection_scores"]

                # Filtrar detecciones con puntajes de confianza mayores a un umbral
                threshold = 0.5
                filtered_categories = categories[scores > threshold]

                # Obtener los nombres de las categorías detectadas
                detected_labels = [self.categories[i] for i in filtered_categories]

                # Mostrar los resultados en el QTextEdit
                self.results_text.clear()
                self.results_text.append("Objetos Detectados:")
                for label in detected_labels:
                    self.results_text.append(label)

            # Reconocimiento de Caras
            elif recognition_type == "Caras":
                # Convertir la imagen a escala de grises
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Cargar el clasificador Haar Cascade para la detección de caras
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

                # Realizar la detección de caras
                faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                # Dibujar los cuadros delimitadores alrededor de las caras detectadas
                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Mostrar la imagen con las caras detectadas en la interfaz gráfica
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                pixmap = QPixmap.fromImage(QImage(image_rgb.data, image_rgb.shape[1], image_rgb.shape[0], QImage.Format_RGB888))
                self.image_scene.clear()
                self.image_scene.addItem(QGraphicsPixmapItem(pixmap))
                self.image_view.fitInView(self.image_scene, Qt.IgnoreAspectRatio)  # Modificado aquí

            # Reconocimiento de Patrones
            elif recognition_type == "Patrones":
                # Convertir la imagen a escala de grises
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Aplicar el detector de bordes de Canny
                edges = cv2.Canny(gray_image, 100, 200)

                # Mostrar los bordes detectados en la interfaz gráfica
                pixmap = QPixmap.fromImage(QImage(edges.data, edges.shape[1], edges.shape[0], QImage.Format_Grayscale8))
                self.image_scene.clear()
                self.image_scene.addItem(QGraphicsPixmapItem(pixmap))
                self.image_view.fitInView(self.image_scene, Qt.IgnoreAspectRatio)  # Modificado aquí

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Configurar estilo oscuro para la aplicación
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    window = ImageRecognitionApp()
    window.show()
    sys.exit(app.exec_())
