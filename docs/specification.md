# Projekt: UNO
### Rövid összefoglaló
A már jól ismert UNO kártya játék leprogramozása a cél. A játékot lehet egyedül gép ellen, de akár 4-en is lehet játszani.
Kezdetben 108 lapot tartalmaz egy kártya pakli, amelyet véletlenszerű sorrendben kap meg a "játék". Egy játék kezdetekor minden játékos 7 lapot kap, a pakli végéről kivesszük az első olyan lapot, amely megfelel a kezdőkártya kritériumainak(nem lehet szinválasztó, lapfelhúzós, sem egyéb akciókártya, mindenképp számnak kell lennie).
A játékosok kezdetben az óramutató járásával megegyező irányban következnek sorban, mindenki "egyet léphet" (kártya felhúzás/lerakás).
A program ellenőrzi, hogy a játékos által lerakni kivánt lap lerakható-e az utoljára lerakott kártyára.
Ha lapfelhúzós kártya kerül lerakásra, a program, automatikusan "felhúzza" az adott lap mennyiséget a játékos nevében(mivel ez lépésnek számit, ezért a következő játékos jön a körben).

## Osztályok
- **Kártya** metódusok: json-ből betölteni a kártya adatokat, lerakható-e egy adott kártyára?, szinválasztós kártyánál szinkérés
- **Pakli** metódusok: méret, pakli készités a betöltött kártya adatokból, elkészült pakli megkeverése, kezdő kártya kiszedése
- **Játékos** metódusok: kártya hozzáadás, kártya lerakás, van-e kártyája, amit le tud rakni?
- **Játék** metódusok: játékos hozzáadása, kártya húzás, kártya lerakás, játékosok kártyával, következő játékos, robot(magától tesz le/húz fel kártyákat), kör megforditása
## Plot
- A játék során folyamatosan logolni, hogy kinek hány lapja van, a végén egy vonaldiagrammal megjeleniteni, melyik játékosnak hogyan változtak a lapjai.
