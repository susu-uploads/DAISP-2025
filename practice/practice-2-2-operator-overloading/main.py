class Snow:
    def __init__(self, snowflakes_count):
        self.snowflakes_count = snowflakes_count

    def __add__(self, n):
        if isinstance(n, Snow):
            return Snow(self.snowflakes_count + n.snowflakes_count)
        elif isinstance(n, (int, float)):
            return Snow(self.snowflakes_count + int(n))
        else:
            raise TypeError("Можно складывать только с числами или другими объектами Snow")

    def __sub__(self, n):
        if isinstance(n, Snow):
            result = self.snowflakes_count - n.snowflakes_count
        elif isinstance(n, (int, float)):
            result = self.snowflakes_count - int(n)
        else:
            raise TypeError("Можно вычитать только числа или другие объекты Snow")

        return Snow(result)

    def __mul__(self, n):
        if isinstance(n, (int, float)):
            return Snow(int(self.snowflakes_count * n))
        elif isinstance(n, Snow):
            return Snow(self.snowflakes_count * n.snowflakes_count)
        else:
            raise TypeError("Можно умножать только на числа и объект Snow")

    def __truediv__(self, n):
        if isinstance(n, (int, float)) and n != 0:
            result = round(self.snowflakes_count / n)
            return Snow(result)
        elif isinstance(n, Snow):
            if n.snowflakes_count == 0:
                raise ZeroDivisionError("Деление на ноль невозможно")
            result = round(self.snowflakes_count / n.snowflakes_count)
            return Snow(result)
        elif n == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        else:
            raise TypeError("Можно делить только на числа и объект Snow")

    def __call__(self, new_count):
        if isinstance(new_count, (int, float)):
            self.snowflakes_count = int(new_count)
        else:
            raise TypeError("Количество снежинок должно быть числом")

    def makeSnow(self, snowflakes_per_row):
        if snowflakes_per_row <= 0:
            return ""

        total_rows = self.snowflakes_count // snowflakes_per_row
        remaining_snowflakes = self.snowflakes_count % snowflakes_per_row

        snow_pattern = ""

        for i in range(total_rows):
            snow_pattern += "*" * snowflakes_per_row
            if i < total_rows - 1 or remaining_snowflakes > 0:
                snow_pattern += "\n"

        if remaining_snowflakes > 0:
            snow_pattern += "*" * remaining_snowflakes

        return snow_pattern

    def __str__(self):
        return f"Snow({self.snowflakes_count})"

    def __repr__(self):
        return f"Snow({self.snowflakes_count})"

print("Creating Snow")
snow1 = Snow(20)
snow2 = Snow(10)

print("\nShowing arithmetic operations:")
print(f"snow1 = {snow1}")
print(f"snow2 = {snow2}\n")

snow_add = snow1 + snow2
print(f"snow1 + snow2 = {snow_add}\n")

snow_add_num = snow1 + 15
print(f"snow1 + 15 = {snow_add_num}\n")

snow_sub = snow1 - snow2
print(f"snow1 - snow2 = {snow_sub}\n")

snow_sub_num = snow1 - 5
print(f"snow1 - 5 = {snow_sub_num}\n")

snow_mul = snow1 * 2
print(f"snow1 * 2 = {snow_mul}\n")

snow_div = snow1 / 3
print(f"snow1 / 3 = {snow_div}\n")

print("Showing makeSnow():")
test_snow = Snow(25)
print(f"Snow с {test_snow.snowflakes_count} снежинками:")
print("По 5 снежинок в ряду:")
print(test_snow.makeSnow(5))
print("\nПо 7 снежинок в ряду:")
print(test_snow.makeSnow(7))
print()

print("Call as a function")
print(f"Before: {test_snow}")
test_snow(50)  # Изменяем количество снежинок
print(f"After: {test_snow}")
print("New makeSnow()")
print(test_snow.makeSnow(8))
