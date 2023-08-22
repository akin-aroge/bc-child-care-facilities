install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt


format:
	black .

run:
	streamlit run app.py