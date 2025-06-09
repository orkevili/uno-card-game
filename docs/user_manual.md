# Program működésének, funkcióinak bemutatása, használati útmutató
## Bot
 - A programban van lehetőség `bot` ellen is játszani, amennyiben *egyetlen* játékossal indítjuk a játékot.
 - Ilyenkor a program automatikusan hozzáad a játékmenethez egy `bot` játékost, amely teljesen önállóan működik.

        Bot játékos működése, funkciói
    - Figyelembe veszi a lapokat, nem teljesen random módon rakja a kártyákat.
    - Ha le tud tenni egyszerű 'szám' lapot, akkor azt teszi, ha csak 'akció' lapot tud, akkor leteszi azt, ha ezek közül egyiket se, de rendelkezik 'színválasztó', vagy 'színválasztó húzz fel 4-et' lappal, akkor leteszi azt. Amennyiben nem tud semmilyen lapot se letenni, akkor felhúz egy lapot a pakliból.
        > Színválasztós kártya lerakásánál megnézi a saját kártyái között, hogy melyikből van a legtöbb és olyan színt kér.

## Indítás
    A programot a 'main.py' fájl futtatásával lehet elindítani.
Az indulást követően a program megkérdezi a felhasználótól, hogy hány emberrel szeretnénk játszani (A játékosok száma 1-4 között lehet).
>A program bekér a játékosok számának függvényében nevet/neveket.

## Játékmenet
1. A játékosnevek megadása után a program hozzáadja a játékosokat a játékhoz, legenerál egy kevert paklit.
2. Minden játékosnak kiosztja a kezdőkártyákat, randomizált módon kiválasztja a kezdőjátékost.
3. Amikor egy játékos sorra kerül két választása van:
    - felhúz egy lapot, parancssorban: `pull`,
    - letesz egy lapot, parancssorban: `drop`
        > Ha úgy adunk egy `drop` parancsot, hogy nem tudnák lapot tenni, akkor a program automatikusan felhúz egy lapot a nevünkben. A program kilistázza a játékos lapjait sorszámozva és egy sorszámot vár válaszul a *parancssorsba*.
    
    Miután egy játékos lépett (`drop`, `pull`), a program a le/nem rakott kártyától függően lép tovább a következő játékosra.
4. A játék során minden körben készül diagram játékmenetről, amelyet `stat.png` fájl megtekintésével lehet nyomon követni. (A diagram tartalmazza a játékosokat, azok kártyáinak számát körökre lebontva, így vizuálisan is következő a játékosok állása).
5. A játék addig tart, amíg el nem fogy a húzópakli, vagy csak 1 játékos marad kártyákkal.