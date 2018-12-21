import util
import re
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

category_data = util.read_json("categoryData.json")
region_data = category_data["region"]
crops_data = category_data["crops"]
price_data = util.read_json("priceData.json")

# 사용자가 입력한 문장에서 플래그 뽑아내기 (문장 정제 함수)
def analysis_text(origin_text):
    where = ""
    what = ""

    if re.findall("\d+", origin_text):
        price = re.findall("\d+", origin_text)
        price = int(price[0])
    else:
        price = 0

    for reg in region_data:
        if reg in origin_text:
            where = reg
            break
        else:
            where = region_data[0]

    for crop in crops_data:
        if crop in origin_text:
            what = crop
            break
        else:
            what = crops_data[0]

    return [where, what, price]

# 플래그 기반 챗봇 응답 함수
def bot_dialog(origin_text, refined_text):

    if "얼마" in origin_text or "가격" in origin_text:
        return show_price(refined_text)
    elif "살까" in origin_text or "구매" in origin_text:
        return judge_price(refined_text)
    elif "수원" in origin_text:
        return "그런거 없다 현정아 딱콩!"
    elif "사용법" in origin_text or "어떻게" in origin_text:
        return show_guide()
    else:
        for reg in category_data['region']:
            if reg in origin_text:
                return show_price_all(reg)
        return "후헿헿 감자 고장나부러땅!"

# 지역, 품목, 가격을 입력받아 시세와 비교하여 구매여부를 알려주는 함수
def judge_price(refined_text):
    keywords = []
    difference = refined_text[2] - price_data[refined_text[0]][refined_text[1]]['가격']

    if difference > 0:
        sentence = "개손해 개손해! 사지마! 지금 시세 보다 " + str(difference) + "원이나 비싸다구!"
    elif difference < 0:
        sentence = "갸꿀~~ 개이득! 당장사! 지금 시세 보다 " + str(abs(difference)) + "원이나 싸다구!"
    elif difference == 0:
        sentence = "음... 아주 정직한 집이군 시세랑 정확히 똑같아!"

    keywords.append(sentence)
    return u'\n'.join(keywords)

# 지역, 품목을 입력받아 현재 시세를 알려주는 함수
def show_price(refined_text):
    keywords = []
    price_info = price_data[refined_text[0]][refined_text[1]]

    sentence = (refined_text[0] + " 지역의 " + refined_text[1] + "(은)는 " + price_info['단위'] +
                "에 " + str(price_info['가격']) + "원 이고 전주 대비 " + price_info['변동'] + " / " +
                price_info['변동비'] + " 변동하였습니다.")

    keywords.append(sentence)
    return u'\n'.join(keywords)

# 지역을 입력받아 모든 품목의 현재 시세를 알려주는 함수
def show_price_all(reg):
    keywords = []
    for what in category_data['crops']:
        keywords.append(show_price([reg, what]))

    #show_guide()
    return u'\n'.join(keywords)

# Potato 챗봇 사용법 출력하는 함수
def show_guide():
    try:
        with open("data/guide.txt", 'rt', encoding='UTF8') as file:
            print("show_guide Success")
            return u''.join(file.readlines())
    except:
        print("show_guide Fail")

def show_chart(reg):

    data_h = crops_data
    data_v = []

    for crop in crops_data:
        data_v.append(price_data[reg][crop]['가격'])
    pos = range(len(data_h))

    font = fm.FontProperties(fname='font/NanumBarunGothic.ttf')

    plt.bar(pos, data_v, align='center')
    plt.xticks(pos, data_h, rotation='vertical', fontproperties=font)
    plt.title(reg+" 지역 채소 소매가", fontproperties=font)
    plt.ylabel('원', fontproperties=font)
    plt.tight_layout()

    plt.savefig('images/graph.png')
