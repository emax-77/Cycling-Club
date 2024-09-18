# Cyclo-Tourist Club / Member and event management, club treasury

This Django project is a platform to manage members, club events and club treasury.
The aim of the project is to create an application for management of club members, club treasury, publication of club events with the possibility of registration of members for individual club events and some other features.

# Latest updates
- Auth app added into the project.
- Confirmation email is sent to the user after registration to club event.
- contact template with 'contact us' form added to the project - sending email to the club admin.
- the project got a new modern look (with some new CSS) 

# Technology Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Django, Python
- Database: SQlite
- Data visualization library: Plotly
- Image processing library: Pillow

# O projekte:

Kedze som pokladnikom cykloturistickeho klubu, cielom projektu je vytvorit jednoduchu aplikaciu na manazment clenov klubu, spravu klubovej pokladnice, zverejnovanie klubovych akcii s moznostou prihasovania clenov na jednotlive klubove akcie vratane emailovej notifikacie. Ako bonus zatial galeria cykloklubu, graf financnej bilancie klubu a kontaktny formular.

# Projekt a jeho funkcionalita:

kostrou projektu su 3 zalozky - Clenovia, Pokladna a Klubove akcie

1. **Clenovia**

Clenov cyklokubu prijma clenska rada ako najvyssi organ klubu raz rocne na vyrocnej schodzi, preto povodne nemalo zmysel riesit registraciu clenov cez formular. Udaje o novych clenoch mal do databazy cez admin panel pridat raz rocne predseda klubu. Po novom je mozna registracia clenov cez formular s tym ze nasledne ich schvalovenie bude na clenskej schodzi.
Pre zoznam clenov sluzi databaza Members.
Na zalozke je zoznam clenov, po kliknuti na konkretneho clena sa ukazu jeho dalsie udaje.

2. **Pokladna**

Prijmy klubu pochadzaju z clenskych prispevkov. Vydavky su peniaze ktorymi klub prispieva na jednotlove akcie. Uhradeny clensky poplatok je jedna z poloziek databazy Members. Na vydavky je samostatna databaza Expenses. Prijmy a vydavky eviduje pokladnik klubu cez admin panel v spomenutych databazach.
Na zalozke je tabulka s clenskymi poplatkami od jednotlivych clenov a pod nou tabulka s vydavkami klubu v danom roku. Celkove zhrnutie prijmov a vydavkov, spolu s grafom je na zalozke Graficka bilancia.

3. **Klubove akcie**

Klub pocas roku poriada niekolko klubovych akcii na ktorych sa clenovia mozu zucastnit. Na tento ucel su databazy ClubEvents a EventSubscribe. 
Na tejto zalozke je preto tabulka so zoznamom klubovych akcii, prihlasovaci formular pomocou ktoreho sa clenovia na akcie mozu prihlasovat a nasledne tabulka s jednotlivymi clenmi ktory sa na klubove akcie prihlasili. Po prihlaseni na akciu pride clenovi potvrdzovaci email.

***zatial bonusove zalozky:***

4. **Klubova galeria**

Obrazky sa nahravaju cez databazu ClubPicture v Admin paneli. Pouzita je kniznica Pillow.

5. **Graficka bilancia**

Tu je zhrnutie prijmov a vydavkov klubu spolu s grafom. Jednoduchy graf je vytvoreny pomocou kniznice Plotly.

6. **Kontakt**

Klasicky kontaktny formular ktory posle spravu na klubovu emailovu adresu. 

# Zaver:

Bol to moj prvy vacsi Django projekt pri ktoreho budovani som sa toho moc naucil (okrem Djanga aj vela o samotnom HTTP protokole, databazach, atd).
Je tu sice par veci ktoré by som dnes urobil inak, kazdopadne po miernych upravach moze projekt sluzit ako WWW stranka, ktoru klub este nema.

PS.: udaje a sumy v databazach su vymyslene a sluzia k testovaniu funkcnosti systemu :)
