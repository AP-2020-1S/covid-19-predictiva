#python3.7 covid-19-predictiva/Datalab/Cargue_inicial_datos.py

jupyter nbconvert --execute covid-19-predictiva/Datalab/Datos_COVID-19.ipynb

jupyter nbconvert --to html covid-19-predictiva/Datalab/Datos_COVID-19.ipynb
mv covid-19-predictiva/Datalab/Datos_COVID-19.html covid-19-predictiva/Dashboard/SARS-COV-2/

cd covid-19-predictiva/Dashboard/SARS-COV-2
python3 jinja2_resultados.py

cd ../../..

cp -R covid-19-predictiva/Dashboard/SARS-COV-2 yoalvarezh.github.io

cd yoalvarezh.github.io
git add .
git commit -m "Actualización Dashboard"
git push origin

cd ..

cd covid-19-predictiva
git add .
git commit -m "Actualización Dashboard"
git push origin

cd ..

