import requests
from PIL import Image, ImageDraw
from io import BytesIO
from bs4 import BeautifulSoup
import re, sys, os
import face_recognition
from urllib.parse import urlparse
import argparse

class PersonRecognition():
    def __init__(self, tolerance=0.6):
        self.tolerance = tolerance
        self.person_face_encoding = None
        self.instagram_username = None
    
    def process_person_face(self, instagram_username):  
        """Encode person face to further recognition"""

        self.instagram_username = instagram_username # Save username to further use

        profile_image = self.get_profile_image() # Get profile image from instagram
        
        person_image = face_recognition.load_image_file(profile_image) # Load image to the face recognition application

        self.person_face_encoding = face_recognition.face_encodings(person_image)[0] # Encode face

    def recognate(self, path):
        """Recognate person in the image"""

        # Check if argument is URL or path to a file system
        if urlparse(path).scheme in ('http', 'https'):
            response = requests.get(path)
            img = BytesIO(response.content)

        elif os.path.exists(path):
            img = path

        else:
            print('Input image not found. Please check the image path')
            exit()
        
        # Load test image
        test_image = face_recognition.load_image_file(img)

        # Find faces
        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image, face_locations)

        # Convert to PIL format
        pil_image = Image.fromarray(test_image)

        # Image draw
        draw = ImageDraw.Draw(pil_image)

        # Loop through faces
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces([self.person_face_encoding], face_encoding, tolerance=self.tolerance)

            if True in matches:
                first_match_index = matches.index(True)
                name = self.instagram_username

                # Draw box
                draw.rectangle(((left, top), (right, bottom)), outline=(255,0,0))

                # Draw label
                text_width, text_height = draw.textsize(name)
                draw.rectangle(((left, bottom-text_height-10), (right, bottom)), fill=(255,0,0), outline=(255,0,0))
                draw.text((left + 6, bottom - text_height - 5), name, fill=(255,255,255,255))

        del draw

        # Display image
        pil_image.show()

    def get_profile_image(self):
        """Return the profile image from @instagram_username"""
        
        url = "https://www.instagram.com/{}/".format(self.instagram_username)

        session = requests.session()

        #Header parameter to resolve bad gateway 502 error
        try:
            html = session.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
        except:
            raise("PageNotFound")
            sys.exit()
        
        # Get image URL using regex and BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all('body')
        profile_pic_url_hd = re.findall(r"profile_pic_url_hd\":\"([\S]+?)\"",str(tags[0]))[0].replace(r'\u0026', '&')

        response = session.get(profile_pic_url_hd, headers={'User-Agent': 'Mozilla/5.0'}).content

        return BytesIO(response)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument('-u', '--username', required=False, type=str,
                help = 'Instagram username of the person to recognate. Ex.: zuck', default = 'zuck')

    ap.add_argument('-p', '--path', required=False, type=str,
                help = 'Path to input image (you can use URL or path to file system)', default = 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Mark_Zuckerberg_F8_2018_Keynote_%28cropped_2%29.jpg/220px-Mark_Zuckerberg_F8_2018_Keynote_%28cropped_2%29.jpg')    
    
    ap.add_argument('-t', '--tolerance', required=False, type=float,
                help = 'Tolerance value to match face to person 0-1.0', default = 0.6)
    
    args = ap.parse_args()

    person_recognition = PersonRecognition(tolerance=args.tolerance)
    person_recognition.process_person_face(instagram_username=args.username)
    person_recognition.recognate(path=args.path)


