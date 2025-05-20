import cv2
import numpy as np
import pandas as pd

def analyze_image_content(image):
    """Analyze image content to find features that might indicate parking spaces and cars"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply edge detection
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by size to find potential car-sized objects
    car_like_contours = []
    min_car_area = 500  # Minimum area for a potential car
    max_car_area = 10000  # Maximum area for a potential car
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_car_area < area < max_car_area:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h if h > 0 else 0
            # Typical car aspect ratios are around 2.0 to 2.5 (width/height)
            if 0.5 < aspect_ratio < 3.0:
                car_like_contours.append(contour)
    
    # Count potential cars
    potential_cars = len(car_like_contours)
    
    # Get color distribution - parking lots often have darker areas (cars) and lighter areas (empty spaces)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Dark areas in value channel (potential cars)
    _, dark_mask = cv2.threshold(hsv[:,:,2], 100, 255, cv2.THRESH_BINARY_INV)
    dark_pixel_count = cv2.countNonZero(dark_mask)
    
    # Image dimensions for normalization
    h, w = image.shape[:2]
    total_pixels = h * w
    
    return {
        'potential_cars': potential_cars,
        'dark_pixel_percentage': dark_pixel_count / total_pixels,
        'contour_count': len(contours),
        'image_area': total_pixels,
        'image_width': w,
        'image_height': h
    }

def manual_count_based_on_image(image):
    """Analyze image to estimate parking slots and occupancy based on image content"""
    # Get image analysis data
    analysis = analyze_image_content(image)
    
    # Image size affects the total capacity estimate
    # Larger images often indicate larger parking lots
    size_factor = analysis['image_area'] / (800 * 600)  # Normalized by a standard size
    
    # Base the total on potential cars detected and image size
    # Start with a reasonable base number
    base_estimate = 50
    
    # Adjust based on image size
    size_adjustment = max(int(size_factor * 40), 0)
    
    # Adjust based on detected features
    feature_adjustment = min(max(analysis['potential_cars'], 5), 50)
    
    # Calculate total slots with a minimum of 10 and maximum of 300
    total_slots = min(max(base_estimate + size_adjustment + feature_adjustment, 10), 300)
    
    # Occupied slots based on potential cars and dark areas
    dark_factor = min(analysis['dark_pixel_percentage'] * 2, 0.9)  # Cap at 90%
    car_factor = min(analysis['potential_cars'] / max(total_slots * 0.5, 1), 0.9)  # Cap at a reasonable percentage
    
    # Weighted combination of both factors
    occupied_percentage = (dark_factor * 0.7) + (car_factor * 0.3)
    occupied_slots = int(total_slots * occupied_percentage)
    
    # Ensure occupied slots is reasonable
    occupied_slots = min(max(occupied_slots, int(total_slots * 0.1)), int(total_slots * 0.9))
    
    # Available slots is the difference
    available_slots = total_slots - occupied_slots
    
    return {
        'Total Number of Slots': total_slots,
        'Occupied Slots': occupied_slots,
        'Available Slots': available_slots
    }

def export_results_to_csv(total, occupied, available, filename='parking_data.csv'):
    """Export the results to a CSV file"""
    data = {
        'Total Number of Slots': [total],
        'Occupied Slots': [occupied],
        'Available Slots': [available]
    }
    
    df = pd.DataFrame(data)
    
    # Get absolute path
    import os
    full_path = os.path.abspath(filename)
    
    df.to_csv(filename, index=False)
    print(f"Results exported to {full_path}")
    
    return df