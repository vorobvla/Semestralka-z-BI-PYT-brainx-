=========== Popis semestrální práce z BI-PYT ===========
Vladimir Vorobyev (vorobvla), červen 2015

--------------------------------------------------------
Daný program slouží jako interpretr programů v jazycích brainfuck,  brainloller a braincopter i jako překladač z brainfucku do brainlolleru nebo braincopteru a  z  brainlolleru nebo braincopteru do brainfucku. 
Program je napsán a otestován v jazyce Python v. 3.4. S verzemi jazyka 2.x program nebude korektně fungovat. Funkčnost s verzemi 3.x (kromě 3.4) nebyla otestována.

Funkcionalita odpovídající požadavkům:
*	interpretr podporuje rozšíření # ( podle specifikace z zadání ) a rozšíření ! (v. detailnější popis implementace)
*	program implementuje varianty brainloller a braincopter pro čtení (v režimu interpretru – v. dále) a pro zápis (v režimu překladače)
*	program umí načíst brainfukovský kód (v. režim interpretru) z příkazové řadky, ze standardního vstupu (v interaktivním režimu), z textových souborů (s názvy končící postfixem „.b“)  a z souborů ve formátu PNG (obsahující kód ve variantě brainloller nebo braincopter)
*	program umí zapsat brainfukovský kód z PNG souborů (obsahující kód  ve variantě brainloller nebo braincopter) do  standardního výstupu nebo do textového souboru. (v. režim překladače)
*	program umí zapsat brainfukovský kód do PNG souborů (ve variantě brainloller nebo braincopter) do  standardního výstupu nebo do textového souboru. (v. režim překladače)

--------------------------------------------------------
Funkcionalita navíc:
*	Zápis brainlolleru ve formě spirály (--f2lc --bl-spiral)
		Překladač standardně zapisuje brainloller (a braincopter) v pořadí stejném jako na příkladu z přednášek. Dá se to uspořádaní změnit do uspořádání do spirály, které zkusím popsat následujícím schématem:
	-----------------V
	>--------------V |
	| >----------V | |
	| | >------V | | |
	| | | >--V | | | |
	X X X XXX< | | | |
	| | | ^----< | | |
	| | ^--------< | |
	| ^------------< |
	^----------------<

Kde symboly V < ^ > označují rotace IP doprava, X je NOP,  - | jsou ostatní instrukce.
Tuto funkčnost se dá využít požitím přepínače --bl-spiral u přepínače --f2lc ( příklad syntaxe: --f2lc --bl-spiral -i input_bf_file [input_png_file] -o output_bl_bc_file ). Je-li daný přepínač nastaven, výstupem překladače bude vždy obrázek v brainlolleru (a v spirálové podobě). Výskytuje-li se zároveň argument input_png_file, program ho ignoruje.
*	Vstup brainfuckovského programu ze souboru nebo od uživatele v interaktivním režimu (--prin|--program-input [program_input_file] v režímu interpretru)
		V režimu interpretru se dá zadát vstup prográmu pomocí přepínače --prin|--program-input [program_input_file]. Vstup bude načítan ze souboru, jehož název je v argumentu program_input_file. Nebude-li daný argument uveden, užívateloví bude nabídnuto uvést vstup v interaktivním režímu (podobně tomu, ják se uvádí kód 
ve variantě bez argumentů). Je-li interpretr už běží v intaratívním řežímu, úžívatel zjíská možnost úvest vstup poté když uvedé kód prográmu. Je-li vstup prográmu je nástaven pomocí tohoto přepínače, vstup, který je úveden ve pográmovém kódu (pomocí !) je ignorován.
*	Možnost aplikovat operace mod 128 na výstup programu (--o128, v obou režimu interpretru)
		Jelikož data v paměťových buňkách mohou být v rozsahu od 0 255 a program pro kování vstupu používá ASCII, mohou se nastávat chyby, pokud do výstupu
