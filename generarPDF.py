from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def generarInforme(correcto, incorrecto):
    from reportlab.pdfgen import canvas

    informe = "INFORME GENERADO \n"
    informe += "REALIZADO CORRECTAMENTE: \n"

    for t in correcto:
        informe += "-" + t + "\n"

    informe += "ASPECTOS A MEJORAR: \n"

    for t in incorrecto:
        informe += "-" + t + "\n"

    c = canvas.Canvas("informe.pdf")
    c.setFont("Helvetica", 14)
    y = 750
    for line in informe.splitlines():
        c.drawString(100, y, line)
        y -= 20
    c.save()

    return informe


correcto = ["hola", "adios"]
incorrecto = ["f en el chat", "jeje"]
filename = "informe.pdf"


print(generarInforme(correcto, incorrecto))
