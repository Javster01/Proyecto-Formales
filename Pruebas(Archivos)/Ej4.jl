# Datos de ejemplo
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Calcular la media
mean_value = sum(data) / length(data)

# Calcular la suma de los cuadrados de las diferencias
sum_squared_diff = sum((x - mean_value)^2 for x in data)

# Calcular la varianza
variance = sum_squared_diff / (length(data) - 1)

# Calcular la desviación estándar como la raíz cuadrada de la varianza
std_deviation = sqrt(variance)

println("Desviación estándar: ", std_deviation)