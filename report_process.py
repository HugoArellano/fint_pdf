#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 12:45:39 2022

@author: hugoarellano
"""

#Replace path with github path
def emoji_selector(my_list):
    'Give the emoji path'
    if my_list[0] < 40:
        emoji = 'ft_automated_pdf/danger.png'
    elif my_list[0] < 80:
        emoji = 'ft_automated_pdf/warning.png'
    else:
        emoji= 'ft_automated_pdf/cool.png'
    
    return emoji


def color_selector(my_list):
    '''Define un color según el score obtenido'''
    if my_list[0] < 40:
        color_selected = 'rgb(255,102,102)'
    elif my_list[0] < 80:
        color_selected = 'rgb(255,255,104)'   
    else:
        color_selected = 'rgb(111,249,123)'
    return color_selected


def calibration_annot(my_list, area):
    """Prove el número para calibrar la anotación porcentual
    con el eje x, en función si es de uno o dos dígitos"""
    
    if area == 'deuda':
        if my_list[0] < 10:
            cal_params = 0.080
        else:
            cal_params = 0.055

    
    elif area == 'inversion':
        if my_list[0] < 10:
            cal_params = 0.915
        else:
            cal_params = 0.945
    
    
    return cal_params


def statement_selector(my_list,area):
    '''Define una frase según el score obtenido'''
    
    if area == 'global':
        if my_list[0] < 40:
            statement = '¡Tu futuro te está llamando!, dice que necesitas corregir el rumbo antes de que sea demasiado tarde, tal vez el camino sea largo, pero nosotros estaremos contigo en cada paso, hasta que logres un bienestar financiero.'
        elif my_list[0] < 80:
            statement = '¡No dejes pasar más tiempo!, estás en el mejor momento para empezar a hacer los ajustes necesarios y poner tus finanzas bien fit. Nosotros estaremos ayudándote mano a mano para que logres tu libertad financiera.'
        else: 
            statement = 'Felicidades, vemos que el manejo general de tus finanzas es bueno. Sin duda estás formando un buen patrimonio, en FinT, estaremos encantados de apoyarte a que logres un brillante futuro financiero.'
    
    elif area == 'deuda':
        if my_list[0] < 40:
            statement = 'No hay mal que dure 100 años, trabajemos en resolver el problema y en tomar mejores decisiones.' 
        elif my_list[0] < 80:
            statement = '¡Cuidado!, El mal uso de la deuda dificulta tu consolidación financiera y el cumplimiento futuro de metas.'
        else:
            statement = '¡Bien hecho! Estás utilizando la deuda de manera responsable. ¿Damos el siguiente paso?'
    
    elif area == 'ahorro':
        if my_list[0] < 40:
            statement = '¡Ten mucho cuidado!, Los bajos niveles de ahorro comprometen tu calidad de vida futura.'
        elif my_list[0] < 80:
            statement = 'Trabajemos en tu presente para mejorar tu futuro, el ahorro es un factor clave para alcanzar tus metas, no lo dejes para después.'
        else:
            statement = '¡Felicidades! Tienes buenas prácticas de ahorro, es momento de poner a trabajar tus recursos para alcanzar la libertad financiera.'
            
    elif area == 'inversion':
        if my_list[0] < 40:
            statement = 'Todo viaje comienza con un primer paso. Recuerda, las buenas inversiones son vitales para una calidad de vida envidiable.'
        elif my_list[0] < 80:
            statement = 'Ya diste algunos pasos dentro del mundo de las inversiones, pero aún queda mucho potencial por explotar.'
        else:
            statement = '¡Genial! Es bueno saber que estés trabajando en la consolidación de tu vida financiera. ¡Llevémosla a un nivel FinT!'
            
    elif area == 'somos_fint':
        statement = 'Nuestro Programa Wealth-Being® además de poner tus finanzas bien fit, te brinda el apoyo y el respaldo de todo un equipo de expertos para que florezcas en todas las áreas de tu vida'
    
    else:
        statement = 'Error: Por favor verifica el nombre de lista y área'
        
    return statement




def sort_opp(my_list):
    '''Asigna orden a los valores de la gráfica para que empiecen de manera uniforme'''
    if my_list[0] > 49:
        key_sort = True
    else:
        key_sort = False
    return key_sort



def annotation_in_chart(my_list):
    '''Coloca en texto el porcentaje que corresponde a cada gráfica'''
    annot = str(my_list[0]) + '%'
    return annot




def chart_params(df, df_col):
    """Construye los parametros para crear los circulos de progreso(gráficas)"""
    my_list = df[f'{df_col}'].astype(int).tolist()
    my_list.insert(1, 100 - my_list[0])
    
    labels = [f'{df_col}', f'reference_{df_col}']
    
    return my_list, labels



def global_chart(values, labels, annot_global, color_global):
    """Gráfica el score total"""
    import plotly.express as px
    
    fig = (px.pie(values=values, hole=0.7, color=labels, color_discrete_map={f'{labels[0]}': color_global, f'{labels[1]}':'rgb(166,166,166)'}))
    
    fig.update(layout_showlegend=False)
    
    fig.update_layout(
    annotations=[dict(text=annot_global, x=0.5, y=0.5, font=dict(color= "White", size =120),
                      showarrow=False)])

    #Añadimos fondo transparente para colocar en el reporte
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
    })
    
    #Tamaño para el pdf
    fig.update_layout(
        autosize=False,
        width=960,
        height=535)

    #Eliminamos las 
    fig.update_traces(textinfo='none')

    
    return fig



def area_charts(values, labels, area_colors, key_sort, area_annots, xaxis_deuda, xaxis_inversion):
    """Produce las graficas de las áreas convenidas para el reporte del test"""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    #Añade las tres categorias
    fig = make_subplots(rows=1, cols=3,
                   specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])
    
    fig.add_trace(go.Pie(labels=labels[0], values=values[0], hole=0.70, 
                    marker_colors = [area_colors[0] ,'rgb(166,166,166)'], sort = key_sort[0]),
             1,1)
    
    fig.add_trace(go.Pie(labels=labels[1], values=values[1], hole=0.70,
                    marker_colors = [area_colors[1], 'rgb(166,166,166)'], sort = key_sort[1]),
             1,2)

    fig.add_trace(go.Pie(labels=labels[2], values=values[2], hole=0.70,
                    marker_colors =[area_colors[2], 'rgb(166,166,166)'], sort = key_sort[2]),
             1,3)
    
    #removing default percentages
    fig.update_traces(textinfo='none')

    #removing frame of labels
    fig.update(layout_showlegend=False)
    
    #ading annotations in chart
    fig.update_layout(
        annotations=[dict(text=area_annots[0], x=xaxis_deuda, y=0.5, font=dict(color= "white", size =150),
                          showarrow=False),

                    dict(text=area_annots[1], x=0.5, y=0.5, font=dict(color= "white", size =150),
                         showarrow=False),

                    dict(text=area_annots[2], x=xaxis_inversion, y=0.5, font=dict(color= "white", size =150)
                         , showarrow=False)])
    
    #transparent backlayout
    fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'})

    fig.update_layout(
        autosize=False,
        width=1920,
        height=1071)

    return fig




def generate_pdf(user, nombre, area_chart, text_deuda, text_ahorro, text_inversion, global_chart, emoji, veredicto_txt, somos_fint_txt):
    """Genera documento pdf"""
    
    from fpdf import FPDF
    #general style
    pdf = FPDF(orientation='landscape', unit='mm', format = [285.75, 508])
    
    #user fonts
    pdf.add_font('Quicksand', '', '/Quicksand/static/Quicksand-Regular.ttf', 
             uni=True)

    pdf.add_font('Quicksand', 'B', '/Quicksand/static/Quicksand-Bold.ttf', 
             uni=True)

    #***FIRST_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_brand_1.png', x=0, y=0, w=508, h=285.75, type='', link='')
    
    #***SECOND_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_blank.png', x=0, y=0, w=508, h=285.75, type='', link='')
    
    #Adding font -- Title areas
    pdf.set_font('Quicksand', style='B', size=64)
    pdf.set_text_color(255,255,255)
    
    pdf.set_xy(0,15)
    pdf.cell(169, 20, txt='Deuda', align='C')
    pdf.cell(169, 20, txt='Ahorro',  align='C')
    pdf.cell(169, 20, txt='Inversión', align='C')
    
    #Adding font -- text areas
    pdf.set_font('Quicksand', style='', size=26)
    pdf.set_text_color(255,255,255)
    
    pdf.image(area_chart,x=0, y=-30, w=508, h=285.75)
    
    #text dedua
    pdf.set_xy(20, 195)
    pdf.multi_cell(140, 12, txt = text_deuda, border=False, align='J' )
    
    #Space
    pdf.set_xy(160,195)
    pdf.multi_cell(24, 12, border=False)
    
    #line
    pdf.set_xy(163,10)
    pdf.image('/ft_automated_pdf/line.png', h=185)
    
    ##Texto ahorro
    pdf.set_xy(184, 195)
    pdf.multi_cell(140, 12, txt = text_ahorro, border=False, align='J')
    
    #Space
    pdf.set_xy(324,195)
    pdf.multi_cell(24, 12, border=False)
    
    #line 2
    pdf.set_xy(327,10)
    pdf.image('/ft_automated_pdf/line.png', h=185)
    
    #Texto inversión
    pdf.set_xy(348, 195)
    pdf.multi_cell(140, 12, txt = text_inversion, border=False, align='J' )
    
    #***THIRD_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_blank.png', x=0, y=0, w=508, h=285.75, type='', link='')

    pdf.image(global_chart, x=-130, y=5, w=508, h=285.75, type='', link='')
    
    pdf.image(emoji,x=103, y=172, w=40, h=40)
    
    #Text - font
    pdf.set_font(family='Quicksand', style='B', size=45)
    pdf.set_text_color(245,72,1)
       
    #Blue square
    pdf.image('/ft_automated_pdf/white_square.png', x=260, y=25, w=230, h=110, type='', link='')
    pdf.image('/ft_automated_pdf/white_square.png', x=260, y=150, w=230, h=110, type='', link='')

    # El veredicto
    pdf.set_xy(263, 40)
    pdf.cell(223,15, txt='El Veredicto', border=False, align='C')

    #Somos Fint
    pdf.set_xy(263, 165)
    pdf.cell(223,15, txt='Somos FinT', border=False, align='C')

    pdf.set_font('Quicksand', style='', size=26)
    pdf.set_text_color(0,0,0)

    pdf.set_xy(269, 60)
    pdf.multi_cell(210,12, txt=veredicto_txt, border=False, align='J')

    pdf.set_xy(269, 185)
    pdf.multi_cell(210,12, txt=somos_fint_txt, border=False, align='J')

    #***FOURTH_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_program_4.png', x=0, y=0, w=508, h=285.75, type='', link='')
    
    #***FIFTH_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_slogan_5.png', x=0, y=0, w=508, h=285.75, type='', link='')
    
    #***SIXTH_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_coaches_6.png', x=0, y=0, w=508, h=285.75, type='', link='')
    
    #***SEVENTH_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_final_7.png', x=0, y=0, w=508, h=285.75, type='', link='')
    
    #***OUTPUT***
    output = pdf.output(f'fint_test_{str(user)}_{nombre.title()}.pdf')
    
    return output

def generate_pdf_2(user, nombre, area_chart, text_deuda, text_ahorro, text_inversion, global_chart, emoji, veredicto_txt, somos_fint_txt):
    """Genera documento pdf"""
    import streamlit as st
    from fpdf import FPDF
    #general style
    pdf = FPDF(orientation='landscape', unit='mm', format = [285.75, 508])
    
    #user fonts
    pdf.add_font('Quicksand', '', '/Quicksand/static/Quicksand-Regular.ttf', 
             uni=True)

    pdf.add_font('Quicksand', 'B', '/Quicksand/static/Quicksand-Bold.ttf', 
             uni=True)

    #***FIRST_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_brand_1.png', x=0, y=0, w=508, h=285.75, type='', link='')
    
    #***SECOND_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_blank.png', x=0, y=0, w=508, h=285.75, type='', link='')
    
    #Adding font -- Title areas
    pdf.set_font('Quicksand', style='B', size=64)
    pdf.set_text_color(255,255,255)
    
    pdf.set_xy(0,15)
    pdf.cell(169, 20, txt='Deuda', align='C')
    pdf.cell(169, 20, txt='Ahorro',  align='C')
    pdf.cell(169, 20, txt='Inversión', align='C')
    
    #Adding font -- text areas
    pdf.set_font('Quicksand', style='', size=26)
    pdf.set_text_color(255,255,255)
    
    pdf.image(area_chart,x=0, y=-30, w=508, h=285.75)
    
    #text dedua
    pdf.set_xy(20, 195)
    pdf.multi_cell(140, 12, txt = text_deuda, border=False, align='J' )
    
    #Space
    pdf.set_xy(160,195)
    pdf.multi_cell(24, 12, border=False)
    
    #line
    pdf.set_xy(163,10)
    pdf.image('ft_automated_pdf/line.png', h=185)
    
    ##Texto ahorro
    pdf.set_xy(184, 195)
    pdf.multi_cell(140, 12, txt = text_ahorro, border=False, align='J')
    
    #Space
    pdf.set_xy(324,195)
    pdf.multi_cell(24, 12, border=False)
    
    #line 2
    pdf.set_xy(327,10)
    pdf.image('ft_automated_pdf/line.png', h=185)
    
    #Texto inversión
    pdf.set_xy(348, 195)
    pdf.multi_cell(140, 12, txt = text_inversion, border=False, align='J' )
    
    #***THIRD_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_blank.png', x=0, y=0, w=508, h=285.75, type='', link='')

    pdf.image(global_chart, x=-130, y=5, w=508, h=285.75, type='', link='')
    
    pdf.image(emoji,x=103, y=172, w=40, h=40)
    
    #Text - font
    pdf.set_font(family='Quicksand', style='B', size=45)
    pdf.set_text_color(245,72,1)
       
    #Blue square
    pdf.image('/ft_automated_pdf/white_square.png', x=260, y=25, w=230, h=110, type='', link='')
    pdf.image('/ft_automated_pdf/white_square.png', x=260, y=150, w=230, h=110, type='', link='')

    # El veredicto
    pdf.set_xy(263, 40)
    pdf.cell(223,15, txt='El Veredicto', border=False, align='C')

    #Somos Fint
    pdf.set_xy(263, 165)
    pdf.cell(223,15, txt='Somos FinT', border=False, align='C')

    pdf.set_font('Quicksand', style='', size=26)
    pdf.set_text_color(0,0,0)

    pdf.set_xy(269, 60)
    pdf.multi_cell(210,12, txt=veredicto_txt, border=False, align='J')

    pdf.set_xy(269, 185)
    pdf.multi_cell(210,12, txt=somos_fint_txt, border=False, align='J')

    #***FOURTH_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_program_4.png', x=0, y=0, w=508, h=285.75, type='', link='')
    
    #***FIFTH_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_slogan_5.png', x=0, y=0, w=508, h=285.75, type='', link='')
    
    #***SIXTH_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_coaches_6.png', x=0, y=0, w=508, h=285.75, type='', link='')
    
    #***SEVENTH_PAGE***
    pdf.add_page()
    pdf.image('/ft_automated_pdf/fint_final_7.png', x=0, y=0, w=508, h=285.75, type='', link='')
    
    import base64
    st.download_button(
        'Download Report',
        data=pdf.output(dest='S').encode('latin-1'),
        file_name=f'fint_test_{nombre.title()}_{user}.pdf'
        )
    
    return
