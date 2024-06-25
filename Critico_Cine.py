# Sistema Experta Crítico de Cine que recomendará una terna de películas
# según el género que desee el usuario. La Base de datos utilizado es el IMDB
# con el ranking de las 1000 mejores películas de la historia.
# Tarea 3 Ingeniería del Conocimiento, Programa Doctorado IA
# Autor: Felipe Benavides Pantoja
# Fecha: Junio 2024

import pandas as pd
import streamlit as st
from experta import *
import random

# Cargar los datos IMDB del archivo CSV------------------------------------#
file_path = 'movie_db2.csv'
df = pd.read_csv(file_path, delimiter=';')

#--------------------------------------------------------------------------#
# Separar los géneros combinados y obtener una lista de géneros de peliculas únicos
generos_unicos = set()    # Conjunto vacío
for generos in df['Genre']:
    for genero in generos.split(','):
        generos_unicos.add(genero.strip())
# Convertir el conjunto a una lista y ordenar
generos_unicos = sorted(list(generos_unicos))

#---------------------------------------------------------------------------#
class Pelicula(Fact):
    """Información de la pelicula"""
    pass
#---------------------------------------------------------------------------#

class SistemaRecomendacion(KnowledgeEngine):
    @Rule(Pelicula(genero=MATCH.genero_usuario))    # Regla
    def recomendar(self, genero_usuario):
        peliculas = df[df['Genre'].str.contains(genero_usuario, case=False, na=False)]
        self.recomendaciones = peliculas


    def obtener_recomendaciones(self, genero):
        self.reset()
        self.declare(Pelicula(genero=genero))
        self.run()
        return self.recomendaciones

#-----------------------------------------------------------------------------#

st.title('Sistema de Recomendación de Películas con Experta')

# Selección del género por parte del usuario
genero_seleccionado = st.selectbox('Seleccione un género', generos_unicos)

if genero_seleccionado:
    engine = SistemaRecomendacion() # Enlace al sistema experta
    recomendaciones = engine.obtener_recomendaciones(genero_seleccionado) # LLamada al sistema experta

#-----------------------------------------------------------------------------#
# Recomendación Mejor Película
    st.write(f'La mejor película del genero {genero_seleccionado} y un imperdible '
             f'es: {recomendaciones.iloc[0,1]}, esta obra maestra del año'
             f' {recomendaciones.iloc[0,2]} es dirigida por {recomendaciones.iloc[0,9]}'
             f' y cuenta con interpretaciones magistrales de {recomendaciones.iloc[0,10]}, '
             f' {recomendaciones.iloc[0,11]} y {recomendaciones.iloc[0,12]} entre otros.'
             f' Puntaje IMDB: {recomendaciones.iloc[0,6]}.')
    st.image(f"{recomendaciones.iloc[0,0]}",width=700)
#-----------------------------------------------------------------------------#
# Recomendación Peliculaza [2-10]
    np=random.randint(1,10) # número al azar entre 1 y 10
    st.write(f'Otra pelicula del genero {genero_seleccionado} y dentro de las grandes '
         f'de la historia del séptimo arte es: {recomendaciones.iloc[np, 1]}, esta clásico del año'
         f' {recomendaciones.iloc[np, 2]} es dirigida por {recomendaciones.iloc[np, 9]}'
         f' y cuenta con actuaciones superlativas de {recomendaciones.iloc[np, 10]}, '
         f' {recomendaciones.iloc[np, 11]} y {recomendaciones.iloc[np, 12]} entre otros.'
         f' Puntaje IMDB: {recomendaciones.iloc[np, 6]}.')
    st.image(f"{recomendaciones.iloc[np, 0]}",width=700)
#------------------------------------------------------------------------------#
# Recomendación Tercera Pelicula Anterior a 1980
    recomendaciones.iloc[:,2]=pd.to_numeric(recomendaciones.iloc[:,2], errors='coerce')
    rec_1980=recomendaciones[recomendaciones.iloc[:, 2] < 1980]
    nc=0
    while rec_1980.iloc[nc,1]==recomendaciones.iloc[0,1] or rec_1980.iloc[nc,1]==recomendaciones.iloc[np,1]:
        nc=nc+1    # Codigo para evitar dobles recomendaciones

    st.write(f'Dentro de las películas clásicas de este género, no puedo despedirme sin '
         f'recomendar: {rec_1980.iloc[nc, 1]}, esta clásico del año'
         f' {rec_1980.iloc[nc, 2]} es dirigida por {rec_1980.iloc[nc, 9]}'
         f' y cuenta con interpretaciones magistrales de {rec_1980.iloc[nc, 10]}, '
         f' {rec_1980.iloc[nc, 11]} y {rec_1980.iloc[nc, 12]} entre otros.'
         f' Puntaje IMDB: {rec_1980.iloc[nc, 6]}.')
    st.image(f"{rec_1980.iloc[nc, 0]}",width=700)