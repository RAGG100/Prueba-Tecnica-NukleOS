import pandas as pd
import datetime as dt

# Dirección de folder
PATH = r"D:\alan_\Documents\Alan\NukleOS"
# Leer excel
datos = pd.read_csv(PATH + r"\Recursos.csv", sep = ",")
# Revisar lectura
print(datos.head()) # Existen columnas extras
print(datos.tail()) # Existen filas extras
# Eliminar columnas inecesarias
datos = datos.dropna(axis = 1, how = "all")
# Eliminar filas inecesarias
datos = datos.dropna(axis = 0, how = "all")

# Variable con columnas a modificar
cols = None

# RETO 1
cols = "Nombre comercial"
datos[cols] = datos[cols].map(lambda nombre: nombre.lower())

# RETO 2
cols = ['Fecha de Emisión', 'Fecha Vencimiento']
# Identificar formato
print(datos[cols].head())
# Cambiar formato
def formatear_fecha(fecha: str, sep: str) -> str:
    nueva_fecha = dt.datetime.strptime(fecha, '%d %m %Y'.replace(' ', sep))
    fecha_corregida = nueva_fecha.strftime('%d/%m/%Y')
    return fecha_corregida

datos[cols[0]] = datos[cols[0]].apply(formatear_fecha, args = '*')
datos[cols[1]] = datos[cols[1]].apply(formatear_fecha, args = '-')

# RETO 3
cols = 'Forma Farmacéutica'
datos[cols] = datos[cols].map(lambda nombre: nombre.upper())

# RETO 4
datos = datos.rename(columns = {'0':'Registro'})

# RETO 5
# Crear dataframe auxiliar con registro e indice
datos_aux = pd.DataFrame({'idx':datos.index})
datos_aux['Registro'] = datos['Registro']

# Dataframe para ubicar ultimas apariciones de cada registro
registro_fin = datos_aux.groupby('Registro')['idx'].max()

# Registros por eliminar (aquellos cuyo indice sea menor al de registro_fin)
# Nota: se elimina si no tiene registro
registro_borrar = [i for i in datos.index 
                   if i < registro_fin.get(datos.loc[i,'Registro'], datos.shape[0]+1)]

datos = datos.drop(index = registro_borrar)

# RETO 6
cols = 'Laboratorio'
datos[cols] = datos[cols].map(lambda nombre: nombre[:nombre.rfind(', ')])

# RETO 7
cols = 'Tipo de Sociedad'
datos[cols] = datos[cols].map(lambda nombre: nombre[(nombre.rfind(', ')+2):])


# Escribir csv cambiado
datos.to_csv(PATH + r"\Respuesta.csv", index = False, 
             encoding='utf-8-sig')