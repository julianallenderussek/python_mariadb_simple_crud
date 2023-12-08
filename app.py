# save this as app.py
from flask import Flask, request, jsonify, make_response
from dbhelpers import run_statement, serialize_data
import json

app = Flask(__name__)

car_columns = ['id', 'make', 'model', 'year']

@app.get("/api/cars")
def get_cars():
 try:
  result = run_statement('CALL get_all_cars()')
  print(result[0])
  formatted_cars = serialize_data(car_columns, result)
  return make_response(jsonify(formatted_cars), 200)
 except Exception as error:
  return make_response(error, 200)
 
@app.get("/api/cars/<int:car_id>")
def get_car_by_id(car_id):
 try:
  result = run_statement('CALL get_car_by_id(?)', [car_id])
  formatted_car = serialize_data(car_columns, result)[0]
  return make_response(jsonify(formatted_car), 200)
 except Exception as error:
  return make_response(error, 200)

@app.post("/api/cars")
def insert_car():
 try:
  make = request.json.get('make')
  model = request.json.get('model')
  year = request.json.get('year')
  result = run_statement('CALL insert_car(?,?,?)', [make, model, year])
  formatted_car = serialize_data(car_columns, result)[0]
  return make_response(jsonify(formatted_car), 200)
 except:
  return make_response("Working", 200)

@app.put("/api/cars/<int:car_id>")
def update_car(car_id):
 try:
  make = request.json.get('make')
  model = request.json.get('model')
  year = request.json.get('year')
  result = run_statement('CALL update_car(?,?,?,?)', [car_id, make, model, year])
  formatted_car = serialize_data(car_columns, result)[0]
  return make_response(formatted_car, 200)
 except:
  return make_response("Error updating car", 401)

@app.delete("/api/cars/<int:car_id>")
def delete_car(car_id):
 try:
  run_statement('CALL delete_car(?)', [car_id])
  return make_response("",204)
 except:
  return make_response("Error updating car", 401)

app.run(debug=True)