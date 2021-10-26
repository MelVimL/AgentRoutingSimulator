import uuid

class Indentifiable:
    
    def get_id(self):
        try:
            return self._id
        except AttributeError as e:
            self._id = uuid.uuid1()
        return self._id
