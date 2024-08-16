# Cyclo-Tourist Club / Member and event management, club treasury

This Django project is a platform to manage members, club events and club treasury.
The aim of the project is to create a simple application for management of club members, club treasury, publication of club events with the possibility of registration of members for individual club events.

***on 15.08.2024 an authentication app added into the project. With this app new features will be added soon...***

# To login both to pages and admin section: username: testadmin, password: 12django34

# Technology Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Django, Python
- Database: SQlite
- Data visualization library: Plotly
- Image processing library: Pillow

##### The basic CSS/JavaScript style is not mine - I took it from the Django tutorial project on W3schools.com because my CSS/JavaScript skills are not good enough yet. However, in order to override some of the unnecessary basic styles, I had to use my own CSS as well. The authentication with some of my updates was taken from https://www.geeksforgeeks.org/user-authentication-system-using-django. The rest of the project is my own work.


# O projekte:
***15.8.2024 som do projektu pridal prihlasovanie a registraciu co bude ciastocne menit koncept projektu ktory povodne s prihlasovanim nepocital. Vdaka tomu pribudnu nove moznosti (pridavanie, uprava a mazanie prispevkov clenmi atd.) ktore zatial nie su implementovane. Pre skusobny pristup aj do admin casti pouzite login - username: testadmin, password: 12django34***

Kedze som clenom and sucastne aj pokladnikom cykloturistickeho klubu, cielom projektu je vytvorit jednoduchu aplikaciu na manazment clenov klubu, spravu klubovej pokladnice, zverejnovanie klubovych akcii s moznostou prihasovania clenov na jednotlive klubove akcie. Ako bonus zatial galeria cykloklubu a graf financnej bilancie klubu. 

# Projekt a jeho funkcionalita:

kostrou projektu su 3 zalozky - Clenovia, Pokladna a Klubove akcie

1. **Clenovia**

Clenov cyklokubu prijma clenska rada ako najvyssi organ klubu raz rocne na vyrocnej schodzi, preto povodne nemalo zmysel riesit registraciu clenov cez formular. Udaje o novych clenoch mal do databazy cez admin panel pridat raz rocne predseda klubu. Po novom bude mozna registracia clenov cez formular s tym ze nasledne ich schvalovenie bude na clenskej schodzi. Tuto variantu som ztial neimplementoval (comming sooon).
Pre tento ucel bola vytvorena databaza Members.
Na zalozke je zoznam clenov, po kliknuti na konkretneho clena sa ukazu jeho dalsie udaje. Aj tu bude este potrebny mensi update na databazu - pridat emailovu adresu clena a rok narodenia.

2. **Pokladna**

Kazdy klub ma prijmy a vydavky. Prijmy nasho klubu pochadzaju z clenskych prispevkov. Vydavky klubu su peniaze ktorymi klub prispieva na jednotlove klubove akcie. Uhradeny clensky poplatok je jedna z poloziek databazy Members. Na vydavky je samostatna databaza Expenses. Prijmy a vydavky eviduje pokladnik klubu cez admin panel v spomenutych databazach.
Na zalozke je tabulka s clenskymi poplatkami od jednotlivych clenov a pod nou tabulka s vydavkami klubu v danom roku. Celkove zhrnutie prijmov a vydavkov, spolu s grafom je na zalozke Graficka bilancia.

3. **Klubove akcie**

Klub pocas roku poriada niekolko klubovych akcii na ktorych sa clenovia mozu zucastnit. Nakolko akcie je treba dopredu logisticky naplanovat je dolezite dopredu vediet kolko clenov sa na danu akciu prihlasi. Na tento ucel sluzia databazy ClubEvents a EventSubscribe. 
Na tejto zalozke je preto tabulka so zoznamom klubovych akcii, prihlasovaci formular pomocou ktoreho sa clenovia na akcie mozu prihlasovat a nasledne tabulka s jednotlivymi clenmi ktory sa na klubove akcie prihlasili. Vvdaka autentifikacii bude mozne upravovat alebo mazat zadane udaje samotnymi clenmi.

***zatial bonusove zalozky:***

4. **Klubova galeria**

Po pokusoch s roznymi typmi galerii som zistil ze su komplikovane na spravu ked sa v nich nachadza vacsie mnozstvo obrazkov. Tento problem sa vyriesil vytvorenim databazy ClubPicture cez ktoru sa obrazky jednoducho nahravaju v Admin paneli. 

5. **Graficka bilancia**

Tu je zhrnutie prijmov a vydavkov klubu spolu s grafom. Graf je vytvoreny pomocou kniznice Plotly.

# Zaver:

Nakolko sa Django stale ucim, je zrejme ze by sa projekt dal zvladnut aj lepsie - hlavne frontendova cast. Po miernych upravach a vyladeni vsak moze sluzit ako WWW stranka, ktoru klub este nema.

PS.: udaje a sumy v databazach su samozrejme vymyslene a sluzia k testovaniu funkcnosti systemu :)