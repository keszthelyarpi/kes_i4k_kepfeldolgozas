import cv2
import numpy as np

class LaneDetector:
    def __init__(self):
        self.lower_bound = np.array([15, 20, 70])
        self.upper_bound = np.array([45, 255, 255])

    def process_frame(self, frame):
        h, w, _ = frame.shape
        annotated = frame.copy()

        roi_start_y = int(h * 0.5)
        roi = frame[roi_start_y:h, 0:w]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        M = cv2.moments(mask)
        cx = None
        error_norm = 0.0

        center_x = w // 2
        center_y = roi_start_y + (h - roi_start_y) // 2

        cv2.line(annotated, (center_x, roi_start_y), (center_x, h), (255, 255, 255), 2)

        if M["m00"] > 500:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"]) + roi_start_y

            error_px = cx - center_x
            error_norm = float(error_px) / float(w / 2)

            cv2.circle(annotated, (cx, cy), 8, (0, 0, 255), -1)
            cv2.line(annotated, (center_x, cy), (cx, cy), (0, 255, 0), 3)

            status_text = f"Elteres: {error_norm:+.2f}"
            cv2.putText(annotated, status_text, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            cv2.putText(annotated, "Sav nem talalhato", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        cv2.line(annotated, (0, roi_start_y), (w, roi_start_y), (255, 0, 0), 1)

        return error_norm, annotated, mask

if __name__ == '__main__':
    print("Önálló kamera teszt indítása (Kilépés: 'q' billentyű)...")
    detector = LaneDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Hiba: Nem sikerult megnyitni a webkamerat!")
        exit(1)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Nem erkezik kep a kamerabol.")
            break

        err, annotated_img, mask_img = detector.process_frame(frame)

        cv2.imshow("1. Lane Detector - Standalone Test", annotated_img)
        cv2.imshow("2. HSV Mask (ROI)", mask_img)

        # 'q' megnyomására kilép
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
