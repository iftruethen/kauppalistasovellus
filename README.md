# kauppalistasovellus
Projektin aihe: <b>kauppalistasovellus</b>

Sovellus tulee toteuttamaan vaaditut toiminnallisuudet:

<ul>
    <li>
        Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
        <ul>
        <li>
            Selvä ratkaisu ja toiminnallisuus.
        </li>
        </ul>
    </li>
    <li>
        Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita.
        <ul>
            <li>
                Käyttäjät pystyvät luomaan henkilökohtaisia ostoslistoja kauppareissuja varten. Ostoslistoja pystyy myös jakamaan muiden käyttäjien kanssa, jolloin he pääsevät näkemään ja muokkaamaan jaettuja listoja.
            </li>
        </ul>
    </li>
    <li>
        Käyttäjä näkee sovellukseen lisätyt tietokohteet.
        <ul>
            <li>
                Selvä ratkaisu ja toiminnallisuus.
            </li>
        </ul>
    </li>
    <li>
        Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella.
        <ul>
            <li>
                Käyttäjät voivat luoda useita kauppalistoja esimerkiksi eri tarkoituksiin: ruokakauppaan, rautakauppaan, lemmikkieläintarvikeliikkeeseen jne. Listoista voi myös etsiä yksittäisiä artikkeleita (helpottaa jos käsittelee pitkää listaa ja haluaa vaikka poistaa tietyn artikkelin).
            </li>
        </ul>
    </li>
    <li>
        Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät tietokohteet.
        <ul>
            <li>
                Selvä ratkaisu ja toiminnallisuus.
            </li>
        </ul>
    </li>
    <li>
        Käyttäjä pystyy valitsemaan tietokohteelle yhden tai useamman luokittelun. Mahdolliset luokat ovat tietokannassa.
        <ul>
            <li>
                Käyttäjä voi luokitella ostoslistoja esimerkiksi sen perusteella koskeeko lista ruokakauppaa tai jotain muuta.
            </li>
        </ul>
    </li>
    <li>
        Käyttäjä pystyy lähettämään toisen käyttäjän tietokohteeseen liittyen jotain lisätietoa, joka tulee näkyviin sovelluksessa.
        <ul>
            <li>
                Käyttäjät voivat kommentoida heille jaettuja ostoslistoja ja muokata niitä.
            </li>
        </ul>
    </li>
</ul>

<hr>
<h2><b>Käyttöohjeet</b></h2>
<p>Käyttöönotto:</p>
<ul>
<li>Lataa repositorion tiedostot</li>
<li>Navigoi ladattuun hakemistoon</li>
<li>Suorita komento <code>python3 -m venv .</code></li>
<li>Suorita komento <code>source ./bin/activate</code></li>
<li>Suorita komento <code>pip3 install flask</code></li>
<li>Luo <code>config.py</code> tiedosto ja aseta sille sisällöksi <code>secret_key = [salainen avain]</code></li>
<li>Voit luoda salaisen avaimen esimerkiksi Pythonin secrets moduulilla</li>
<li>Suorita komento <code>flask run</code></li>
<li>Mene selaimella sovelluksen osoitteeseen</li>
</ul>

<p>Tietokannan alustaminen (varoitus: kaikki tiedot katoaa):</p>
<ul>
<li>Suorita komento <code>./purge_database.sh</code></li>
</ul>

<p>Suuren tietomäärän testaaminen (varoitus: kaikki tiedot katoaa):</p>
<ul>
<li>Suorita komento <code>./set_DEV_mode.sh</code></li>
<li>Suorita komento <code>python3 seed.py</code></li>
<li>Suorita komento <code>flask run</code></li>
<li>Mene selaimella sovelluksen osoitteeseen</li>
<li>Kirjoita nyt käyttäjätunnuskenttään esimerkiksi <code>user9</code>, salasanakentän voi jättää tyhjäksi, koska tässä testitilassa sovellus toimii ilman salasanaa</li>
<li>Testauksen lopuksi suorita komento <code>./set_PROD_mode.sh</code> (ja <code>./purge_database.sh</code>, jos haluat tyhjentää tietokannan testidatasta)</li>
</ul>

<hr>
<h2><b>Sovelluksen suorituskyky</b></h2>
<p>Sovelluksen tietokanta käyttää indeksejä ja tuotehakutoimminnon vasteaika osoitettu kuvassa <i><code>application_response_speed.png</code></i>.</p>

<hr>
<h2><b>Sovelluksen vaihe:</b></h2>
2.2.2025
<br>
<h4>Tavoitteet ja tila</h4>
<ul>
    <li>
        Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
        <ul><li>
            Toteutettu
        </ul></li>
    </li>
    <li>
        Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita.
        <ul><li>
            Lisääminen toteutettu. Muokkaus ja poistaminen vielä vaiheessa.
        </ul></li>
    </li>
    <li>
        Käyttäjä näkee sovellukseen lisätyt tietokohteet.
        <ul><li>
            Toteutettu
        </ul></li>
    </li>
    <li>
        Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella.
        <ul><li>
            Tämä ominaisuus vielä vaiheessa.
        </ul></li>
    </li>
</ul>

Sovelluksen puutteet ja tarvittavat korjaukset:
<ul>
    <li><s>tietokohteiden muokkauksen ja poistamisen viimeistely</s></li>
    <li><s>hakutoiminnon toteuttaminen</s></li>
    <li><s>sovelluksen tietoturvan parantaminen (erityisesti pitää estää luvaton listojen katselu ja muokkaus)</s></li>
    <li><s>yleinen bugien etsintä ja reunatapaustilanteiden varmistaminen</s></li>
</ul>
