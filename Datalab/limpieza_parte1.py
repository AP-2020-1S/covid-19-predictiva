### **Descripción metadata**

**Id de caso:** identificador de caso.

**Fecha de notificación:** fecha de notificación al SIVIGILA.

**Código Divipola:** código Divipola.

**Ciudad de ubicación:** por seguridad de las personas, algunos datos serán limitados evitando así la exposición y posible identificación en determinados municipios. 

**Departamento o Distrito:** por seguridad de las personas, algunos datos serán limitados evitando así la exposición y posible identificación en determinados municipios. 

**Atención:** * corresponde a muertes no relacionadas con COVID-19, aún si eran casos activos ** Hay pacientes recuperados para COVID-19, que pueden permanecer en hospitalización por otras comorbilidades.

**Edad:** edad del paciente.

**Sexo:** sexo del paciente.

**Tipo:** por seguridad de las personas, algunos datos serán limitados evitando así la exposición y posible identificación en determinados municipios. 

**Estado:** * corresponde a muertes no relacionadas con COVID-19, aún si eran casos activos ** Hay pacientes recuperados para COVID-19, que pueden permanecer en hospitalización por otras comorbilidades.

**País de procedencia:** país de procedencia.

**Fecha de ingreso al sistema (FIS):** fecha de ingreso al sistema.

**Fecha de muerte:** fecha de muerte del paciente.

**Fecha de diagnóstico:** fecha de confirmación por laboratorio.

**Fecha recuperado:** fecha recuperado.

**Fecha reporte Web:** fecha reporte Web.

**Tipo recuperación:** se refiere a la variable de tipo de recuperación que tiene dos opciones: PCR y tiempo. PCR indica que la persona se encuentra recuperada por segunda muestra, en donde dio negativo para el virus; mientras que tiempo significa que son personas que cumplieron 30 días posteriores al inicio de síntomas o toma de muestras que no tienen síntomas, que no tengan más de 70 años ni que estén hospitalizados.

**Código Departamento:** código Departamento.

**Código País:** código País de procedencia.

**Pertenencia etnica:** esta variable se actualizará cada semana.

**Nombre grupo etnico:** nombre grupo etnico.

consolidated_files['fecha_de_notificaci_n'] = pd.to_datetime(consolidated_files['fecha_de_notificaci_n']).dt.tz_localize(None) ## Se cambia el tipo de dato de objeto a datatime
consolidated_files['fecha_diagnostico'] = pd.to_datetime(consolidated_files['fecha_diagnostico']).dt.tz_localize(None) 
consolidated_files['fecha_recuperado'] = pd.to_datetime(consolidated_files['fecha_recuperado']).dt.tz_localize(None) 
consolidated_files['fecha_reporte_web'] = pd.to_datetime(consolidated_files['fecha_reporte_web']).dt.tz_localize(None) 
consolidated_files['fecha_de_muerte'] = pd.to_datetime(consolidated_files['fecha_de_muerte']).dt.tz_localize(None)


