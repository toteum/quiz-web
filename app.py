from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import csv
import random

app = Flask(__name__)
app.secret_key = "chiave_segreta"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


def carica_domande():
    domande = []

    with open("domande.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for riga in reader:
            opzioni = riga["opzioni"].split(";")
            corrette_originali = riga["corrette"].split(";")

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

    random.shuffle(domande)
    return domande



DOMANDE = carica_domande()


@app.route("/")
def home():
    session["i"] = 0
    session["punteggio"] = 0
    session["storico"] = []
    session["risposto"] = False
    session["ultimo_risultato"] = None
    session["ultima_corrette"] = []
    session["ultime_selezionate"] = []
    session["modalita"] = None
    session.pop("domande_ritenta", None)
    return redirect(url_for("quiz"))


@app.route("/quiz")
def quiz():
    i = session.get("i", 0)
    domande = get_domande()

    if i >= len(domande):
        return redirect(url_for("termina"))

    return render_template(
        "index.html",
        domanda=domande[i],
        numero=i + 1,
        totale=len(domande),
        session=session
    )
def get_domande():
    if session.get("modalita") == "ritenta":
        return session.get("domande_ritenta", [])
    return DOMANDE


@app.route("/risposta", methods=["POST"])
def risposta():
    if session.get("risposto"):
        return redirect(url_for("quiz"))

    i = session["i"]
    domande = get_domande()

    if i >= len(domande):
        return redirect(url_for("termina"))

    d = domande[i]

    selezionate = request.form.getlist("opzione")

    corretto = set(selezionate) == set(d["corrette"])

    if corretto:
        session["punteggio"] += 1
        session["ultimo_risultato"] = "corretto"
    else:
        session["ultimo_risultato"] = "sbagliato"

    session["ultima_corrette"] = d["corrette"]
    session["risposto"] = True
    session["ultime_selezionate"] = selezionate

    corrette_testo = [
        d["opzioni"][int(x) - 1]
        for x in d["corrette"]
    ]

    selezionate_testo = [
        d["opzioni"][int(x) - 1]
        for x in selezionate
    ]

    storico = session.get("storico", [])

    storico.append({
        "domanda": d["domanda"],
        "opzioni": d["opzioni"],
        "corrette": corrette_testo,
        "selezionate": selezionate_testo,
        "corretto": corretto
    })

    session["storico"] = storico

    return redirect(url_for("quiz"))




@app.route("/next")
def next_question():
    session["i"] += 1
    session["risposto"] = False
    session["ultimo_risultato"] = None
    session["ultima_corrette"] = []
    session["ultime_selezionate"] = []

    return redirect(url_for("quiz"))


@app.route("/reset")
def reset():
    global DOMANDE
    DOMANDE = carica_domande()
    session.clear()
    return redirect(url_for("home"))

@app.route("/termina")
def termina():
    storico = session.get("storico", [])
    punteggio = session.get("punteggio", 0)
    n_sbagliate = len([x for x in session.get("storico", []) if not x["corretto"]])

    return render_template(
        "review.html",
        storico=storico,
        punteggio=punteggio,
        totale=len(storico),
        n_sbagliate = n_sbagliate
    )


@app.route("/review")
def review():
    filtro = request.args.get("filtro", "tutti")

    storico = session.get("storico", [])
    n_sbagliate = len([x for x in session.get("storico", []) if not x["corretto"]])

    if filtro == "corretti":
        storico = [x for x in storico if x["corretto"]]
    elif filtro == "sbagliati":
        storico = [x for x in storico if not x["corretto"]]

    return render_template(
        "review.html",
        storico=storico,
        punteggio=session.get("punteggio", 0),
        totale=len(session.get("storico", [])),
        filtro=filtro,
        n_sbagliate=n_sbagliate
    )


@app.route("/ritenta")
def ritenta():
    storico = session.get("storico", [])
    sbagliate = [e for e in storico if not e["corretto"]]

    if not sbagliate:
        return redirect(url_for("termina"))

    nuove_domande = []
    for entry in sbagliate:
        opzioni = entry["opzioni"][:]
        random.shuffle(opzioni)

        corrette_idx = [
            str(opzioni.index(c) + 1) for c in entry["corrette"]
        ]

        nuove_domande.append({
            "domanda": entry["domanda"],
            "opzioni": opzioni,
            "corrette": corrette_idx
        })

    random.shuffle(nuove_domande)

    session["domande_ritenta"] = nuove_domande
    session["i"] = 0
    session["punteggio"] = 0
    session["storico"] = []
    session["risposto"] = False
    session["ultimo_risultato"] = None
    session["ultima_corrette"] = []
    session["ultime_selezionate"] = []
    session["modalita"] = "ritenta"

    return redirect(url_for("quiz"))


if __name__ == "__main__":
    app.run()