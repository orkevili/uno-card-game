# Beadandóval kapcsolatos elvárások, értékelési szempontok

## Git és GitHub használata

A munkát a default `main` branchen kell végezni.
*(Kísérletezéshez le lehet belőle ágazni, de a véglegesnek szánt változat kerüljön merge-ölésre a `main`be.)*

Amikor az adott fázis elkészült, mindhárom oktató (@hegyhati, @oliverosz, @szakitom) legyen felkérve reviewernek a Feedback pull request (#1) oldalán.

Az adott reviewer által kért javítások elkészültét a neve melletti *Re-request review* gombbal kell jelezni.

A commit history ne 2-3 db 100+ soros commitból álljon, hanem legyenek gyakori commitok.
Minden önállóan is értelmes (és lehetőleg helyesen működő) változtatásról készüljön commit.
A commit message-ben legyen röviden leírva, hogy mi változott, angolul.
A követendő commit konvenciókról bővebb leírás olvasható [ebben a cikkben](https://cbea.ms/git-commit/).

## 1. Fázis: Specifikáció elkészítése

Először ki kell találni a beadandó témáját, hogy mi legyen a készítendő program célja.
Ezt le kell írni a [docs/specification.md](docs/specification.md)-be, majd review-t kérni.
Erre a **határidő május 26.**
A kérdéses részek tisztázása és a jóváhagyás után kezdődhet a fejlesztés.

A feladat komplexitása jelentősen haladja meg egy 2-3 órás nagy ZH feladat méretét.
Tehát egy 3 függvényből álló ~100 soros program biztos nem éri el az elégséges szintet.

A feladat lehetőleg tartalmazza az alábbiakat:

- File I/O
- `os` modult igénylő könyvtár- vagy fájlműveletek
- `matplotlib` grafikonok
- Hibakezelés, ahol szükséges

## 2. Fázis: Implementáció

### Kódstílus

A program a gyökérkönyvtárból legyen futtatható a `main.py` scripttel.
A forráskódon kívüli további szükséges fájlok kerüljenek a `data`, `img`, `reports`, stb. alkönyvtárakba.

A forráskód legyen szépen tagolt, átlátható és jól dokumentált.
A funkciók legyenek külön fájlokba (modulokba) csoportosítva, a UI és az adatkezelő réteg különüljön el.

Az ismétlődő kódrészletek legyenek külön függvényekbe kiszervezve.
A hosszú, bonyolult függvények legyenek több kisebb, egyetlen önálló részfeladatért felelős függvényekre szétbontva ([single responsibility principle](https://en.wikipedia.org/wiki/Single-responsibility_principle)).

Ne legyenek globális változók, legfeljebb globális konstansok (csupa nagybetűs névvel jelölve őket).

Ahol átláthatóbb kódot eredményez, legyen comprehensionnel létrehozva a list, dict, set.

A függvények paraméterei és visszatérési típusai legyenek type hintekkel ellátva.
Többszintű vagy vegyes értékeket tároló dict-eknél lehet egyszerűsíteni, pl.: `dict[str, dict]` elegendő `dict[str, dict[str, int | str | float | list[tuple[float, float]]]]` helyett.
A helyes típushasználatot a mypy fogja ellenőrizni, ha hibát ír, nem elfogadható a megoldás.

A függvények és a változók nevei legyenek beszédesek, magától értetődőek és angol nyelvűek.
Az indexváltozók, comprehensionben használt ciklusváltozók, file handle-ök lehetnek egybetűs (i,j,k,x,f) nevűek, de törekedni kell a kifejező nevekre.

## Dokumentáció

A függvények docstringjében legyen dokumentálva, hogy mi a feladatuk, mit és milyen formában várnak paraméterben, illetve adnak vissza eredményül, és hogy milyen kivételeket dobhatnak.
Ez alól a triviálisan egyszerű feladatot ellátó függvények kivételek, ha az elnevezésekből egyértelműen kiderülnek a fenti információk.
A docstring ne a függvénynév, a paraméterek és az eredmény felsorolása legyen, hanem adjon plusz információt az olvasónak.
Az egységesen használandó formázás a [google styleguide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) által javasolt formátum.

A docstringekből HTML dokumentáció generálható a pdoc3 programmal (`pip install pdoc3` után) a `html` mappába:

```bash
pdoc3 --html --force .
```

Ez minden push után a GitHubon is megtörténik, és a dokumentáció elérhető lesz az uni-sopron.github.io/REPOSITORY_NAME címen.

A készített program használatát, működésének magyarázatát a [`docs/user_manual.md`](docs/user_manual.md) fájlban kell leírni.

### Tesztelés

A felhasználói interakciót nem igénylő, adatokon műveletet végző függvényekhez készüljenek tesztek.
Ezek lehetnek [doctest](https://docs.python.org/3/library/doctest.html) formában, vagy [pytest](https://pytest.org)-es unit tesztek, vagy vegyesen.

A tesztmodulok a `tests` mappába kerüljenek.
Itt egy példa is látható a pytest használatára.
A doctest-re és a dokumentációra pedig az `example.py` mutat példát.
Ezek a példafájlok kerüljenek törlésre a leadás előtt.

### Külső forrásból származó kódok

Fel szabad használni interneten talált kódrészleteket, de annak egyértelműen jelölni kell a forrását.
Pl. commit message-ben, vagy kommentben.
Az értékelésnél csak a saját kódot vesszük figyelembe.

Szabad felhasználni külső csomagokat is, de akkor ezek legyenek felsorolva a `requirements.txt`-ben (soronként 1 csomagnév).

Copilot, ChatGPT és társainak használata tilos.
Indokolt esetben a szóbeli vizsgán meg kell tudni védeni a megírt kódot, hogy az saját munka volt.
Ez kisebb módosítások megírását is magában foglalhatja.