se dostala hodnota, kterou ASCII není schopno rozkódovat. Přepínač interpretru --o128 slouží k tomu aby se dalo této situací vyhnout. Zaručuje, že nad každou hodnotou,
která přichází na výstup, bude provedena operace mod 128, tedy výstup vždy bude rozkódovatelný. 
*	Generování programů v brainfucku. (--gen-bf | --gen-bl [text], bez žádných dalších parametrů)
		Jednoduchý generátor braifukovského kódu. Vygeneruje program v brainfucku, který bude vypisovat zadaný text. Není-li text uveden, uživatelovi bude nabídnuto uvést ho za běhu programu (interaktivní režim). Varianta --gen-bf vypíše program do standardního výstupu a zapíše jeho podobu v jazyce brainloller do PNG souboru s názvem T.bl.png kde T je prvních (nejvíce) 20 znaku výpisu programu. Samotný program vždy využívá právě dvě paměťové buňky. Je-li počet instrukcí, které se má provádět nad stejnou buňkou je příliš velký, přepíše je pomocí cyklu tak, aby jak jeho tělo tak i počet inkrementací před jeho zavoláním byli co nejmenší (v ideálním případě by se rovnali). Jelikož daná funkcionalita nespadá do kompetence žádného režimu, měla by být přidaná režimu novému, který by se odlišoval od ostatních dvou. Autorovi nezbývá čas ani energie pro to aby to slušně odladil a implementoval, takže on jenom upozorní že do parametrů programu by měl byt zadán jenom jeden z uvedených přepínačů a bez žádných kombinací s parametry z jiných režimů. V opačném případě korektní funkčnost programu není zaručená.
--------------------------------------------------------

Detailnější popis programu:

