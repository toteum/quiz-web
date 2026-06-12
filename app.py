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


# 🔥 DOMANDE GLOBALI (NON IN SESSIONE)
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
    return quiz()


@app.route("/quiz")
def quiz():
    i = session.get("i", 0)

    # 🏁 FINE QUIZ
    if i >= len(DOMANDE):
        return redirect(url_for("termina"))

    return render_template(
        "index.html",
        domanda=DOMANDE[i],
        numero=i + 1,
        totale=len(DOMANDE),
        session=session
    )


@app.route("/risposta", methods=["POST"])
def risposta():
    i = session["i"]
    d = DOMANDE[i]

    selezionate = request.form.getlist("opzione")

    corretto = sorted(selezionate) == sorted(d["corrette"])

    if corretto:
        session["punteggio"] += 1
        session["ultimo_risultato"] = "corretto"
    else:
        session["ultimo_risultato"] = "sbagliato"

    session["ultima_corrette"] = d["corrette"]
    session["risposto"] = True
    session["ultime_selezionate"] = selezionate

    # 🔥 SALVATAGGIO STORICO
    corrette_idx = d["corrette"]
    selezionate_idx = selezionate

    corrette_testo = [d["opzioni"][int(i) - 1] for i in corrette_idx]
    selezionate_testo = [d["opzioni"][int(i) - 1] for i in selezionate_idx]

    session["storico"].append({
        "domanda": d["domanda"],
        "corrette": corrette_testo,
        "selezionate": selezionate_testo,
        "corretto": corretto
    })

    return quiz()


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
    session.clear()
    return home()

@app.route("/termina")
def termina():
    storico = session.get("storico", [])
    punteggio = session.get("punteggio", 0)

    return render_template(
        "review.html",
        storico=storico,
        punteggio=punteggio,
        totale=len(storico)
    )


if __name__ == "__main__":
    app.run()