def check_tags(list: list, need_wrong_list: bool = False):
    wrong_list = []

    for value in list:
        if need_wrong_list and type(value) != str:
            wrong_list.append(value)

        elif type(value) != str:
            return False
            
    if need_wrong_list:
        return wrong_list

    return True