*	Spuštění
		Program se dá spouštět ve dvou režimech: jako interpretr („Interpreter mode“) a jako překladač (v helpu je uveden jako „Translator mode“). Parametry příkazové řádky pro teto dvě varianty se odlišují.  Ovšem v obou režimech jsou vlídní přepínače -t i --test  (aktivace výpisu ladící informace ve formátu, určeném v zadání; v režimu překladače v  výpisu budou mizet informace o paměti (#memory  a #memory pointer), protože program se v daném režimu nespustí a tedy stav paměti není zajímavý pro uživatele), -h i --help (výpis pomocné informace) a  --pnm i --pbm (zápis vstupních/výstupních obrázků do PNM souborů ve formátu uvedeném v zadaní a s názvy input_image_in_pnm resp output_image_in_pnm). Vyskytují-li se v parametrech nespecifikované argumenty a přepínače, opakující se  přepínače nebo parametry, které jsou příslušné různým režimům, (většinou) se vyskytne výjimka nebo parametr bude (měl by byt) ignorován. 

  		Režim interpretru:
			Využíti:  brainx [__zdrojový_soubor__ | "__kód_v_brainfucku__"] [-t|--test] [-m|memory b'__počáteční_stav_paměti__'] [-p|--memory_pointer_position __pozice_paměťového_ukazatele__] [--pnm|--pbm] ['--prin'|'--program-input' [__vstup_programu__]] [-h|--help] [--o128]
			Varianta bez argumentů načítá program ze standardního vstupu (v interaktivním režimu). Ovšem přepínače v daném případě budou platit (není to úplně podle zadání ale to připadá autorovi praktičtější, lze tedy opravit nastavení i pro program uvedený  v interaktivním režimu) 
			První argument  je název zdrojového souboru. Pokud název končí příponou „.b“ je vnímán jako textový soubor s programem v brainfucku tedy program se pokusí tento kód spustit. O opačném případě soubor je vnímán jako (možný) PNG obrázek a program se pokusí spustit kód, který získá překladem daného obrázku do brainfucku. Mimořádným případem je argument v uvozovkách, který bude vnímán jako spustitelný program v brainfucku (podle zadání)
			Argument přepínače -m (--memory) je binární řetězec popisující počáteční stav paměti programu.
			Argument přepínače -p (--memory-pointer) je počáteční pozice paměťového ukazatele. Je-li nastaven na pozice mimo paměti (tedy větší než délka paměti zmenšená o 1) program vyhodí výjimku. 
			Argument --prin | --program-input [program_input_file] nastavuje programový vstup ze souboru nebo od uživatele. Podrobněji v. Funkcionalita navíc.
			Přepínač --o128 provedení operace mod 128 nad výstupem ( v. Funkcionalita navíc).

		Režim překladače:
			Využíti: brainx [-t|--test] [--pnm|--pbm] [-h|--help] ( --lc2f __vstupní_bl_nebo_bc_soubor__ [__výstupní_bf_soubor__] | --f2lc [--bl-spiral] -i input_bf_file [input_png_file] -o output_bl_bc_file )
			--lc2f  přeloží brainlollerovský nebo braincopterovský kód  ze vstupního obrázku do brainfucku. Výsledek zapíše do výstupního souboru, pokud je uveden (přepíše soubor s daným jménem je-li existuje, v opačném případě vytvoří nový). Pokud název výstupního souboru uveden není, výsledek se vypisuje do standardního vstupu. Jazyk vstupního obrázku program rozpoznává sám (plodě analýzy barev jako je uvedeno v zadání). Název výstupního souboru by měl  končit  příponou „.b“, ovšem pokud uživatel uvede název jinak, program to automatické opraví (tedy je zaručeno že nový/přepsaný soubor bude mít název končící na „.b“) 
			--f2lc přeloží brainfuckovský kód do obrázku s programem v brainlolleru (pokud název vstupního PNG souboru není uveden) nebo v braincopteru (v opačném případě). Předpokládá se že název souboru s kódem v brainfucku končí na „.b“ ale není-li tomu tak, program tuto chybu opraví (stejně jako u --lc2f). Je-li název v vstupního PNG souboru je uveden, jeho obsah bude použit u překladu do braincopteru. Program výpise debagovací  informace, narazí-li  na instrukce # v brainfuckovském kódu. Program ignoruje nepovinné přepínače uvedené-li po daném příkladu (nemá to praktický smysl, to je bug). --bl-spiral zapíná zápís brainlollerovského obrázku do spirálové podoby (v. Funkcionalita navíc)

*	Ukončení
		Po úspěšném běhu program vrátí kód 0 a vepíše výsledek běhu spušteného programu (jedná-li se o interpretru) a výsledek překladu nebo nic (u překladače, záleží na parametrech). Pokud se během programu pokusilo zpracovat soubor, který není ani textem ani PNG nebo soubor, který obsahuje nějakou povinni hlavičku kromě IHDR, IDAT a IEND program se chová podle zadání (vyhodí příslušnou výjimku a ukončí se s příslušným kódem). V jiném případě vyhazuje výjimky které se  objevili a končí se s kódem 1.

*	Implementace
		Struktura projektu
			Projekt  se skládá z modulů  graphics, lang a maintainance a z souboru __main__.py v kořenovém modulu projektu. Modul graphics zodpovídá za práce s obrázky, tedy za jejích převod z souboru do podoby (třída image), se kterou pracuje modul lang a zpátky. Modul lang obsahuje samotnou implementace interpretru a překladače. Modul maintainance se zabývá zapracováním argumentů a logováním. __main__.py zajišťuje   fungování celého programu s použitím funkcionality ostatních části projektu.
		Interpretr (/lang/interpreter.py)
			Paměť
			Paměťové buňky se číslují od 0. Buňky jsou jednobajtové, při přetečení nablívají hodnotu, která je výsledkem operace modulo 256. Při pohybu ukazatele doprava paměť se rozšiřuje je-li to potřeba (ovšem vždy o jednou buňku). Nové buňky obsahuji hodnotu 0. Pokud ukazatel je na pozice 0 a pokusilo se ho posunout doleva,  stav interpretru se nezmění (tedy daný pokus nebude mít žádné dopady).  Vykonání programu se začíná s jedinou paměťovou buňkou obsahující 0 s ukazatelem nastaveném na ní (není-li nastaveno jinak)
			Vstup
			Vstup se odliší pomoci instrukce ! . Část kódu od prvního výskytu této instrukce do konce programu je brána jako vstup.  Instrukce , (čtení ze vstupu) nezapisuje nic do buňky pokud se ze vstupu nedá nic načíst.
			Výstup
			Výstup programu se aktualizuje jakmile se program narazí na instrukce . (výpis do výstupu). Pro dekódování výstupu se používá ASCII, proto vyskytují-li se v něm hodnoty 128 -- 255, vyhodí se výjimka při dekódování. Aby se tomu vyhnout lze použít přepínač --o128 (v. Funkcionalita navíc)
			Cykly
			Před spuštěním kódu interpretr ho analyzuje s tím aby odhalil cykly a zapsal je do slovníků v podobě {pozice v kódu, kde začíná cyklus} : {pozice v kódu, kde začíná cyklus}  (případně naopak). Potom, u vykonání kódu, pří pořečtění instrukce začátku nebo konce cyklu a při splnění souvisejících podmínek (tedy zda je potřeba skočit na konec/začátek cyklu) interpretr mění aktuální pozice v kódu na příslušnou pozice zapsanou v příslušném slovníku (pod klíčem který se rovná aktuální pozici). Samotná analýza probíhá pomocí zásobníku (tedy pomoci seznamu, který se chová jako zásobník). Pozice začátku cyklu se ukládá na vrchol, na konci cyklu začátek příslušného cyklu se vyzvedne ze zásobníku. Při pokusu vyzvednutí z prázdného zásobníku nebo není-li zásobník na konce analýzy prázdny zaznamenají chybný konec nebo začátek cyklu. 
			Další poznámky
			Pokud kód ze třeba získat z obrázku (brainloller nebo braincopter), zvolá se pro tento účel překladač. Pak se spustí přeložený brainfuckovský kód. 
			Za běhu programu zpracování symbolu z kódu který není ani vstupem ani instrukce ani bílým znakem končí výjimkou (neznámá instrukce). Bílé znaky se ignoruji (ve vstupu ale se zachovávají platnost).	
			Pokud na konce výkonné částí programu je #		

		Překladač (/lang/translater.py)
		Z brainlolleru nebo braincopteru do brainfucku
		Překládá se data obrázku poskytované objektem třídy Image (v. dále). Výsledek se ukládá do řetězce.
		Z brainfucku do brainlolleru nebo braincopteru.
		Překládá se jenom část kódu, která není vstupem. Instrukce ! a # se nepřekládají. Při přečtení  na instrukce # lajdající informace se vypisuje podle zadání (ovšem bez informace o paměti a ukazatele, která v daném kontextu nemá smysl). Pokud na obrázku po překladu programu zbývá se nezakódovávané pixely, této pixely se kódují tak, aby označovali instrukce No Operation. Pokud velikost původního obrázku (jedná se o braincopter) není postačující pro překlad (počet pixelu je menší než počet instrukcí, které je třeba zapsat), obrázek se rozšiřuje dolu na jeden řádek, který je zaplněn černými pixely. Zápis do obrázku se provádí stejným směrem jako třeba na obrázku z textů (tedy zleva doprava do konce řádku, dvakrát se otočí doprava s zápisem příslušných operací, zprava doleva do začátku řádku, zase otočí se dvakrát doprava … ). Kód se překládá do objektu třídy image (buď na začátku (skoro) prázdného pro variantu brainloller nebo obsahujícího data ze vstupního obrázku pro variantu braincopter)

	Třída Image (graphics/image.py)
	Obsahuje data obrázku v podobě, vhodnou pro zpracování uvnitř programu (tedy jako dvojrozměrné  pole tuplů, reprezentujících jednotlivé pixely).  Poskytuje funkcionalitu pro pohodlnou práce s polem (posun ukazatele na aktuální pozice, čtení, zápis, směr posunu, změna směru apod. ) a pro překlad dat z pole do jiné podoby (do textové nebo do souboru). 

	Png Processor (graphics/png_processor.py)
	Zpracovává soubor s obrázkem. Kontroluje zda je soubor PNG, zda neobsahuje povinné chunky, které by obsahovat neměl, zda končí správně a zda data v něm je validní (tedy sedí-li CRC). Je-li nějaká z těchto podmínek je porušená hodí příslušnou výjimku. V opačném případě vytvoří objekt třídy Image reprezentující obrázek uložený v daném souboru.

	Logger (maintainance/logger.py)
	Zapíše potřebné ladící data do příslušného debagovaciho souboru.	

	Context (maintainance/context.py)
	Zpracovává vstupní parametry  programu a ukládá je do třídy Settings. 

	Další poznámky:
Autor psal  vše komentáře a commitovací zprávy v angličtině protože programuje právě v angličtině, to je jeho zvykem.  
