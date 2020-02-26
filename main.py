from User import User

def main():
    user_name = ''
    passwd = ''
    u = User(user_name=user_name, passwd=passwd)
    u.login()

if __name__ == "__main__":
    main()


