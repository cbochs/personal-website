

def handle_cursor(cursor_loc=None, limit=0):
    def decorator(api_call):
        def wrapper(self, *args, **kwargs):
            no_cursor = kwargs.pop('no_cursor', False)
            if no_cursor:
                if limit > 0:
                    kwargs.update(limit=limit)
                
                result = api_call(self, *args, **kwargs)

                if cursor_loc is not None:
                    cursor = result[cursor_loc]
                else:
                    cursor = result

                items = cursor['items']
                while cursor['next']:
                    cursor = self._next(cursor)
                    items.extend(cursor['items'])
                
                if cursor_loc is not None:
                    result[cursor_loc] = items
                else:
                    result = items

                return result
            else:
                return api_call(self, *args, **kwargs)
        return wrapper
    return decorator


def handle_bulk(limit):
    def decorator(api_call):
        def wrapper(self, *args, **kwargs):
            call_name = api_call.__name__

            if isinstance(kwargs['ids'], list):
                item_ids = kwargs.pop('ids')
                items = []
                for ids in chunks(item_ids, limit):
                    kwargs.update(ids=','.join(ids))
                    items.extend(api_call(self, *args, **kwargs)[call_name])
                return items
            else:
                return api_call(self, *args, **kwargs)[call_name]
        return wrapper
    return decorator


def chunks(list_, n):
    for i in range(0, len(list_), n):
        yield list_[i:i+n]