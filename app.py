from flask import Flask, request, render_template, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password@92'
app.config['MYSQL_DB'] = 'water management'
mysql = MySQL(app)

class Building:
    def __init__(self, id=None, num_flats=None, water_supply=None):
        self.id = id
        self.num_flats = num_flats
        self.water_supply = water_supply

    def save(self):
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO buildings (num_flats, water_supply) VALUES (%s, %s)',
            (self.num_flats, self.water_supply)
        )
        mysql.connection.commit()
        cur.close()

    def update(self):
        cur = mysql.connection.cursor()
        cur.execute(
            'UPDATE buildings SET num_flats = %s, water_supply = %s WHERE id = %s',
            (self.num_flats, self.water_supply, self.id)
        )
        mysql.connection.commit()
        cur.close()

    def delete(self):
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM buildings WHERE id = %s', [self.id])
        mysql.connection.commit()
        cur.close()

    @classmethod
    def all(cls):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM buildings')
        data = cur.fetchall()
        cur.close()
        return [cls(*row) for row in data]

    @classmethod
    def find_by_id(cls, id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM buildings WHERE id = %s', [id])
        data = cur.fetchone()
        cur.close()
        if data:
            return cls(*data)
        return None

@app.route('/')
def index():
    buildings = Building.all()
    return render_template('index.html', buildings=buildings)

@app.route('/building/new', methods=['GET', 'POST'])
def new_building():
    if request.method == 'POST':
        num_flats = request.form['num_flats']
        water_supply = request.form['water_supply']
        building = Building(num_flats=num_flats, water_supply=water_supply)
        building.save()
        return redirect('/')
    return render_template('new_building.html')

@app.route('/building/<int:id>', methods=['GET', 'POST'])
def edit_building(id):
    building = Building.find_by_id(id)
    if request.method == 'POST':
        num_flats = request.form['num_flats']
        water_supply = request.form['water_supply']
        building.num_flats = num_flats
        building.water_supply = water_supply
        building.update()
        return redirect('/')
    return render_template('edit_building.html', building=building)

@app.route('/building/<int:id>/delete', methods=['POST'])
def delete_building(id):
    building = Building.find_by_id(id)
    building.delete()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
