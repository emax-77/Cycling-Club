# Cyclo-Tourist Club / Member and event management, club treasury

## !!! IMPORTANT UPDATE (JANUARY 2026) !!! - I decided to refactor most of the old code, so the project may not work properly in the next few days/weeks :)

The project aims to develop an application for managing club members, finances, and publishing club events, with the capability to register members for individual events, as well as other features.

# Latest updates
- Sponsor and Sponsorship models added  
- Auth app added to the project.
- A confirmation email is sent to the user after registration for the club event.
- Contact template with 'contact us' form added to the project - emailing the club admin.
- The project got a new look (with some new CSS)
- Balance_graph.html fixed (grid container)
   

# Technology Stack
- Frontend: HTML, CSS, JS
- Backend: Django, Python
- Database: SQLite3
- Data visualization library: Plotly
- Image processing library: Pillow

# O projekte:

Kedze som pokladnikom cyklo-turistickeho klubu, cielom projektu je vytvorit funkcnu aplikaciu (webove stranky) na manazment clenov klubu, spravu klubovej pokladnice, spravu klubovych akcii s moznostou prihasovania clenov na jednotlive klubove akcie vratane emailovej notifikacie. Ako bonus zatial galeria cykloklubu, graf financnej bilancie klubu a kontaktny formular.

# Projekt a jeho funkcionalita:

kostrou projektu su 3 zalozky - Clenovia, Pokladna a Klubove akcie

1. **Clenovia**

Clenov cyklokubu prijma clenska rada ako najvyssi organ klubu raz rocne na vyrocnej schodzi, preto povodne nemalo zmysel riesit registraciu clenov cez formular. Udaje o novych clenoch mal do databazy cez admin panel pridat raz rocne predseda klubu. Po novom je mozna registracia clenov cez formular s tym ze nasledne ich schvalovenie bude na clenskej schodzi.
Pre zoznam clenov sluzi databaza Members.
Na zalozke je zoznam clenov, po kliknuti na konkretneho clena sa ukazu jeho dalsie udaje.

2. **Pokladna**

Prijmy klubu pochadzaju prevazne z clenskych prispevkov. Vydavky su peniaze ktorymi klub prispieva na jednotlove akcie. Na vydavky je samostatna databaza Expenses. Prijmy a vydavky eviduje pokladnik klubu cez admin panel v spomenutych databazach.
Na zalozke je tabulka s clenskymi poplatkami od jednotlivych clenov a pod nou tabulka s vydavkami klubu v danom roku. Celkove zhrnutie prijmov a vydavkov, spolu s grafom je na zalozke Graficka bilancia.
Novinkou (2026) je pridany model Sponsor a Sponsorship, na ich zapracovani do pokladne sa momentalne pracuje :)

3. **Klubove akcie**

Klub pocas roku poriada niekolko klubovych akcii na ktorych sa clenovia mozu zucastnit. Na tento ucel su databazy ClubEvents a EventSubscribe. 
Na tejto zalozke je preto tabulka so zoznamom klubovych akcii, prihlasovaci formular pomocou ktoreho sa clenovia na akcie mozu prihlasovat a nasledne tabulka s jednotlivymi clenmi ktory sa na klubove akcie prihlasili. Po prihlaseni na akciu pride clenovi potvrdzovaci email.

***zatial bonusove zalozky:***

4. **Klubova galeria**

Obrazky sa nahravaju cez databazu ClubPicture v Admin paneli. Pouzita je kniznica Pillow.

5. **Graficka bilancia**

Tu je zhrnutie prijmov a vydavkov klubu spolu s grafom. Jednoduchy graf je vytvoreny pomocou kniznice Plotly.

6. **Kontakt**

Klasicky kontaktny formular, ktory posle spravu na klubovu adresu. 

# Zaver:

V roku 2024 to bol moj prvy vacsi Django projekt pri ktoreho budovani som sa vela naucil.
Je tu par veci ktoré by som dnes urobil inak, kazdopadne po miernych upravach moze projekt sluzit ako WWW stranka, ktoru klub este nema.
Update 01/2026 - rozhodol som sa dat tomuto projektu sancu a v najblizsom case prepisem vacsinu stareho backendu a ak bude cas, pozriem sa aj na frontend :)

