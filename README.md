# Discussiondeck

Discussiondeck-sovellus on keskustelualusta, jossa käyttäjät voivat aloittaa uusia keskusteluketjuja eri aiheista.


## Ominaisuudet
# välipalautusta varten toteutettu seuraavat ominaisuudet
- Sovellukseen voi luoda käyttäjätunnuksen. Käyttäjätunnus vaatii salasanan.
- Käyttäjät voivat kirjautua sovellukseen.
- Käyttäjät voivat aloittaa uuden keskusteluketjun ja antaa sille otsikon.
- - Etusivulla käyttäjät näkevät keskusteluketjuja. Jokaisesta ketjusta näkee otsikon, aloituspäivän sekä tykkäysten määrän.

# Toteuttamatta:
- Sovelluksessa kahdenlaisia käyttäjiä, pääkäyttäjiä ja tavallisia käyttäjiä.
- Keskusteluketjun otsikkoa voi muuttaa.
- Jokaisesta ketjusta näkee myös aloittajan nimen ja kommenttien määrän.
- Käyttäjät voivat tykätä ketjusta.
- Käyttäjät voivat lisätä ketjuun kommentteja avaamalla ketjun näkyviin uuteen näkymään.
- Käyttäjät näkevät muiden käyttäjien kommentit ja voivat tykätä kommenteista.
- Keskusteluketjuun voi lisätä tunnisteen tai niin sanotun tagin.
- Ketjun perustanut käyttäjä voi poistaa ketjun. Muut tavalliset käyttäjät eivät voi poistaa ketjua.
- Pääkäyttäjä voi poistaa minkä tahansa ketjun, kommentin tai käyttäjän sovelluksesta 
- Sovelluksessa on hakutoiminto, jolla voi hakea ketjuja. Hakutoiminto etsii ketjuja, joissa on hakusanaa vastaava sana tai joissa on hakusanaa vastaava tunniste eli tag.

## Käynnistysohjeet:

Kloonaa discussiondeck repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

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
