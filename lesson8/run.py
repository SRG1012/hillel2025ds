import threading
import random
import time

# Глобальний список для спільного використання
global_list = []

# Заповнення списку випадковими числами
def fill_list():
    global global_list
    print("T1: Заповнення списку...")
    global_list = [random.randint(1, 1000) for _ in range(10_000)]
    print("T1: Список заповнено.")

# Знаходження суми елементів у списку
def calculate_sum():
    global global_list
    print("T2: Очікування заповнення списку...")
    while not global_list:
        time.sleep(0.1)  # Очікуємо, поки список не заповниться
    print("T2: Обчислення суми...")
    total_sum = sum(global_list)
    print(f"T2: Сума елементів = {total_sum}")

# Знаходження середнього арифметичного
def calculate_average():
    global global_list
    print("T3: Очікування заповнення списку...")
    while not global_list:
        time.sleep(0.1)
    print("T3: Обчислення середнього арифметичного...")
    average = sum(global_list) / len(global_list)
    print(f"T3: Середнє арифметичне = {average}")

# Основна функція для запуску потоків
def main():

    t1 = threading.Thread(target=fill_list)
    t2 = threading.Thread(target=calculate_sum)
    t3 = threading.Thread(target=calculate_average)

    # Запуск потоків
    t1.start()
    t2.start()
    t3.start()

    # Очікування завершення потоків
    t1.join()
    t2.join()
    t3.join()

if __name__ == "__main__":
    main()
