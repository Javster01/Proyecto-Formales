# Solicitar al usuario que ingrese un número
puts "Por favor, ingresa un número:"
numero = gets.chomp.to_i

# Verificar si el número es positivo, negativo o cero
if numero > 0
  puts "El número es positivo."
else
  puts "El número es negativo."
end

# Imprimir los primeros 'n' números pares
puts "Los primeros #{numero} números pares son:"
contador = 0
i = 0
while contador < numero
  if i.even?
    puts i
    contador += 1

  i += 1
end
