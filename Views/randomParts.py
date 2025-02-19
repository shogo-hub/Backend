from ..Database.MySQLWrapper import MySQLWrapper
import random
from flask import Flask,  render_template

app = Flask(__name__)

db = MySQLWrapper()

@app.route("/")
def randomPart():
    try:
        db.cursor.execute("SELECT * FROM computer_parts ORDER BY RAND() LIMIT 1")

        result = db.cursor.fetchone()

        if result:
            # 結果を辞書型に変換 (扱いやすくするため)
            part = {
                "name": result[1],           # 適切なインデックスを指定
                "type": result[2],
                "brand": result[3],
                "model_number": result[4],
                "release_date": result[5],
                "description": result[6],
                "performance_score": result[7],
                "market_price": result[8],
                "rsm": result[9],
                "power_consumptionw": result[10],
                "lengthm": result[11],
                "widthm": result[12],
                "heightm": result[13],
                "lifespan": result[14],
                "updated_at": result[15]
            }
            return render_template("card.html", part=part)  # card.html をレンダリング
        else:
            return "No part found!"

    except Exception as e:
        return f"Error fetching random part: {e}"




