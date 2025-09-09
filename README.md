# diplom

### Шаги
1. Склонировать проект 'git clone https://github.com/Anna-5555/diplom.git'
2. Установить зависимости 'pip install -r requirements.txt'
3. Запустить тесты 'pytest'
4. Сгенерировать отчет 'allure generate allure-files -o allure-report'
5. Открыть отчет 'allure open allure-report'
6. В файле [test_UI.py] есть ожидания. Это связано в тем, что сайт может
запустить проверку на робота и нужно ее пройти в ручном режиме:
нажать на чек-бокс и ввести в появившемся поле показываемые значения.

### Стек:
- pytest
- selenium
- requests
- _sqlalchemy_
- allure
- config

### Струткура:
- ./pages - описание страниц и тесты
- ./api - хелперы для работы с API
- ./db - хелперы для работы с БД

### Полезные ссылки:
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore)
