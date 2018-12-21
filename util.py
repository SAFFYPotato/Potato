import json

# Json file 읽어오기
def read_json(filename):
    path = "data/" + filename

    try:
        with open(path, 'rt', encoding='UTF8') as file:
            data = json.load(file)
        print("read_json Sucess")
        return data

    except:
        print("read_json Fail")
        return False

# Json file 생성하기
def make_json(data, filename):
    path = "data/" + filename

    try:
        with open(path, 'w+', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
        print("Success")
        return True
    except:
        print("Fail")
        return False
