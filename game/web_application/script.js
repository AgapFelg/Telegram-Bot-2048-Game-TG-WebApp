// ожидание полной загрузки DOM перед выполнением js
document.addEventListener('DOMContentLoaded', () => {
    // ОСНОВНЫЕ ПЕРЕМЕННЫЕ
    let grid = []; // массив для хранения состояния игры
    let score = 0; // текущий счет игрока
    let bestScore = localStorage.getItem('bestScore') || 0; // попытка взять лучший счет игрока из локального хранилища, если его нет, тогда присваивается 0
    let gameOver = false; // флаг гейм овера
    let isBWTheme = localStorage.getItem('isBWTheme') === 'true'; // получение темы из локального хранища

    // получение ссылок на элементы DOM
    const gridContainer = document.querySelector('.grid'); // контейнер сетки
    const tileContainer = document.querySelector('.tile-container'); // контейнер плиток
    const scoreDisplay = document.getElementById('score'); // отображение счета
    const bestScoreDisplay = document.getElementById('best-score'); // отображение лучшего счета
    const gameMessage = document.querySelector('.game-message'); // сообщение о гейм овере
    const restartButton = document.getElementById('restart-btn'); // кнопка рестарта
    const themeButton = document.getElementById('theme-btn'); // кнопка смены оформления
    const upButton = document.querySelector('.up-btn'); // кнопка движения вверх
    const leftButton = document.querySelector('.left-btn'); // документ движения влево
    const rightButton = document.querySelector('.right-btn'); // кнопка движения вправо
    const downButton = document.querySelector('.down-btn'); // кнопка движения вниз

    // РАЗМЕРЫ ИГРОВОГО ПОЛЯ
    const gridSize = 4;

    // ФУНКЦИЯ ИНИЦИАЛИЗАЦИИ ИГРЫ
    function init() {
        // УСТАНОВКА ТЕМЫ из локального хранилища
        if (isBWTheme) {
            document.body.classList.add('bw-theme'); // если чернобелая, то добавляется класс черно белой темы
            themeButton.textContent = 'Классическая тема'; // и изменяется текст кнопки
        } else { // если тема классическая
            document.body.classList.remove('bw-theme'); // то класс черно-белой темы удаляется
            themeButton.textContent = 'Черно-белая тема'; // текст кнопки изменяется
        }

        // обновление показателя рекорда
        bestScoreDisplay.textContent = bestScore;

        // Создание массива 4х4 (сетки), заполненного нулями
        grid = Array(gridSize).fill().map(() => Array(gridSize).fill(0));

        // сброс счета и состояния игры
        score = 0;
        scoreDisplay.textContent = '0'; // обновление отображаемого счета
        gameOver = false; // установка в фолсе флага гейм овера
        gameMessage.style.display = 'none'; // убираем сообщение о гейм овере

        // очистка контейнера с плитками
        tileContainer.innerHTML = '';

        // Добавление двух начальных плиток
        addRandomTile();
        addRandomTile();

        // ОТРИСОВКА СЕТКИ
        render();
    }

    // ФУНКЦИЯ ДОБАВЛЕНИЯ СЛУЧАЙНОЙ ПЛИТКИ
    function addRandomTile() {
        const emptyCells = []; // создания массива, в который будут заноситься пустые ячейки

        // поиск всех нулевых ячеек
        // проходится по всему массиву и если значение в ячейки i j равняется нулю, то заносятся координаты в виде x, y в массив для пустых ячеек
        for (let i = 0; i < gridSize; i++) {
            for (let j = 0; j < gridSize; j++) {
                if (grid[i][j] === 0) {
                    emptyCells.push({x: j, y: i});
                }
            }
        }

        // Если есть пустые ячейки, добавляем новую плитку
        if (emptyCells.length > 0) {
            const randomCell = emptyCells[Math.floor(Math.random() * emptyCells.length)]; // выбор случайной ячейки из массива со случайными ячейками
            grid[randomCell.y][randomCell.x] = Math.random() < 0.9 ? 2 : 4; // основному массисву поля по координатам x и y из выбранной случайрной ячейки рандомно присваивается
            // либо значение 2 либо значение 4
        }
    }

    // ФУНКЦИЯ ОТРИСОВКИ ИГРОВОГО ПОЛЯ
    function render() {
        tileContainer.innerHTML = ''; // происходит очистка контейнера на хтмл странице
        // начинается перебор всех ячеек
        for (let i = 0; i < gridSize; i++) {
            for (let j = 0; j < gridSize; j++) {
                // если ячейка не нулевая (типо есть плитка), то
                if (grid[i][j] !== 0) {
                    // создается в доме элемент плитки
                    const tile = document.createElement('div')
                    tile.classList.add('tile', `tile-${grid[i][j]}`); // добавление класса для плитки с координатами
                    tile.textContent = grid[i][j]; // устанавливается текст, то есть значение плитки

                    // позиционирование с помощью CSS grid
                    tile.style.gridRow = i + 1; // номер строки, начиная с 1
                    tile.style.gridColumn = j + 1; // номер колонки, начиная с 1

                    tileContainer.appendChild(tile); // добавление созданной плитки в контейнер
                }
            }
        }
    }

    // Движение плиток
    function move(direction) {
        if (gameOver) return false; // если игра окончена, то движения не происходит
        // инициализация флага, показывающего то, было ли совершено движение
        let moved = false;
        // в отдельную переменную сохраняется копия сетки, которая была до того,как было совершено движение
        let oldGrid = JSON.parse(JSON.stringify(grid));

        // Поворот сетки
        // если движение происходит вверх, или вниз, то происходит транспонирование сетки
        if (direction === 'up' || direction === 'down') {
            grid = transpose(grid);
        }
        // для движения вправо или вниз нужно отзеркалить строки
        if (direction === 'right' || direction === 'down') {
            grid = grid.map(row => row.reverse());
        }

        // Обработка движения и слияния
        // запускается цикл по размеру сетки
        for (let i = 0; i < gridSize; i++) {
            // из строки убираются нули
            let row = grid[i].filter(val => val !== 0);
            // проверяется возможгность того, можно ли слить соседние плитки
            for (let j = 0; j < row.length - 1; j++) { // запускается цикл по ячейкам в строке, до макс значение-1 (так как если надо проверить предпоследнюю и последнюю и остановиться)
                if (row[j] === row[j + 1]) { // если исследуемая и следующая после исследуемой ячейки одинаковые
                    row[j] *= 2; // то их значение умножается
                    row[j + 1] = 0; // вторая плитка становится пустой
                    score += row[j]; // к значению счета игрока прибавляется умноженное значекние плитки
                    moved = true; // флагу того, было ли движение присваивается значение true
                }
            }
            // снова убираем все нули из строки, чтобы не было лишних нулей там где их быть не должно
            row = row.filter(val => val !== 0);
            // добавляем нули, пока количество ячеек в строке (в том числе нулевых) не станет равняться нужной длине строки
            while (row.length < gridSize) {
                row.push(0);
            }

            grid[i] = row; // обновляем в массиве для хранения поля строку, которая изменилась
        }

        // проверяется какое было направление движения, если направление было в право, или вниз
        // то есть, если массив с сеткой отражался, то происходит обратное построчное отражение
        if (direction === 'right' || direction === 'down') {
            grid = grid.map(row => row.reverse());
        }
        // проверяется какое направление движения было, если направление было вверх или вниз,то есть
        // массив с сеткой транспонировался, то применяется обратное транспонирование
        if (direction === 'up' || direction === 'down') {
            grid = transpose(grid);
        }

        // проверяется то, случилось ли все-таки движение, посредством сравнения со старой версией массива сетки
        if (!arraysEqual(oldGrid, grid)) {
            moved = true;
        }

        // Если движение произошло, добавляем новую плитку
        if (moved) {
            addRandomTile(); // добавление новоей плитки
            scoreDisplay.textContent = score; // присвоение показателю счета игрока нового значения

            // Обновление рекорда
            if (score > bestScore) { // проверка того, больше ли новый счет, чем старый
                bestScore = score; // установка значению рекорда текущего счета
                bestScoreDisplay.textContent = bestScore; // измение текста у элемента, отвечающего за отображение рекорда
                localStorage.setItem('bestScore', bestScore); // сохранение в локальное хранилище показтеля лучшего счета
            }

            render(); // перерисовывается сетка

            // Проверка на завершение игры
            if (isGameOver()) {
                gameOver = true; // устанавилвается флаг гейм овера
                gameMessage.querySelector('p').textContent = 'Игра окончена!'; // элементу сообщения присваивается текст о том, что
                // игра окончена
                gameMessage.style.display = 'flex'; // выводится сообщение
            }
        }

        return moved; // возвращает флаг движения
    }

    // Проверка на завершение игры
    function isGameOver() {
        // проверка наличия пустых ячеек
        // проходится по каждой ячейке массива игрвого поля
        for (let i = 0; i < gridSize; i++) {
            for (let j = 0; j < gridSize; j++) {
                if (grid[i][j] === 0) { // и если находит хотя бы одну свободную, то тогда
                    // возвращает фолс насчет того, окончена ли игра
                    return false;
                }
            }
        }

        // проверяется то, можно ли сделать хоть какой-нибудь ход
        // цикл по каждой ячейке массива
        for (let i = 0; i < gridSize; i++) {
            for (let j = 0; j < gridSize; j++) {
                const value = grid[i][j]; // получение текущего значения
                if (j < gridSize - 1 && grid[i][j + 1] === value) {
                    return false; // если горизонтально можно сделать ход, тогда возвращается фолсе
                }

                if (i < gridSize - 1 && grid[i + 1][j] === value) {
                    return false; // если вертикально можно сделать ход, тогда возвращается фолсе
                }
            }
        }
        // если цикл завершился и нету возможности сделать ход, то возвращае тру (игра проиграна)
        return true;
    }

    // ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ

    // ФУНКЦИЯ ТРАНСПОНИРОВАНИЯ МАТРИЦЫ
    function transpose(matrix) {
        return matrix[0].map((_, colIndex) => matrix.map(row => row[colIndex]));
    }
    // ФУНКЦИЯ СРАВНЕНИЯ ДВУХ МАССИВОВ
    function arraysEqual(a, b) {
        // проходит по всем ячейкам
        // берет i и j
        // и если хотя бы у одной ячейки i и j не одинаковое значение в массивах
        // a и b, тогда возвращает фолсе
        for (let i = 0; i < gridSize; i++) {
            for (let j = 0; j < gridSize; j++) {
                if (a[i][j] !== b[i][j]) {
                    return false; // массивы не равны
                }
            }
        }
        return true; // массивы равны
    }

    // ОБРАБОТЧИКИ СОБЫТИЙ

    // ОБРАБОТКА НАЖАТИЙ СТРЕЛОК НА КЛАВИАИТУРЕ КОМПЬЮТЕРА
    // слушатель наажатия
    document.addEventListener('keydown', event => {
        // проверяет то, какая кнолпка нажата
        switch(event.key) {
            // если нажата стрелка вверх
            case 'ArrowUp':
                // предотвращение прокрутки страницы
                event.preventDefault();
                move('up'); // вызов функции движения с передачей направления вверх
                break; // остановка
            case 'ArrowDown': // если нажата стрелка вниз
                event.preventDefault(); // предотвращение прокрутки страницы
                move('down'); // движение вних
                break;
            case 'ArrowLeft': // есди нажата стрелка влево
                event.preventDefault(); // происходит предотвращеение прокрутки страницы
                move('left'); // движение влево
                break; // остановка
            case 'ArrowRight': // если нажата стрелка вправо
                event.preventDefault(); // происхоидт предотвращение прокрутки страницы
                move('right'); // движение вправо
                break; // остановка
        }
    });

    // обработчики для кнопки управления
    // если нажимается кнопка вверх, то движение вверх
    upButton.addEventListener('click', () => move('up'));
    downButton.addEventListener('click', () => move('down')); // если нажимается кнопка вниз, то движение вниз
    leftButton.addEventListener('click', () => move('left')); // если нажимается кнопка влево, то движение влево
    rightButton.addEventListener('click', () => move('right')); // если нажимается кнопка вправо, то движение вправо

    // кнопка перезапуска игры
    restartButton.addEventListener('click', init); // если нажата, то заново инициализируется игра

    // кнопка смены темы
    themeButton.addEventListener('click', () => {
        isBWTheme = !isBWTheme; // тема меняется на противоположную
        localStorage.setItem('isBWTheme', isBWTheme); //тема сохраняется в локальное хранилище

        if (isBWTheme) {
            document.body.classList.add('bw-theme'); // если выбрана черно-белая тема, то добавляется в документ
            themeButton.textContent = 'Классическая тема'; // меняется текст у кнопки
        } else {
            document.body.classList.remove('bw-theme'); // если выбрана классическая тема, до черно белая удаляется
            themeButton.textContent = 'Черно-белая тема'; // меняется текст у кнопки
        }
    });

    // кнопка "Сыграть еще" в сообщении о завершении игры
    gameMessage.querySelector('button').addEventListener('click', init);

    // обработка свайпов для мобильных устройств
    let touchStartX, touchStartY, touchEndX, touchEndY;

    // сохранение координат касания начальных
    document.addEventListener('touchstart', event => {
        touchStartX = event.touches[0].clientX;
        touchStartY = event.touches[0].clientY;
    }, { passive: true });
    // сохранение координат касания конечных
    document.addEventListener('touchend', event => {
        touchEndX = event.changedTouches[0].clientX;
        touchEndY = event.changedTouches[0].clientY;
    // обработка свайпа
        handleSwipe();
    }, { passive: true });

    // добавляем обработчик для предотвращения скролла при свайпах
    document.addEventListener('touchmove', function(event) {
        // проверяем, происходит ли касание внутри игровой области
        if (event.target.closest('.game-container')) {
            event.preventDefault();
        }
    }, { passive: false });
    // функция обработки свайпов
    function handleSwipe() {
        const dx = touchEndX - touchStartX; // переменная для хранения разницы по горизонтали
        const dy = touchEndY - touchStartY; // переменная для хранения разницы по ветрикали

        // минимальное расстояние для определения свайпа
        const minSwipeDistance = 30;
        // определение направления свайпа
        if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > minSwipeDistance) { // сравнение того, какая разница (модуль) больше
        // если разница по горизонтали больше разницы по вертикали и больше минимальной дистанции для засчитывания свайпа, то
        // присваивается горизонтальный свайп
            // если разница положительна (движение было слева направо), то движение вправо
            if (dx > 0) {
                move('right');
            // если разница отрицательна (движение было справа на лево), то движение влево
            } else {
                move('left');
            }
        // если разница по вертикали больше разницы по горизонтали (модули) и разница (модуль) больше минимальной
        // дистанции для свайпа, то присваивается вертикальный свайп
        } else if (Math.abs(dy) > Math.abs(dx) && Math.abs(dy) > minSwipeDistance) {
            // если разница больше нуля (движение было вниз), то движение вниз
            if (dy > 0) {
                move('down');
            // если разница меньше нуля (движение было вверх), то движение вверх
            } else {
                move('up');
            }
        }
    }

    // запуск игры
    init();
});