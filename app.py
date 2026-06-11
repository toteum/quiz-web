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

        storico = session.get("storico", [])

        html = f"""
        <div style="max-width:800px; margin:50px auto; font-family:Arial;">
            <h2>🏁 Quiz completato!</h2>
            <h3>Punteggio: {session['punteggio']} / {len(DOMANDE)}</h3>
            <hr>
        """

        for idx, item in enumerate(storico, start=1):

            esito = "✅" if item["corretto"] else "❌"

            html += f"""
            <div style="margin-bottom:20px; padding:10px; border:1px solid #ccc; border-radius:10px;">
                <b>{idx}. {item['domanda']}</b>
                <p>Esito: {esito}</p>
                <p><b>Risposte corrette:</b> {", ".join(item['corrette'])}</p>
                <p><b>Tue risposte:</b> {", ".join(item['selezionate'])}</p>
            </div>
            """

        html += """
            <a href="/reset" class="btn btn-primary">🔄 Riprova quiz</a>
        </div>
        """

        return html

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

    return quiz()


@app.route("/reset")
def reset():
    session.clear()
    return home()


if __name__ == "__main__":
    app.run()