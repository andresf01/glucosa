#!/usr/bin/python
#-*- coding: utf-8 -*-

from datetime import date
from datetime import timedelta
import time

from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,landscape,inch
from reportlab.platypus import Table, TableStyle

operaciones = {0:'ANTES DE APLICAR INSULINA 8PM', 1: 'A LAS 3AM', 2:'AYUNAS', 3:'2 HORAS DESPUES DEL ALMUERZO'}
weekday = {0:'LUNES', 1:'MARTES', 2:'MIERCOLES', 3:'JUEVES', 4:'VIERNES', 5:'SABADO', 6:'DOMINGO'}

months = {1:'ENERO', 2:'FEBRERO', 3:'MARZO', 4:'ABRIL', 5:'MAYO', 6:'JUNIO', 7:'JULIO', 8:'AGOSTO', 9: 'SEPTIEMBRE', 10:'OCTUBRE', 11:'NOVIEMBRE', 12:'DICIEMBRE'}

myCanvas = canvas.Canvas("glucosa.pdf", pagesize=landscape(letter))

def getInfo():
  global operaciones
  print ("Que año desea empezar:")
  anio = input()
  print ("Que mes desea empezar:")
  mes = input()
  print ("Que día desea empezar:")
  dia = input()
  print ("Seleccione en que momento desea iniciar (número): ")
  print (operaciones)
  start = int(input())
  fecha = date(int(anio), int(mes), int(dia))
  # start = 2
  print ("Cuántos meses desea generar en total?")
  cantidad = int(input());
  mes_before = fecha.month
  iterator = 0
  elements = []

  while iterator < cantidad:
    dom = str(fecha.day)
    dow = weekday[fecha.weekday()]
    op = (operaciones[start % len(operaciones)])
    tmp = [dom ,dow, op]
    elements.append(tmp)
    start += 1
    # print ("{} == {}".format(fecha.month, iterator))
    fecha = fecha + timedelta(days=3)
    if fecha.month != mes_before:
      iterator += 1
      mes_before = fecha.month
    pass

  return elements, [mes,anio]
  pass

def generatePDF(month, anio, elements):
  global months, myCanvas
  

  # Crear documento de tamaño carta en orientación horizontal
  width, height = landscape(letter)

  tableMaxWidth = width-2*inch
  contentColWidths = [tableMaxWidth*0.12, tableMaxWidth*0.16, tableMaxWidth*0.56, tableMaxWidth*0.16]
  
  # header = [[months[month]]]
  newMonth = int(month)
  newAnio = int(anio)
  day_before = int(elements[0][0])
  data = []

  for item in elements:
    if (day_before > int(item[0])):
      
      header = [[months[newMonth]]]
      # print (data)
      generatePage(width, height, tableMaxWidth, contentColWidths, header, data, newAnio)
      data = []
      newMonth += 1
      if newMonth > 12:
        newMonth = 1
        newAnio += 1
      pass
    day_before = int(item[0])
    data.append(item)

  header = [[months[newMonth]]]
  generatePage(width, height, tableMaxWidth, contentColWidths, header, data, newAnio)

  myCanvas.save()

def generatePage(width, height, tableMaxWidth, contentColWidths, header, data, anio):
  global myCanvas
  subheader = [['FECHA', 'DIA', '', 'RESULTADO']]

  myCanvas.setLineWidth(.3)
  myCanvas.setFont('Helvetica', 10)

  # For header function require(myCanvas, month)

  table = Table(header, colWidths=tableMaxWidth)

  table.setStyle(TableStyle([
    ('VALIGN', (0,0), (0,0), 'MIDDLE'),
    ('ALIGN', (0,0), (0,-1), 'CENTER'),
    # ('GRID', (0,0), (-1,-1), 0.25, colors.black),
    ('FONTSIZE', (0,0), (0,0), 22),
    # ('BOTTOMPADDING', (0,0), (0,0), 18)
    ]))


  table.wrapOn(myCanvas, width, height)
  table.drawOn(myCanvas, 1 * inch, 7.5 * inch)

  table = Table(subheader, colWidths=contentColWidths)

  table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    # ('GRID', (0,0), (-1,-1), 0.25, colors.black),
    ('FONTSIZE', (0,0), (-1,-1), 14),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

  table.wrapOn(myCanvas, width, height)
  table.drawOn(myCanvas, 1 * inch, 7 * inch)


  count = 0
  for item in data:
    item.append('')
    count += 1
    table = Table([item], colWidths=contentColWidths)

    table.setStyle(TableStyle([
      ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
      ('ALIGN', (0,0), (0,0), 'CENTER'),
      ('GRID', (0,0), (-1,-1), 0.25, colors.black),
      ('FONTSIZE', (0,0), (-1,-1), 14),
      ('BOTTOMPADDING', (0,0), (-1,-1), 10),
      ]))

    table.wrapOn(myCanvas, width, height)
    table.drawOn(myCanvas, 1 * inch, (7-0.5*count) * inch)

    pass

  # Signature
  myCanvas.drawString( width-1*inch, height-0.5*inch, "{}".format(anio))
  myCanvas.drawString( width-2*inch, 0.5*inch, "Developed by andresF01")

  myCanvas.showPage()
  pass

elements, fech = getInfo()
# print (mes)
generatePDF(fech[0], fech[1], elements)
