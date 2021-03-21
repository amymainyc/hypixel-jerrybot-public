def price_formatter(price):
    price = str(price)
    if len(price) > 9:
        price = price[:-3] + ',' + price[-3:]
        price = price[:-7] + ',' + price[-7:]
        price = price[:-10] + ',' + price[-10:]
    elif len(price) > 6:
        price = price[:-3] + ',' + price[-3:]
        price = price[:-7] + ',' + price[-7:]
    elif len(price) > 3:
        price = price[:-3] + ',' + price[-3:]
    else:
        pass
    return price

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
    if len(price) > 9:
        price = price[:-3] + ',' + price[-3:]
        price = price[:-7] + ',' + price[-7:]
        price = price[:-10] + ',' + price[-10:]
    elif len(price) > 6:
        price = price[:-3] + ',' + price[-3:]
        price = price[:-7] + ',' + price[-7:]
    elif len(price) > 3:
        price = price[:-3] + ',' + price[-3:]
    else:
        pass
    return f"{price}.{end}"

def bz_name_formatter(name):
    name = name.lower()
    name = name.split('_')
    new_name = []
    for word in name:
        new_name.append(word.capitalize())
    return ' '.join(new_name)