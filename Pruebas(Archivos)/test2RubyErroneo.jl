def calcular_estadisticas(datos)
    n = datos.length


    suma = datos.reduce(:+)
    media = suma / n.to_f
  if
    datos_ordenados = datos.sort
    if n % 2 == 0
      indice_medio1 = n / 2
      indice_medio2 = indice_medio1 + 1
      mediana = (datos_ordenados[indice_medio1 - 1] + datos_ordenados[indice_medio2 - 1]) / 2.0
    else
      indice_medio = (n + 1) / 2
      mediana = datos_ordenados[indice_medio - 1]
    end
  
    suma_cuadrados_diff = datos.reduce(0) { |acc, dato| acc + (dato - media)**2 }
    desviacion_estandar = Math.sqrt(suma_cuadrados_diff / n)
    
    puts "Media: #{media}"
    puts "Mediana: #{mediana}"
    puts "Desviación estándar: #{desviacion_estandar}"
  end
  
datos = [12.3, 45.6, 78.9, 23.4, 56.7, 89.0, 34.5, 67.8, 90.1, 43.2, 76.5, 98.7, 54.3, 87.6, 21.0, 65.4, 32.1, 43.8, 76.9, 98.2]
  
calcular_estadisticas(datos)
  