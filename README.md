Cyclo-Tourist Club / Member and event management, club treasury

This is my first Django project. It's a platform to manage members, club events and club treasury.

You also need to install (with PIP) the following to make it work: Plotly and Pandas for graphs, Pillow for images and Django Debug Toolbar.

The base CSS/JS style is not mine - I took it from the Django tutorial project on W3schools.com as my CSS/JavaScript skills aren't good enough yet. However, to override some unnecessary base style, I also had to use custom CSS.

remarks (for myself only) :

15.7 Pridane polia do tabulky Members, pridana zalozka club_treasury.html

17.7 pridany debug toolbar (instalacia django debug toolbar), vytvorena tabulka Expenses 

18.7 update na club_treasury, vytvorena dalasia testovacia stranka template2,  pridany vzor na login - zatial na testovacej stranke templates2.html - otazka je ci je vobec potrebny kedze s databazou manipuluje iba predseda klubu a pokladnik - uvidime casom.
Pridana zalozka gallery.html - zatial iba zaklad - urobit z toho slideswow / lightbox ?
Update na club_treasury  - pomaly zacinam chapat ten CSS/JS co som sem natiahol z W3schoools.com :)

19.7 pridana zalozka club_events.html  - tu budu planovane akcie cykloklubu a registracia clenov na tieto akcie 

21.7 vytvorene tabulky ClubEvents a EventsSubscribe, vytvoreny prihlasovaci formular (cez footer.html) pre club_events.html

22.7 update na gallery - skusil som lightbox z W3Scholls.com  - je to pekne no takto to nepojde, pri vacsom pocte obrazkov je ich sprava komplikovana, potrebne ine riesenie - nahrat ako objekty do databazy ?

23.7 vytvorena tabulka ClubPicture, obrazky vlozene do nej (instalacia Pillow)

30.7 funguje prihlasovanie clenov na akcie

31.7 funguju vsetky sekcie, treba sa pohrat s designom, mozno pridat grafy a nakoniec upratat: vymazat zbytocne stlpce z databaz: ClubEvents (event_members) a ClubPicture(description) a stare adresare v ktorych boli obrazky predtym ako isli do databazy

6.8 Vytvorena zalozka balance_graph.html - pouzitie grafickej kniznice Plotly pre zobrazenie grafu z databazy (potrebne instalovat Plotly aj Pandas). 

























































