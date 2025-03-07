import cv2
from PIL import Image
import numpy as np
from util import get_limits

yellow = [0, 255, 255]  # yellow in BGR colorspace
black = [0, 0, 0]  # black in BGR colorspace

cap = cv2.VideoCapture(1)
# Inicializar la variable para rastrear la detección anterior
objeto_detectado_previo = np.zeros((3, 3), dtype=bool)

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    # Dividir la pantalla en un cuadrado de 3x3
    region_height = height // 3
    region_width = width // 3

    # Variable para rastrear si se ha detectado algo en la iteración actual
    algo_detectado = False

    for i in range(3):
        for j in range(3):
            # Obtener la región actual
            region = frame[i * region_height:(i + 1) * region_height, j * region_width:(j + 1) * region_width]

            # Convertir la región a HSV
            hsv_region = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)

            # Definir los límites de color (amarillo)
            lower_limit, upper_limit = get_limits(color=yellow)

            # Aplicar la máscara
            mask_yellow = cv2.inRange(hsv_region, lower_limit, upper_limit)

            # Convertir la región a escala de grises
            gray_region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

            # Aplicar la máscara
            mask_black = cv2.inRange(hsv_region, np.array([0, 0, 0]), np.array([180+25, 255+25, 30+25]))

            # Verificar si se detecta un objeto en la región actual
            objeto_detectado_yellow = cv2.countNonZero(mask_yellow) > 0
            objeto_detectado_black = cv2.countNonZero(mask_black) > 0
            objeto_detectado = objeto_detectado_yellow or objeto_detectado_black

            # Actualizar el estado previo
            if objeto_detectado and not objeto_detectado_previo[i, j]:
                print(f"Galleta {'quemada' if objeto_detectado_black else 'en buen estado'} en la sección ({i+1}, {j+1})")
                objeto_detectado_previo[i, j] = True
                algo_detectado = True
            elif not objeto_detectado:
                objeto_detectado_previo[i, j] = False

            # Dibujar el cuadro de la región
            color = (0, 255, 0) if objeto_detectado_yellow else (0, 0, 255) if objeto_detectado_black else (255, 255, 255)
            frame = cv2.rectangle(frame, (j * region_width, i * region_height), ((j + 1) * region_width, (i + 1) * region_height), color, 5)

    # Imprimir el arreglo 3x3 correspondiente al estado de los objetos
    if algo_detectado:
        print(objeto_detectado_previo.astype(int))

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
