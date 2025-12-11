c = get_config()

# ServerApp settings for JupyterLab 4.x
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.open_browser = False
c.ServerApp.port = 8888
c.ServerApp.allow_root = True

# Password is literally "password"
c.ServerApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=8$gZ5o1JVUiXnSk7US+dIoeg$ogbFypNBBRxLPkr+Z36Q+w'
