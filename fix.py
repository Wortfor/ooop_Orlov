import os

root = r"C:\Users\orlov\Desktop\http_gui\src"

for dirpath, _, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith(".py"):
            filepath = os.path.join(dirpath, filename)
            
            # Пытаемся прочитать в UTF-8, если не выходит - читаем в cp1251
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(filepath, "r", encoding="cp1251") as f:
                    content = f.read()
                    
            # Записываем строго в UTF-8
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Исправлен: {filename}")

print("ГОТОВО! Все файлы переведены в UTF-8.")