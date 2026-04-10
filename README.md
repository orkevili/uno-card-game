# Program működésének, funkcióinak bemutatása, használati útmutató

## Kártyák
Összesen 108 kártya van egy pakliban, ezek 3 különböző kategóriába választhatók szét, nem egyforma arányban. A játékban a kártyák 4 féle színűek lehetnek: piros, zöld, kék, sárga.
1. Szám: 
    - 0-9-ig terjed számozásuk, mindegyik számból 2 lap van színenként, kivéve a 0-ást, abból csak 1.
    - Ezeknek a kártyáknak nincs semmi különleges tulajdonsága.
2. Akció:
    - 'skip' - Ha lerakják a következő játékos kimarad
    - 'reverse' - Megfordítja a kört, ha csak két játékos van, akkor úgy működik, mint a 'skip' kártya
    - 'draw_2' - A következő játékosnak fel kell húznia 2 lapot
3. Színválasztó:
    - Színválasztó - A lerakást követően, aki lerakta választhat egy tetszőlegest színt.
    - Színválasztó húzz fel 4-et - Hasonlóan működik, mint az egyszerű színválasztós kártya, csak utána a következő játékosnak fel kell húznia 4 lapot.

## Bot
 - A programban van lehetőség `bot` ellen is játszani, amennyiben *egyetlen* játékossal indítjuk a játékot.
 - Ilyenkor a program automatikusan hozzáad a játékmenethez egy `bot` játékost, amely teljesen önállóan működik.

        Bot játékos működése, funkciói
    - Figyelembe veszi a lapokat, nem teljesen random módon rakja a kártyákat.
    - Ha le tud tenni egyszerű 'szám' lapot, akkor azt teszi, ha csak 'akció' kártyát tud, akkor leteszi azt, ha ezek közül egyiket se, de rendelkezik 'színválasztó', vagy 'színválasztó húzz fel 4-et' lappal, akkor leteszi azt. Amennyiben nem tud semmilyen lapot se letenni, akkor felhúz egy lapot a pakliból.
        > Színválasztós kártya lerakásánál megnézi a saját kártyái között, hogy melyikből van a legtöbb és olyan színt kér.

## Indítás
A programot a 'main.py' fájl futtatásával lehet elindítani. (Parancssori argumentumként megadható pluszban a `bot` kulcsszó, amelyet, ha beírunk, csak bot játékosokkal futtatja a játékot. Ez a tesztelések során hasznos funkció).
Az indítást követően megkérdezi a program, hogy hány emberrel szeretnénk játszani (A játékosok száma 1-4 között lehet).
>A program bekér a játékosok számának függvényében nevet/neveket. Ha csak egy játékost adunk a játékhoz, a program automatikusan beléptet 3 bot játékost.

## Játékmenet
1. A játékosnevek megadása után a program hozzáadja a játékosokat a játékhoz, legenerál egy kevert paklit.
2. Minden játékosnak kiosztja a kezdőkártyákat, randomizált módon kiválasztja a kezdőjátékost, majd ezután átrendezi a játékoslistát, hogy a kezdőjátékostól induljon(Ez a körök számolásánál fontos).
3. Amikor egy játékos sorra kerül két választása van:
    - felhúz egy lapot, parancssorban: `0`,
    - letesz egy lapot,
        >A program kilistázza a játékos lapjait sorszámozva és egy sorszámot vár válaszul a *parancssorsba*. Ha olyan lapot rakna le a játékos, amely nem letehető, az adott utolsó kártyára, akkor `Can't place red(5) on blue(skip)`-hez hasonló szöveget láthatunk válaszul. Ezen kívül van még egy üzenet, amivel találkozhatunk kártya dobásnál: `[játékos neve] does't have any card to drop on [utolsó rakott kártya]. Please pull a card.(0)`
    
    Miután egy játékos lépett, a program a le/nem rakott kártyától függően lép tovább a következő játékosra.
4. A játék során minden körben készül diagram játékmenetről, amelyet `img/game_stats.png` fájl megtekintésével lehet nyomon követni. (A diagram tartalmazza a játékosokat, azok kártyáinak számát körökre lebontva, így vizuálisan is következő a játékosok állása).
5. A játék addig tart, amíg csak 1 játékos marad kártyákkal. Amennyiben elfogy a húzópakli, a játék kever mégegyet.