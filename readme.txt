Python version: 3.10.0
Toate bibliotecile cu care am lucrat sunt in fisierul requirements.txt

Lansati fisierul index.py, am creat url pentru fiecare pas din conditii 
si tot am creat url pentru toti pasii intr-un url.(/adverts)
Url-ul (/adverts) descarca toate anunturile din contul Johny si deodata face 
verificari daca se diferintiaza de ceea ce avem in fisierul all_adverts.json 
sau in caz ca fisierul nu este atunci el scoate din MongoDB. Dupa ce descarca/citeste
datele se sorteaza anunturile dupa ID, din ceea ce avem in fisier/bd si din ceea 
ce am primit din API, dupa se face match pe fiecare id si daca un id nu este sau 
este in plus in fisier/bd atunci el se sterge/adauga, in caz ca este atunci se verfiica 
daca anuntul se diferentiaza de ceea ce am primit din API si dupa, daca este diferetena,
se face un update in MongoDB. Inainte de a face un insert/update se foloseste decorator-ul 
creat care converteste valuta din 'EUR' in 'MDL', se converteste in lista currencies din anunt 
care unitatea este in euro. Datele despre cursul valutare de descarca de pe site https://www.bnm.md/
si se salveaza intr-un fisier, current_currency.json. La urma functia "check_adverts_changes" returneaza 
toate anunturile si le scriem pe pagina in format .json din url-ul (/adverts).

La lansarea step-ului posibil sa necesite timp pentru descarcarea anunturilor cu API.

Mersi,
Victor