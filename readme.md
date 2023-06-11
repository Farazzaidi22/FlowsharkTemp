 
# FLOW SHARK

## Tech Stack  

**Server:** Python, Django, Postgres 

## Documentation
[DETAILED DOCUMENT](https://docs.google.com/document/d/16FNhMRJ2ih8CGDYW9rzp8fSJWS3KHkEkn1es7_L6Zdc/edit#heading=h.3jf5ya7wnu0g)

[FIGMA](https://www.figma.com/proto/m4NwX9bOQawH2QDSppFAkJ/Flowshark?page-id=0%3A1&node-id=804-566&viewport=125%2C212%2C0.06&scaling=scale-down-width&starting-point-node-id=2%3A2)

[financial modeling prep](https://site.financialmodelingprep.com/developer/docs/)

## Run Locally  

Clone the project  

~~~bash  
git clone https://github.com/Hamzaaasif/flowShart-python.git
~~~

Run Postgres
~~~bash  
docker run -d --name flowShark -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e PGDATA=/var/lib/postgresql/data/pgdata -v <YOUR_LOCAL_PATH>:/var/lib/postgresql/data postgres:15.1
~~~
<YOUR_LOCAL_PATH> => replace your local YOUR_LOCAL_PATH

Go to the project directory  

~~~bash  
cd flowShark
~~~

Install dependencies  

~~~bash  
pip install -r requirements.txt
~~~

Run Migrations 

~~~bash  
python manage.py migrate
~~~

Start the server  

~~~bash  
python manage.py runserver
~~~


## License  

[MIT](https://choosealicense.com/licenses/mit/)
 
 
