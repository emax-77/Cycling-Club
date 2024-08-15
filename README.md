# Today (15.08) I added an authentication app into the project. It still has some bugs, but I will try to fix them ASAP. Due to new authentication system, the new features will be added soon.
# To test login: username: testadmin, password: 12django34




# Cyclo-Tourist Club / Member and event management, club treasury

This is my first Django project. It's a platform to manage members, club events and club treasury.
The aim of the project is to create a simple application for management of club members, management of club treasury, publication of club events with the possibility of registration of members for individual club events.

# Technology Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Django, Python
- Database: SQlite3
- Data visualization library: Plotly
- Image processing library: Pillow


##### The base CSS/JS style is not mine - I took it from the Django tutorial project on W3schools.com as my CSS/JavaScript skills aren't good enough yet. However, to override some unnecessary base style, I also had to use custom CSS.


# O projekte:
***!!! upozornenie: 15.8. som do takmer hotoveho projektu pridal autentifikaciu ktora este nie je plne funkcna no zaroven sa tym bude ciastocne menit i koncept projektu ktory povodne s autentifikaciou nepocital. Vdaka nej pribudnu nove moznosti (ako pridavanie, uprava a mazanie prispevkov clenmi) ktore zatial nie su dole uvedene. Pre skusobny pristup pouzite username: testadmin, password: 12django34***

Kedze som clenom and sucastne aj pokladnikom cykloturistickeho klubu, cielom projektu je vytvorit jednoduchu aplikaciu na manazment clenov klubu, spravu klubovej pokladnice, zverejnovanie klubovych akcii s moznostou prihasovania clenov na jednotlive klubove akcie.
Ako bonus su zatial galeria cykloklubu a graf financnej bilancie klubu. Sekundarnym cielom je ucit sa lepsie pracovat s Django frameworkom.

# Poziadavky na aplikaciu a jej funkcionalita:

kostrou aplikacie su 3 zalozky - Clenovia, Pokladna a Klubove akcie

1. **Clenovia**

Clenov cyklokubu prijma clenska rada ako najvyssi organ klubu raz rocne na vyrocnej schodzi, preto nema zmysel riesit registraciu clenov cez formular. Udaje o novych clenoch do databazy cez admin panel prida raz rocne predseda klubu.
Pre tento ucel bola vytvorena databaza Members.
Na tejto zalozke je zoznam clenov, po kliknuti na konkretneho clena sa ukazu jeho dalsie udaje.

2. **Pokladna**

Kazdy klub ma prijmy a vydavky. Prijmy nasho klubu pochadzaju z clenskych prispevkov. Vydavky klubu su peniaze ktorymi klub prispieva na jednotlove klubove akcie. Uhradeny clensky poplatok je jedna z poloziek databazy Members. Na vydavky je samostatna databaza Expenses. Prijmy a vydavky eviduje pokladnik klubu cez admin panel v spomenutych databazach.
Na tejto zalozke je tabulka s clenskymi poplatkami od jednotlivych clenov a pod nou tabulka s vydavkami klubu v danom roku.
Celkove zhrnutie prijmov a vydavkov, spolu s grafom je na zalozke Graficka bilancia.

3. **Klubove akcie**

Klub pocas roku poriada niekolko klubovych akcii na ktorych sa clenovia mozu zucastnit. Nakolko akcie je treba dopredu logisticky naplanovat je dolezite dopredu vediet kolko clenov sa na danu akciu prihlasi. Na tento ucel sluzia databazy ClubEvents a EventSubscribe. 
Na tejto zalozke je preto tabulka so zoznamom klubovych akcii, prihlasovaci formular pomocou ktoreho sa clenovia na akcie mozu prihlasovat a nasledne tabulka s jednotlivymi clenmi ktory sa na klubove akcie prihlasili.

***bonusove zalozky:***

4. **Klubova galeria**

Po pokusoch s roznymi typmi galerii som zistil ze su komplikovane na spravu ked sa v nich nachadza vacsie mnozstvo obrazkov. Tento problem sa vyriesil vytvorenim databazy ClubPicture cez ktoru sa obrazky jednoducho nahravaju v Admin paneli. 

5. **Graficka bilancia**

Tu je zhrnutie prijmov a vydavkov klubu spolu s grafom. Graf je vytvoreny pomocou kniznice Plotly.

# Zaver:

Nakolko sa jedna o moj prvy projekt s Django, je zrejme ze by sa dal zvladnut aj lepsie, hlavne frontendova cast. Po miernych upravach a vyladeni vsak moze aplikacia sluzit ako hlavna webova stranka, ktoru klub este nema. 

PS.: udaje a sumy v databazach su samozrejme vymyslene a sluzia iba k testovaniu funkcnosti systemu :)