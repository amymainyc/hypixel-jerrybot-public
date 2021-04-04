def price_formatter(price):
    price = str(price)
    num = ""
    for i in range(len(price)):
        if len(price[len(price) - i:]) % 3 == 0 and num != "":
            num = "," + num
        num = price[len(price) - i - 1] + num
    return num

def item_name_formatter(item_name):
    name = ""
    for char in range(len(item_name)):
        if item_name[char] == "§":
            pass
        elif char != 0:
            if item_name[char - 1] == "§":
                pass
            else:
                name += item_name[char]
    return name 

def enchant_formatter(enchants):
    name = []
    for enchant in enchants:
        enchant_name = enchant.split("_")
        enchant_name2 = []
        for word in range(len(enchant_name)):
            word = enchant_name[word].capitalize()
            enchant_name2.append(word)
        enchant_name = ' '.join(enchant_name2) + ' ' + str(enchants[enchant])
        name.append(enchant_name)
    return ', '.join(name)

def bz_price_formatter(price):
    price = str(price)
    price = price.split('.')
    end = price[-1]
    price = price[0]
    num = ""
    for i in range(len(price)):
        if len(price[len(price) - i:]) % 3 == 0 and num != "":
            num = "," + num
        num = price[len(price) - i - 1] + num
    return f"{num}.{end}"


def bz_name_formatter(name):
    name = name.lower()
    name = name.split('_')
    new_name = []
    for word in name:
        new_name.append(word.capitalize())
    return ' '.join(new_name)