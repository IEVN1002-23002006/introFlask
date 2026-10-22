from flask import Flask, render_template, request

app=Flask(__name__)

@app.route("/")
def index():
    titulo ='Hola!'
    lista=['Luis','Paco','Pedro']
    return render_template("index.html",titulo=titulo, lista=lista)

@app.route("/hola")
def hola():
    return"<h3> Saludo desde Hola </h3>"

@app.route("/user/<string:user>")
def user(user):
    return "Hola " + user

@app.route("/numero/<int:n>")
def numero(n):
    return "Numero: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return 'ID: {} nombre: {}'.format(id,username)

@app.route("/suma/<float:n1>/<float:n2>")
def func(n1,n2):
    return "lasuma es: {}".format(n1+n2)


@app.route("/cinepolis", methods=["GET", "POST"])
def cinepolis():
    nombre = ""
    compradores = 0
    tarjeta = "no"
    boletos = 0
    total = 0
    mensaje = ""

    if request.method == "POST":
        nombre = request.form.get("nombre")
        compradores = int(request.form.get("compradores"))
        tarjeta = request.form.get("tarjeta")
        boletos = int(request.form.get("boletos"))

        if compradores <= 0 or boletos <= 0:
            mensaje = "Ingresa cantidades validas"

        elif boletos > compradores * 7:
            mensaje = "No puedes comprar mas de 7 boletos por persona"

        else:
            total = boletos * 12

            if boletos > 5:
                total = total * 0.85

            elif boletos >= 3:
                total = total * 0.90

            if tarjeta == "si":
                total = total * 0.90

            mensaje = "Compra realizada correctamente"

    return render_template(
        "cinepolis.html",
        nombre=nombre,
        compradores=compradores,
        tarjeta=tarjeta,
        boletos=boletos,
        total=total,
        mensaje=mensaje
    )


@app.route("/distancia", methods=["GET","POST"])
def distancia():
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    dist = 0
    
    if request.method == "POST":
        x1 = float(request.form.get("x1", 0))
        y1 = float(request.form.get("y1", 0))
        x2 = float(request.form.get("x2", 0))
        y2 = float(request.form.get("y2", 0))
        
        dist = (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5

    return render_template("distancia.html", x1=x1, y1=y1, x2=x2, y2=y2, dist=dist)

@app.route("/operasbas", methods=["GET","POST"])
def operasbas():
    n1=0
    n2=0
    rest=0
    operacion=""
    if request.method=="POST":
        n1=request.form.get("n1")
        n2=request.form.get("n2")
        if request.form.get("operacion")=="suma":
            rest=float(n1)+float(n2)
        

    return render_template("operasbas.html", n1=n1, n2=n2, rest=rest)

if __name__ == "__main__":
    app.run(debug=True)

