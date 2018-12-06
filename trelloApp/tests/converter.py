class OrderedDictToObject:

    def __str__(self):
        attribute_value_list = []

        for key in self.__dict__:
            attribute_value_list.append(f'{key}: {self.__getattribute__(key)}')

        return ', '.join(attribute_value_list)

    def __init__(self, ordered_dict):
        for key, value in ordered_dict.items():
            if isinstance(value, list):
                item_object_list = []
                for item in value:
                    item_object_list.append(OrderedDictToObject(item))

                self.__setattr__(key, item_object_list)

            else:
                self.__setattr__(key, value)