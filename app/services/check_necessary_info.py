from app.services.get_type import get_type
from app.services.check_tags import check_tags

def check_necessary_info(data: dict, list: list, check_type: dict):
    
    def check(value: str):
        value_content = data.get(value)
        value_type = get_type(value_content)

        if check_type != {}:
            if (value == "tags" and value_type == "list"):
                if value_content == []:
                    return True

                elif check_tags(value_content):
                    return True

                else:
                    return False

            return value_type == check_type.get(value)

        if (value == "tags" and value_type == "list"):
            if value_content == []:
                return True

        return value_content
        
    necessary_info = []

    for text in list:
        necessary_info.append(check(text))

    return all(necessary_info)