# Cyclo-Tourist Club / Member and event management, club treasury
This is my first Django project. It's a platform to manage members, club events and club treasury.
The aim of the project is to create a simple application for management of club members, management of club treasury, publication of club events with the possibility of registration of members for individual club events.

# Technology Stack
- Frontend: HTML, CSS, JavaScript and some Python scripts
- Backend: Django, Python
- Database: SQlite
- Data visualization library: Plotly
- Image processing library: Pillow


# Installation
### Prerequisites
- Django
- packages: plotly, pandas, pillow

1. Clone the repository:
```bash
    git clone https://github.com/emax-77/Cycling-Club.git
    cd Cycling-Club
```

2. Install dependencies:
```bash
    pip install -r requirements.txt
```

3. Set up environment variables:
   - Create a .env file in the root directory.
   - Add the following variables:
```bash
    python -m venv env
    source env/bin/activate   # On Windows, use `env\Scripts\activate`
```

4. Apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

##### The base CSS/JS style is not mine - I took it from the Django tutorial project on W3schools.com as my CSS/JavaScript skills aren't good enough yet. However, to override some unnecessary base style, I also had to use custom CSS.


# O projekte:

Kedze som clenom and sucastne aj pokladnikom cykloturistickeho klubu, cielom projektu bolo vytvorit jednoduchu aplikaciu na manazment clenov klubu, spravu klubovej pokladnice, zverejnenie klubovych akcii s moznostou prihasovania clenov na jednotlive klubove akcie.
Ako bonus su zatial galeria cykloklubu a graf financnej bilancie klubu. 

# Navrh aplikacie:

kostrou aplikacie su 3 zalozky - Clenovia, Pokladna a Klubove akcie

1. **Clenovia**

Clenov cyklokubu prijma clenska rada ako najvyssi organ klubu raz rocne na vyrocnej schodzi, preto nema zmysel riesit registraciu clenov cez formular. Udaje o novych clenoch do databazy cez admin panel prida raz rocne predseda klubu.
Pre tento ucel bola vytvorena databaza Members.
Na tejto zalozke je zoznam clenov, po kliknuti na konkretneho clena sa ukazu jeho dalsie udaje.

2. **Pokladna**

Kazdy klub ma prijmy a vydavky. Prijmy nasho klubu pochadzaju z clenskych prispevkov. Vydavky klubu su peniaze ktorymi klub prispieva na jednotlove klubove akcie. Uhradeny clensky poplatok je jedna z poloziek databazy Members. Na vydavky je samostatna databaza Expenses. Prijmy a vydavky eviduje pokladnik klubu cez admin panel v spomenutych databazach.
Na tejto zalozke je tabulka s clenskymi poplatkami od jednotlivych clenov a pod nou tabulka s vydavkami klubu v danom roku.
Celkove zhrnutie prijmov a vydavkov, spolu s grafom je na zalozke Graficka bilancia 

3. **Klubove akcie**

Klub pocas roku poriada niekolko klubovych akcii na ktorych sa clenovia mozu zucastnit. Nakolko akcie je treba dopredu logisticky naplanovat je dolezite dopredu vediet kolko clenov sa na danu akciu prihlasi. Na tento ucel sluzia databazy ClubEvents a EventSubscribe. 
Na tejto zalozke je preto tabulka so zoznamom klubovych akcii, prihlasovaci formular pomocou ktoreho sa clenovia na akcie mozu prihlasovat a nasledne tabulka s jednotlivymi clenmi ktory sa na klubove akcie prihlasili.

bonusove zalozky:

4. **Klubova galeria**

Po pokusoch s roznymi typmi galerii som prisiel na to ze su komplikovane na spravu pokial sa v nich nachadzalo vacsie mnozstvo obrazkov. Tento problem som vyriesil vytvorenim databazy ClubPicture do ktorej sa obrazky jednoducho nahravaju cez Admin panel. 

5. **Graficka bilancia**

Tu je zhrnutie prijmov a vydavkov klubu spolu s grafom. Graf je vytvoreny pomocou kniznice Plotly.

# Zaver:

Myslim si ze hlavne ciele projektu sa podarilo naplnit. Kedze sa vsak jedna o moj prvy projekt s Django a zaroven som programator samouk, je zrejme ze projekt by sa dal zvladnut aj lepsie. Hlavne Frontend s ktorym sa zatial prilis nekamaratim. Po miernych upravach a vyladeni vsak moze aplikacia sluzit ako hlavna webova stranka, ktoru klub este nema.
Sekundarnym cielom bolo naucit sa pracovat s Django frameworkom co sa mi verim podarilo. Pochopil som T-M-V model, pracoval s databazami a podaril sa mi nejaky Backend. A prave na Backend by som sa chcel aj v dalsich projektoch zamerat.

PS.: udaje a sumy v databazach su samozrejme vymyslene a sluzia iba k testovaniu funkcnosti systemu :)