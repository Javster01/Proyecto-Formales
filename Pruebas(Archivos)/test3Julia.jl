# Solicitar un número al usuario
println("Ingresa un número:")
num = parse(Int, readline())

# Verificar si el número es par o impar
if num % 2 == 0
    println("El número es par.")
else
    println("El número es impar.")
end

# Imprimir los números del 1 al num
println("Números del 1 al ", num, ":")
for i in 1:num
    println(i)
end
