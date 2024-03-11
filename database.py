import pickle

def check_auth(login: str, password: str):
    if login=='admin' and password=='123':
        return True
    else:
        return False
    
def get(uid):
    with open(f'static/userbase/{uid}.pickle', 'rb') as file:
        return pickle.load(file)

def add(uid):
    with open(f'static/userbase/{uid}.pickle', 'wb') as file:
        print('Новый добавлен')
        pickle.dump({'user_id': uid}, file)

def save(uid, params):
    with open(f'static/userbase/{uid}.pickle', 'wb') as file:
        print(f'Сохранено - {params}')
        pickle.dump(params, file)

if __name__=='__main__':
    print(get(199))