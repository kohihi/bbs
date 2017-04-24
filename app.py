from flask import (
    Flask,
)
import config

app = Flask(__name__)

# 配置统一放到 config.py 中
app.secret_key = config.secret_key

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
app.register_blueprint(index_routes)         
app.register_blueprint(topic_routes, url_prefix='/topic')
app.register_blueprint(reply_routes, url_prefix='/reply')
app.register_blueprint(board_routes, url_prefix='/board')

if __name__ == '__main__':
    config = config.dict_run
    app.run(**config)
