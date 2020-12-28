# person-recognition
A person recognition application based on Instagram profile photos

Using the Instagram username of some person, it gets the profile photo used to recognize the person in other photos.

# Example
 `$ python person-recognition.py --username zuck --path /home/user/Desktop/image.jpeg`

It also accepts URLs to get the image

 `$ python person-recognition.py --username zuck --path https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Mark_Zuckerberg_F8_2018_Keynote_%28cropped_2%29.jpg/220px-Mark_Zuckerberg_F8_2018_Keynote_%28cropped_2%29.jpg`
 
 ![](/example/output1.png)

 **Arguments**

 | parameter | type    | description                                      |
 | --------- | ------- | ------------------------------------------------ |
 | `username`     | String  | Instagram username of the person to recognate. Ex.: zuck |
 | `path`  | String | Path to input image (you can use URL or path to file system) |
 | `tolerance` | Float  | Tolerance value to match face to person 0-1.0  |

 ## Credits
 This project is based on <br/>
 [Instagram Profile Picture Extraction](https://github.com/debdutgoswami/instagram-profile-picture)<br/>
 [Face Recognition](https://github.com/ageitgey/face_recognition)
