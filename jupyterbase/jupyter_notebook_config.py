c = get_config()

c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.open_browser = False
c.NotebookApp.port = 8888
c.NotebookApp.allow_root = True

# Password is literally "password"
c.NotebookApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=8$gZ5o1JVUiXnSk7US+dIoeg$ogbFypNBBRxLPkr+Z36Q+w'