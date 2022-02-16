import json

def main():
    dic = {
        'updatetime': '23230',
        'saved_data': []
    }
    with open('sthjt.json', 'w') as fp:
        fp.write(json.dumps(dic))
    return 0


if __name__ == '__main__':
    main()