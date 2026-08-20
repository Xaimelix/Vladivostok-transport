/**
 * Скрипт для взаимодействия с картой транспорта
 * Обрабатывает клики по станциям и управляет их состояниями
 */

document.addEventListener('DOMContentLoaded', function() {
    // Состояние приложения
    const state = {
        origin: null,      // Начальная точка маршрута
        destination: null  // Конечная точка маршрута
    };

    // DOM элементы
    const originElement = document.getElementById('origin-station');
    const destinationElement = document.getElementById('destination-station');
    const svgMap = document.getElementById('transport-map');

    /**
     * Очистить все классы состояния у элемента
     */
    function clearStationStates(element) {
        element.classList.remove(
            'normal', 'active', 'route', 'dimmed', 'closed', 'warning',
            'hover', 'selected', 'origin', 'destination', 'transfer'
        );
    }

    /**
     * Обновить отображение выбранной начальной точки
     */
    function updateOriginDisplay() {
        if (originElement && state.origin) {
            originElement.textContent = state.origin.name || state.origin.id;
        } else if (originElement) {
            originElement.textContent = 'Не выбрана';
        }
    }

    /**
     * Обновить отображение выбранной конечной точки
     */
    function updateDestinationDisplay() {
        if (destinationElement && state.destination) {
            destinationElement.textContent = state.destination.name || state.destination.id;
        } else if (destinationElement) {
            destinationElement.textContent = 'Не выбрана';
        }
    }

    /**
     * Обработчик клика по станции
     */
    function handleStationClick(event) {
        // Найти ближайший элемент станции (может быть клик по дочернему элементу)
        const station = event.target.closest('.station-marker, .station-node');
        
        if (!station) {
            return;
        }

        // Предотвратить стандартное поведение
        event.preventDefault();
        event.stopPropagation();

        // Пропустить закрытые станции
        if (station.classList.contains('closed')) {
            return;
        }

        // Получить идентификатор станции
        const stationId = station.id;
        const stationName = station.getAttribute('data-name') || stationId;

        // Логика выбора станций
        if (!state.origin) {
            // Выбор начальной точки
            state.origin = { id: stationId, name: stationName };
            
            // Установить состояние origin
            clearStationStates(station);
            station.classList.add('origin', 'selected');
            
            updateOriginDisplay();
            
        } else if (!state.destination) {
            // Нельзя выбрать ту же станцию как конечную
            if (state.origin.id === stationId) {
                // Сбросить начальную точку при клике на ту же станцию
                const prevStation = document.getElementById(state.origin.id);
                if (prevStation) {
                    clearStationStates(prevStation);
                    prevStation.classList.add('normal');
                }
                state.origin = null;
                updateOriginDisplay();
                return;
            }
            
            // Выбор конечной точки
            state.destination = { id: stationId, name: stationName };
            
            // Установить состояние destination
            clearStationStates(station);
            station.classList.add('destination', 'selected');
            
            updateDestinationDisplay();
            
        } else {
            // Обе точки уже выбраны - сброс и выбор новой начальной
            // Сбросить предыдущую начальную точку
            if (state.origin) {
                const prevOrigin = document.getElementById(state.origin.id);
                if (prevOrigin) {
                    clearStationStates(prevOrigin);
                    prevOrigin.classList.add('normal');
                }
            }
            
            // Сбросить предыдущую конечную точку
            if (state.destination) {
                const prevDestination = document.getElementById(state.destination.id);
                if (prevDestination) {
                    clearStationStates(prevDestination);
                    prevDestination.classList.add('normal');
                }
            }
            
            // Установить новую начальную точку
            state.origin = { id: stationId, name: stationName };
            clearStationStates(station);
            station.classList.add('origin', 'selected');
            
            state.destination = null;
            
            updateOriginDisplay();
            updateDestinationDisplay();
        }

        // Добавить эффект hover при клике
        station.classList.add('hover');
        setTimeout(() => {
            station.classList.remove('hover');
        }, 200);
    }

    /**
     * Обработчик наведения на станцию
     */
    function handleStationHover(event) {
        const station = event.target.closest('.station-marker, .station-node');
        
        if (!station || station.classList.contains('closed')) {
            return;
        }

        station.classList.add('hover');
    }

    /**
     * Обработчик ухода с станции
     */
    function handleStationLeave(event) {
        const station = event.target.closest('.station-marker, .station-node');
        
        if (!station) {
            return;
        }

        station.classList.remove('hover');
    }

    // Навесить обработчики событий на все станции
    function initializeStations() {
        const stations = document.querySelectorAll('.station-marker, .station-node');
        
        stations.forEach(station => {
            // Сделать станцию интерактивной
            station.style.cursor = 'pointer';
            
            // Добавить обработчики событий
            station.addEventListener('click', handleStationClick);
            station.addEventListener('mouseenter', handleStationHover);
            station.addEventListener('mouseleave', handleStationLeave);
            
            // Установить начальное состояние
            if (!station.classList.contains('closed')) {
                station.classList.add('normal');
            }
        });
    }

    // Инициализация при загрузке страницы
    initializeStations();
    
    // Инициализация отображения
    updateOriginDisplay();
    updateDestinationDisplay();

    console.log('Карта транспорта инициализирована. Станций:', document.querySelectorAll('.station-marker, .station-node').length);
});
