import cv2
import numpy as np
import pandas as pd
import os

def is_valid_parking_lot_image(image):
    if image is None:
        return False, "Image could not be read"
    h, w = image.shape[:2]
    if h < 200 or w < 200:
        return False, "Image is too small to be a valid parking lot"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    std_dev = np.std(gray)
    if std_dev < 20:
        return False, 
    edges = cv2.Canny(gray, 50, 150)
    edge_pixels = cv2.countNonZero(edges)
    edge_percentage = edge_pixels / (h * w)
    if edge_percentage < 0.01:
        return False, 
    if edge_percentage > 0.3:
        return False, 
    
   
    return True, 

def analyze_image_content(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 11, 2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    h, w = image.shape[:2]
    total_pixels = h * w
    typical_car_min_size = (h * w) * 0.001  
    typical_car_max_size = (h * w) * 0.05   
    potential_cars = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if typical_car_min_size < area < typical_car_max_size:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h if h > 0 else 0
            if 0.5 < aspect_ratio < 4.0:
                solidity = area / (w * h)
                if solidity > 0.5:
                    potential_cars.append((x, y, w, h, area, aspect_ratio))
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    v_channel = hsv[:,:,2]
    _, dark_mask = cv2.threshold(v_channel, 90, 255, cv2.THRESH_BINARY_INV)
    dark_pixel_count = cv2.countNonZero(dark_mask)
    dark_percentage = dark_pixel_count / total_pixels

    dark_contours, _ = cv2.findContours(dark_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    dark_regions = []
    
    for contour in dark_contours:
        area = cv2.contourArea(contour)
        if typical_car_min_size < area < typical_car_max_size:
            dark_regions.append(contour)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80, minLineLength=50, maxLineGap=10)
    line_count = 0 if lines is None else len(lines)

    return {
        'potential_cars': len(potential_cars),
        'dark_regions': len(dark_regions),
        'dark_percentage': dark_percentage,
        'lines_detected': line_count,
        'contour_count': len(contours),
        'image_width': w,
        'image_height': h,
        'image_area': total_pixels,
        'std_dev': np.std(gray)
    }

def manual_count_based_on_image(image):
    is_valid, reason = is_valid_parking_lot_image(image)
    
    if not is_valid:
        return {
            'error': reason,
            'Total Number of Slots': 0,
            'Occupied Slots': 0,
            'Available Slots': 0
        }

    analysis = analyze_image_content(image)
    h, w = image.shape[:2]
    image_factor = (h * w) / (1000 * 1000)  
    base_spaces = 30
    size_adjustment = int(image_factor * 40)
    line_adjustment = int(analysis['lines_detected'] * 0.5)
    total_slots = base_spaces + size_adjustment + line_adjustment
    total_slots = min(max(total_slots, 10), 500)
    car_estimate = max(analysis['potential_cars'], analysis['dark_regions'])

    if car_estimate < 5:

        occupied_percentage = analysis['dark_percentage'] * 2  
        occupied_percentage = min(occupied_percentage, 0.9)  
        occupied_slots = int(total_slots * occupied_percentage)
    else:

        occupied_slots = min(car_estimate, total_slots)
    occupied_slots = min(max(occupied_slots, int(total_slots * 0.05)), int(total_slots * 0.95))

    available_slots = total_slots - occupied_slots

    return {
        'Total Number of Slots': total_slots,
        'Occupied Slots': occupied_slots,
        'Available Slots': available_slots,
        'Analysis': analysis 
    }

def export_results_to_csv(total, occupied, available, filename='parking_data.csv'):
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    
    data = {
        'Total Number of Slots': [total],
        'Occupied Slots': [occupied],
        'Available Slots': [available],
        'Occupancy Rate (%)': [round(100 * occupied / total, 1) if total > 0 else 0]
    }
    
    df = pd.DataFrame(data)
    
    df.to_csv(filename, index=False)
    print(f"Results exported to {filename}")
    
    return df