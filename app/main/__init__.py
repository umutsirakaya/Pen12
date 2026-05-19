from flask import Blueprint

main = Blueprint('main', __name__)

from app.main import routes

# Rotalar buraya eklenecek (views.py veya routes.py olarak da ayrilabilir, simdilik init icinde)
