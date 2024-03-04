# Solicitar al usuario que ingrese un número
println "Por favor, ingresa un número:"
numero = parse(Int, readline())

# Verificar si el número es positivo, negativo o cero
if numero > 0
  println("El número es positivo.")
else
  println("El número es negativo.")
end

# Imprimir los primeros 'n' números pares
println("Los primeros $(numero) números pares son:")
contador = 0
i = 0
while contador < numero
  if i % 2 == 0
    println(i)
    contador += 1
  end
  i += 1
end
