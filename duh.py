def the_numbers():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    trash = 'trash'
    return numbers, trash

def get_even_numbers(numbers):
    even_numbers = []
    for number in numbers:
        if number % 2 == 0:
            even_numbers.append(number)
    return even_numbers

#numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
get_numbers = the_numbers()
even_numbers = get_even_numbers(get_numbers)
print(even_numbers)
