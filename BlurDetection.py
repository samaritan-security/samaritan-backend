import cv2

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


"""
checks if an image is blurry
returns True if blurry, False otherwise
"""
def detect_blurry_image(image, threshold):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blur = variance_of_laplacian(image)

    if(blur < threshold):
        return True

    return False