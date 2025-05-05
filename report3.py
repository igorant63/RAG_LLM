import json

def read_filenames(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            filenames = [line.strip() for line in file if line.strip()]
        return filenames
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []

json_files = read_filenames("files.txt")

def calculate_averages_and_save_report(json_files, report_file="report3.txt"):
    report_lines = []
    for file in json_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Проверяем наличие записей
            if not data:
                report_lines.append(f"Файл {file}: нет данных для анализа.\n")
                continue
            
            # Инициализация переменных для подсчета
            total_response_time = 0
            total_criteria = {"точность": 0, "грамотность": 0, "полнота": 0, "лаконичность": 0}
            count = 0
            has_zero_values = False

            for entry in data:
                # Суммируем время ответа
                response_time = entry.get("elapsed_time", 0)
                if response_time == 0:
                    has_zero_values = True
                total_response_time += response_time

                # Суммируем оценки критериев
                for crit in total_criteria:
                    crit_value = entry.get(crit, 0)
                    if crit_value == 0:
                        has_zero_values = True
                    total_criteria[crit] += crit_value
                
                count += 1
            
            # Проверяем, были ли данные
            if count == 0:
                report_lines.append(f"Файл {file}: нет данных для анализа.\n")
                continue

            # Рассчитываем средние значения
            avg_response_time = total_response_time / count
            avg_criteria = {crit: ((total / count) - 1) / 0.9 for crit, total in total_criteria.items()}

            # Формируем строку отчета для текущего файла
            report_lines.append(f"Файл: {file}")
            report_lines.append(f"Среднее время ответа: {avg_response_time:.2f} секунд")
            for crit, avg in avg_criteria.items():
                report_lines.append(f"Средняя оценка по '{crit}': {avg:.2f}")

            # Добавляем предупреждение о нулевых значениях, если есть
            if has_zero_values:
                report_lines.append(f"⚠️ Предупреждение: В файле {file} найдены нулевые значения в данных.")
            report_lines.append("")  # Пустая строка для разделения файлов

        except Exception as e:
            report_lines.append(f"Ошибка при обработке файла {file}: {e}\n")

    # Сохраняем отчет в текстовый файл
    try:
        with open(report_file, "w", encoding="utf-8") as report:
            report.write("\n".join(report_lines))
        print(f"Отчет успешно сохранен в {report_file}.")
    except Exception as e:
        print(f"Не удалось сохранить отчет: {e}")

# Запускаем расчет и генерацию отчета
calculate_averages_and_save_report(json_files)
