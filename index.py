from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Usuario de prueba
USUARIO = "admin"
PASSWORD = "1234"


@app.route("/", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        usuario = request.form.get("usuario")
        contraseña = request.form.get("contraseña")

        if usuario == USUARIO and contraseña == PASSWORD:
            return redirect(url_for("inicio"))
        else:
            error = "Usuario o contraseña incorrectos"

    return render_template("base.html", error=error)


@app.route("/inicio")
def inicio():
    return render_template("inicio.html")


@app.route("/cantina")
def cantina():
    return render_template("cantina.html")


@app.route("/sponsors")
def sponsors():
    return render_template("sponsors.html")


if __name__ == "__main__":
    app.run(debug=True)