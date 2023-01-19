#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 12:38:29 2022

@author: hugoarellano
"""

from report_process import calibration_annot, emoji_selector, color_selector, statement_selector, sort_opp, annotation_in_chart, chart_params, global_chart, area_charts, generate_pdf_2
from fpdf import FPDF
import pandas as pd
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import xlrd
import plotly.graph_objects as go

#trayendo los datos procesados 

#enmarca el id de la hoja y el nombre
gsheetid = '1bDq0wGZ4TTW0txw3O6evXcoMSYIkGh-QrvMjyWKfUhw'
sheet_name = "Sheet1"

#formatea el texto
gsheet_url = f"https://docs.google.com/spreadsheets/d/{gsheetid}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

#convirte los datos de la hoja a pandas dataframe
df_pdf = pd.read_csv(gsheet_url)

user_id = st.selectbox('Selecciona el número de usuario',
              df_pdf['usuario'].unique().tolist())

user_df = df_pdf[(df_pdf['usuario'] == user_id)] 

st.write(user_df)

def get_name(usuario, df):
    return df[df.iloc[:,0]==usuario].iloc[0,1]

nombre = get_name(user_id, user_df)


if st.button('Procesa los datos para obtener reporte pdf'):
    
    #get the params
    total_params = chart_params(user_df, 'total_score')
    deuda_params = chart_params(user_df, 'sco_deuda')
    ahorro_params = chart_params(user_df, 'sco_ahorro')
    inversion_params = chart_params(user_df, 'sco_inversion')
    
    #get_values
    total_values = total_params[0]
    deuda_values = deuda_params[0]
    ahorro_values = ahorro_params[0]
    inversion_values = inversion_params[0]
    
    area_values = [deuda_values, ahorro_values, inversion_values]
    
    #get_labels
    total_labels = total_params[1]
    deuda_labels = deuda_params[1]
    ahorro_labels = ahorro_params[1]
    inversion_labels = inversion_params[1]
    
    area_labels = [deuda_labels, ahorro_labels, inversion_labels]
    
    #get text_params
    veredicto = statement_selector(total_values, 'global')
    text_deuda = statement_selector(deuda_values, 'deuda')
    text_ahorro = statement_selector(ahorro_values, 'ahorro')
    text_inversion = statement_selector(inversion_values, 'inversion')
    
    
    #get colors
    color_global = color_selector(total_values)
    color_deuda = color_selector(deuda_values)
    color_ahorro = color_selector(ahorro_values)
    color_inversion = color_selector(inversion_values)
    
    area_colors = [color_deuda, color_ahorro, color_inversion]
    
    #get annots
    annot_global = annotation_in_chart(total_values)
    annot_deuda = annotation_in_chart(deuda_values)
    annot_ahorro = annotation_in_chart(ahorro_values)
    annot_inversion = annotation_in_chart(inversion_values)
    
    area_annots = [annot_deuda, annot_ahorro, annot_inversion]
    
    #keysort
    keysort_deuda = sort_opp(deuda_values)
    keysort_ahorro = sort_opp(ahorro_values)
    keysort_inversion = sort_opp(inversion_values)
    
    keysorts_area = [keysort_deuda, keysort_ahorro, keysort_inversion]
    
    #global_chart
    global_chart = global_chart(total_values, total_labels, annot_global, color_global)
    global_path = f'{nombre.title()}_{user_id}_global_chart.png'
    global_chart.write_image(global_path)
    user_global_chart = global_path
    
    
    xaxis_deuda = calibration_annot(deuda_values, 'deuda')
    xaxis_inversion = calibration_annot(inversion_values, 'inversion')
    
    
    #area_chart
    area_chart = area_charts(area_values, area_labels, area_colors, keysorts_area, area_annots, xaxis_deuda, xaxis_inversion)
    area_path = f'{nombre.title()}_{user_id}_area_charts.png'
    area_chart.write_image(area_path)
    user_area_chart = area_path
    
    
    #get_emoji
    my_emoji = emoji_selector(total_values)
    
    somos_fint = 'Nuestro Programa Wealth-Being® además de poner tus finanzas bien fit, te brinda el apoyo y el respaldo de todo un equipo de expertos para que florezcas en todas las áreas de tu vida '
    
#obten reporte
    generate_pdf_2(user_id, nombre, user_area_chart, text_deuda, text_ahorro, text_inversion, user_global_chart, my_emoji, veredicto, somos_fint)
