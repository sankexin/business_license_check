import business_license_check
from flask import Flask
from PIL import Image
from PIL import ImageEnhance
import json

app = Flask(__name__)

# Image preprocess
def img_prep(img):
    enh_bri = ImageEnhance.Brightness(img).enhance(1.05)
    enh_col = ImageEnhance.Color(enh_bri).enhance(1.6)
    enh_con = ImageEnhance.Contrast(enh_col).enhance(1.8)
    new_img = ImageEnhance.Sharpness(enh_con).enhance(2.5)
    return new_img

# Image compress
def img_comp(img, mwidth=1080, mheight=1920):
    w, h = img.size
    if w <= mwidth and h <= mheight:
        new_img = img
        print('image is OK.')
    if (1.0 * w / mwidth) > (1.0 * h / mheight):
        scale = 1.0 * w / mwidth
        new_img = img.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)

    else:
        scale = 1.0 * h / mheight
        new_img = img.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
    new_img.show()
    new_img.save('./data/temp.jpg')
    path = './data/temp.jpg'
    return path

# get recognition result
def get_response(path):
    with open(path, 'rb') as bin_data:
        img = bin_data.read()
    ai_obj = business_license_check.AiPlat(business_license_check.app_id, business_license_check.app_key)
    print('----------------------SEND REQ----------------------')
    rsp = ai_obj.busi_lic_check(img)
    list1 = []
    list2 = []
    if rsp['ret'] == 0:
        for i in rsp['data']['item_list']:
            item = i['item']
            itemstring = i['itemstring']
            res = item + ':' + itemstring
            if len(item) != 0:
                list1.append(item)
            else:
                list1.append('NULL')
            if len(itemstring) != 0:
                list2.append(itemstring)
            else:
                list2.append('NULL')
            print(res)
        print('----------------------API SUCC----------------------')
    else:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        print('----------------------API FAIL----------------------')
    final = dict(zip(list1, list2))
    response = json.dumps(final, ensure_ascii=False)
    return response

@app.route('/')
def busi_lice():
    image = Image.open('./data/015.jpg')
    image = img_prep(image)
    image_path = img_comp(image)
    result = get_response(image_path)
    return result

if __name__ == '__main__':
    app.run(debug=False, threaded=True)             #启动app的调试模式