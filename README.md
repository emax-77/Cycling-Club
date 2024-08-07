Cyclo-Tourist Club / Member and event management, club treasury

This is my first Django project. It's a platform to manage members, club events and club treasury.

You also need to install the following to make it work: Plotly and Pandas for graphs, Pillow for images and Django Debug Toolbar.

The base CSS/JS style is not mine - I took it from the Django tutorial project on W3schools.com as my CSS/JavaScript skills aren't good enough yet. However, to override some unnecessary base style, I also had to use custom CSS.

O projekte:

Kedze som clenom and sucastne aj pokladnikom cykloturistickeho klubu, cielom projektu je vytvorit jednoduchu aplikaciu na manazment clenov klubu, spravu klubovej pokladnice, zverejnenie klubovych akcii s moznostou prihasovania clenov na jednotlive klubove akcie.
Ako bonus su zatial galeria cykloklubu a graf financnej bilancie klubu. 

Navrh aplikacie:

kostrou aplikacie su 3 zalozky - Clenovia, Pokladna a Klubove akcie

1. Clenovia:
Clenov cyklokubu prijma clenska rada ako najvyssi organ klubu raz rocne na vyrocnej schodzi, preto nema zmysel riesit registraciu clenov cez formular. Udaje o novych clenoch do databazy cez admin panel prida raz rocne predseda klubu.
Pre tento ucel bola vytvorena databaza Members.
Na tejto zalozke je zoznam clenov, po kliknuti na konkretneho clena sa ukazu jeho dalsie udaje.

2. Pokladna:
Kazdy klub ma prijmy a vydavky. Prijmy nasho klubu pochadzaju z clenskych prispevkov. Vydavky klubu su peniaze ktorymi klub prispieva na jednotlove klubove akcie. Uhradeny clensky poplatok je jedna z poloziek databazy Members. Na vydavky je samostatna databaza Expenses. Prijmy a vydavky eviduje pokladnik klubu cez admin panel v spomenutych databazach.
Na tejto zalozke je tabulka s clenskymi poplatkami od jednotlivych clenov a pod nou tabulka s vydavkami klubu v danom roku.
Celkove zhrnutie prijmov a vydavkov, spolu s grafom je na zalozke Graficka bilancia 

3. Klubove akcie:
Klub pocas roku poriada niekolko klubovych akcii na ktorych sa clenovia mozu zucastnit. Nakolko akcie je treba dopredu logisticky naplanovat je dolezite dopredu vediet kolko clenov sa na danu akciu prihlasi. Na tento ucel sluzia databazy ClubEvents a
EventSubscribe. 
Na tejto zalozke je preto tabulka so zoznamom klubovych akcii, prihlasovaci formular pomocou ktoreho sa clenovia na akcie mozu prihlasovat a nasledne tabulka s jednotlivymi clenmi ktory sa na klubove akcie prihlasili.

bonusove zalozky:

4. Klubova galeria
po pokusoch s roznymi typmi galerii som prisiel na to ze su komplikovane na spravu pokial sa v nich nachadzalo vacsie mnozstvo obrazkov. Tento problem som vyriesil vytvorenim databazy ClubPicture do ktorej sa obrazky jednoducho nahravaju cez Admin panel. 

4. Graficka bilancia
Tu je zhrnutie prijmov a vydavkov klubu spolu s grafom. Graf je vytvoreny pomocou modulu Plotly.

Zaver:

Myslim si ze vsetky hlavne ciele projektu sa podarilo naplnit. Kedze sa vsak jedna o moj prvy projekt s Django frameworkom a zaroven som programator samouk, je zrejme ze projekt by sa dal zvladnut aj lepsie. Hlavne Frontend s ktorym sa zatial prilis nekamaratim. Po miernych upravach a vyladeni vsak moze aplikacia sluzit ako hlavna webova stranka, ktoru klub este nema.
Sekundarnym cielom bolo naucit sa pracovat s Django co sa mi verim podarilo. Pochopil som T-M-V model, pracoval s databazami a podaril sa mi nejaky Backend. A prave na Backend by som sa chcel aj v dalsich projektoch zamerat.

PS.: udaje a sumy v databazach su samozrejme vymyslene a sluzia iba k testovaniu funkcnosti systemu :)




