import streamlit as st
from PIL import Image
import numpy as np
import os
from googletrans import Translator
from PIL import Image
from io import BytesIO
import glob
import shutil

class TranceAncker():

    def translate_ja(self, txt):
        tr = Translator()
        txt = ''.join(filter(str.isalnum, txt))
        print(txt)
        txt = tr.translate(txt, src="ja", dest="en").text.lower().replace(' ', '_')
        return txt

class Tinypng():
    
    def __init__(self):
        self.translator = TranceAncker()
        
    def return_pc(self, COMPRESS_QUALITY: 30, file_name_ja):
        self.COMPRESS_QUALITY = COMPRESS_QUALITY # 圧縮のクオリティ
        self.file_name_ja = file_name_ja

        file_name_en = self.translator.translate_ja(self.file_name_ja)

        images = glob.glob("./imgs/*")

        out_put_dir = './output_dir/'

        if not os.path.exists(out_put_dir):
            os.makedirs(out_put_dir)

        for i, image in enumerate(images):
            file_name = os.path.splitext(os.path.basename(image))[0]
            with open(image, 'rb') as inputfile:
                # バイナリモードファイルをPILイメージで取得
                im = Image.open(inputfile).convert('RGB')
                # JPEG形式の圧縮を実行
                im_io = BytesIO()
                im.save(im_io, 'JPEG', quality = self.COMPRESS_QUALITY)
            with open('./output_dir/' + file_name_en + str(i) + '.jpg', mode='wb') as outputfile:
                # 出力ファイル(comp_png_image.png)に書き込み
                outputfile.write(im_io.getvalue())


translater = TranceAncker()
IMG_PATH = 'imgs'
OUTPUT_PATH='output_dir'
input_dir = './imgs/'

if not os.path.exists(input_dir):
    os.makedirs(input_dir)

text_ja = st.text_input('画像にあった語句を入れてね！(日本語)')
COMPRESS_QUALITY = st.slider('画像のクオリティーを選択〜', min_value = 10, max_value = 100, value =50)
if text_ja:
    files = st.file_uploader('画像をアップロードしてください.', type=['jpg', 'jpeg', 'png'], accept_multiple_files = True)
    file_name_en = translater.translate_ja(text_ja)

    for file in files:
        img_path = os.path.join(IMG_PATH, file.name)
        with open(img_path, 'wb') as f:
            f.write(file.read())
    
    if files:
        tiny = Tinypng()
        tiny.return_pc(COMPRESS_QUALITY, text_ja)
        shutil.make_archive('output_dir', format='zip', root_dir='output_dir')
        
        with open("./output_dir.zip", "rb") as fp:
            btn = st.download_button(
                    label="Download zip",
                    data=fp,
                    file_name="output_dir.zip",
                    mime="application/zip"
                )
            
                
            if(os.path.isfile('./output_dir.zip') == True):
                os.remove('./output_dir.zip')
                
                    
        
        if(os.path.isdir('./imgs/') == True):
            shutil.rmtree('./imgs/')
        if(os.path.isdir('./output_dir/') == True):
            shutil.rmtree('./output_dir/')
else:
    st.error('画像にあった語句を入れてください！')

        
