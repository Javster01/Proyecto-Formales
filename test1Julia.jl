println("Ingrese una lista de numeros separados por espacios:")
entrada = readline()
numeros = parse.(Float64, split(entrada))
hola(skdjvb)
media = sum(numeros) / length(numeros)
mediana = median(numeros)

println("La media de los números es: ", media)
println("La mediana de los números es: ", mediana)

if media > mediana
    println("La media es mayor que la mediana.")
elseif media < mediana
    println("La mediana es mayor que la media.")
else
    println("La media y la mediana son iguales.")
end

println("Numeros mayores que la media:")
for num in numeros
    if num > media
        println(num)
    end
end

Array = ["Geeks", "For", "Geeks"]

# Iterator Variable
i = 1

# while loop
while i <= length(Array)

    # Assigning value to object
    Object = Array[i]

    # Printing object
    println("$Object")

    # Updating iterator globally
    global i += 1
# Ending Loop
end
