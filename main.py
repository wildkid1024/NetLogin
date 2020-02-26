from User import User

def main():
    user_name = ''
    passwd = ''
    u = User(user_name=user_name, passwd=passwd)
    u.login()
    u.get_info(method='loadOnlineDevice')
    u.get_info(method='loadUserInfo')
    # u.logout()

if __name__ == "__main__":
    main()


