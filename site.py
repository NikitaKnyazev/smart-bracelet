# -*- coding: utf-8 -*-
import os, shutil, random
from flask import Flask, render_template, request, send_file
import pandas as pd

columns = ['id', 'name1', 'name2', 'name3', 'gender', 'age', 'blood', 'pulse']
df = pd.DataFrame(columns = columns)

df.loc[len(df)] = [len(df), 'Ivan', 'Ivanov', 'Ivanovich', 'M', str(random.randint(20, 80)), 'A(II) Rh+', random.randint(50, 120)]
df.loc[len(df)] = [len(df), 'Petr', 'Petrov', 'Petrovich', 'M', str(random.randint(20, 80)), 'O(I) Rh-', random.randint(50, 120)]
df.loc[len(df)] = [len(df), 'Mary', 'Petrova', 'Ivanovna', 'F', str(random.randint(20, 80)), 'AB(III) Rh-', random.randint(50, 120)]


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', data = df)

@app.route('/people', methods=['GET', 'POST'])
def people():
    var = int(request.args.get('my_var', None)[1])
    people = df[df['id']==var]
    name1 = people['name1'].values[0]
    name2 = people['name2'].values[0]
    name3 = people['name3'].values[0]
    gender = people['gender'].values[0]
    age = people['age'].values[0]
    blood = people['blood'].values[0]
    people['pulse'] = random.randint(50, 120)
    pulse = int(people['pulse'].values[0])
    return render_template('form2.html', data = (name1, name2, name3, gender, age, blood, pulse))
    #return render_template('form.html')

@app.route('/sms', methods=['GET', 'POST'])
def sms():
    return render_template('video.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
