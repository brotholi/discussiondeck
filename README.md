# Discussiondeck

Discussiondeck-sovellus on keskustelualusta, jossa käyttäjät voivat aloittaa uusia keskusteluketjuja eri aiheista.


## Ominaisuudet
#### Kirjautuminen
- Sovellukseen voi luoda käyttäjätunnuksen. Käyttäjätunnus vaatii salasanan.
- Käyttäjät voivat kirjautua sovellukseen.
- Sovelluksessa kahdenlaisia käyttäjiä, ylläpitäjiä ja tavallisia käyttäjiä.

#### Keskustelut
- Käyttäjät voivat aloittaa uuden keskusteluketjun ja antaa sille otsikon. Ketjulle annetaan myös sisältö.
- Etusivulla käyttäjät näkevät keskusteluketjuja. Jokaisesta ketjusta näkee otsikon, aloituspäivän sekä tykkäysten määrän.
- Jokaisesta ketjusta näkee uudessa ikkunassa myös sisällön, aloittajan nimen ja kommentit.
- Käyttäjät voivat tykätä ketjusta. Ketjusta voi tykätä vain kerran
- Käyttäjät voivat lisätä ketjuun kommentteja.
- Keskusteluketjuun voi lisätä tunnisteen tai niin sanotun tagin
- Sovelluksessa on hakutoiminto, jolla voi hakea ketjuja. Hakutoiminto etsii ketjuja, joiden nimessä tai tagissa on vastaava sana.
- Ketjun perustanut käyttäjä voi poistaa ketjun. Muut tavalliset käyttäjät eivät voi poistaa ketjua.
- Ylläpitäjä voi poistaa minkä tahansa keskusteluketjun
- Ylläpitäjä voi lisätä sovellukseen mainoksia ja aktivoida niitä. Kolme mainosta voi olla kerrallaan aktiivisina. 

### TODO:
- virheilmoitusten siistiminen
- ulkoasun viimeistely
- Etusivulla näkyy kerrallaan yksi aktiivisista mainoksista. Mainoksen taso määrittää sen, kuinka suurella todennäköisyydellä mainos näytetään.

## Käynnistysohjeet:
Ennen käynnistystä asenna PostgreSQL kurssin ohjeiden mukaisesti ja käynnistä tietokanta komennolla start-pg.sh

Kloonaa discussiondeck-repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

```bash
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
```

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```

Määritä vielä tietokannan skeema komennolla

```bash
$ psql < schema.sql
```

Nyt voit käynnistää sovelluksen komennolla

```bash
$ flask run
```
