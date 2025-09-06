python -m venv venv

.\venv\Scripts\activate

python -m pip install --upgrade pip

pip install -r requirements.txt
python app.py

& "C:\Users\hp\AppData\Local\Programs\Python\Python310\python.exe" -m venv venv310


============================================================


Sample 1: Typical (Healthy/Non-glaucoma) Case
Use these values to simulate a typical, healthy patient input:

Age: 55

IOP: 15

CCT: 535

VF Mean: 20

Interval Years: 1

OCT RNFL thickness: 100

OCT RNFL thickness.1: 105

OCT RNFL thickness.2: 110

OCT RNFL thickness.3: 115

OCT RNFL thickness.4: 120


Sample 2: Possible Glaucoma Scenario
Even though your training data didn’t include glaucoma-positive examples, you can test with these values to simulate a different scenario. In a more balanced dataset this might represent a patient with degraded measurements:

Age: 70

IOP: 18

CCT: 500

VF Mean: 15

Interval Years: 2

OCT RNFL thickness: 80

OCT RNFL thickness.1: 75

OCT RNFL thickness.2: 70

OCT RNFL thickness.3: 65

OCT RNFL thickness.4: 60