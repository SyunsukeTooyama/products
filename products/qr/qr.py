import streamlit as st
import qrcode
from PIL import Image
import base64
import io
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def load_image(image_file):
	img = Image.open(image_file)
	return img

st.header("Image QR coder")
image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])

if image_file is not None:

    # To See details
    file_details = {"filename":image_file.name, "filetype":image_file.type,
                    "filesize":image_file.size}
    st.write(file_details)

    # To View Uploaded Image
    st.image(load_image(image_file))
    
    #save an image in server
    with open(os.path.join("fileDir","image.png"),"wb") as f:
        f.write((image_file).getbuffer())
        st.success("File Saved")

    # make download link
    buffered = io.BytesIO()
    img=Image.open('fileDir/image.png')
    img.save(buffered, format="JPEG")
    image_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/jpg;base64,{image_str}" download="image.png">Download</a>'
    st.markdown(f'''## リンクからダウンロードする <button class="link">{href}</button>''', unsafe_allow_html=True)

    # upload image to GoogleDrive
    # connect to drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # delete old file
    file_id = drive.ListFile({'q': 'title = "image.png"'}).GetList()[0]['id']
    old_file = drive.CreateFile({'id': file_id})
    old_file.Delete()

    # upload file
    file_drive=drive.CreateFile()
    file_drive.SetContentFile('fileDir/image.png')
    file_drive['title'] = os.path.basename('fileDir/image.png')
    file_drive.Upload()

    # make download link of drive
    permission = file_drive.InsertPermission({
                            'type': 'anyone',
                            'value': 'anyone',
                            'role': 'reader'})
    link=file_drive['alternateLink']

    # make QR code
    qr = qrcode.make(link)
    qr.save("qr.png")
    st.image("qr.png",output_format="PNG")


_='''
long_url="https://www.python.org/"
url = 'https://api-ssl.bitly.com/v4/shorten'
access_token='73b1d7c0ff1a9ca09886251a5fd609e06c32a5a7'
headers = {"Authorization": f"Bearer {access_token}",
               "Content-Type": "application/json"
               }
body = {'long_url':long_url}
res = requests.post(url, headers=headers, json=body).json()

image_bytes = Path("fileDir/image.png").read_bytes()
image_encoded=base64.b85encode(image_bytes).decode()

href = f'<a href="data:image/png;base64,{image_encoded}" download="image.png">download</a>'''