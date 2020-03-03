from environs import Env    # disgusting temporary solution

env = Env()
env.read_env()

SQLALCHEMY_DATABASE_URI = env.str('POSTGRE_URL')
