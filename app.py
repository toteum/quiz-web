from flask import Flask, render_template, request, session
import csv
import random

app = Flask(__name__)
app.secret_key = "chiave_segreta"


def carica_domande():
    domande = []
    with open("domande.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for riga in reader:
            opzioni = riga["opzioni"].split(";")
            corrette_originali = riga["corrette"].split(";")

            # trasforma in coppie (indice originale, testo)
            coppie = list(enumerate(opzioni, start=1))

            random.shuffle(coppie)

            nuove_opzioni = []
            nuove_corrette = []

            for new_index, (old_index, testo) in enumerate(coppie, start=1):
                nuove_opzioni.append(testo)

                if str(old_index) in corrette_originali:
                    nuove_corrette.append(str(new_index))

            domande.append({
                "domanda": riga["domanda"],
                "opzioni": nuove_opzioni,
                "corrette": nuove_corrette
            })

    random.shuffle(domande)  # 🔥 shuffle domande
    return domande


@app.route("/")
def home():
    session["domande"] = carica_domande()
    session["i"] = 0
    session["punteggio"] = 0
    session["risposto"] = False
    session["ultimo_risultato"] = None
    session["ultima_corrette"] = []
    return quiz()


@app.route("/quiz")
def quiz():
    i = session.get("i", 0)
    domande = session.get("domande", [])

    if i >= len(domande):
        return f"""
        <div style="text-align:center; margin-top:100px;">
            <h2>🏁 Quiz completato!</h2>
            <h3>Punteggio finale: {session['punteggio']} / {len(domande)}</h3>

            <a href="/reset" class="btn btn-primary mt-4">
                🔄 Riprova il quiz
            </a>
        </div>
        """

    return render_template(
        "index.html",
        domanda=domande[i],
        numero=i + 1,
        totale=len(domande),
        session=session
    )


@app.route("/risposta", methods=["POST"])
def risposta():
    i = session["i"]
    domande = session["domande"]
    d = domande[i]

    selezionate = request.form.getlist("opzione")

    if sorted(selezionate) == sorted(d["corrette"]):
        session["punteggio"] += 1
        session["ultimo_risultato"] = "corretto"
    else:
        session["ultimo_risultato"] = "sbagliato"

    session["ultima_corrette"] = d["corrette"]
    session["risposto"] = True
    session["ultime_selezionate"] = selezionate

    return quiz()


@app.route("/next")
def next_question():
    session["i"] += 1
    session["risposto"] = False
    session["ultimo_risultato"] = None
    session["ultima_corrette"] = []
    session["ultime_selezionate"] = []

    return quiz()

@app.route("/reset")
def reset():
    session.clear()
    return home()


if __name__ == "__main__":
    app.run()