#!/usr/bin/env python3
"""Seed скрипт для заполнения БД данными о транспорте.

Читает app/static/css/stations.json и создаёт линии и станции.
Соединения (Connection) не заполняются — см. раздел CONNECTIONS ниже.
"""

import json
import sys
from pathlib import Path

# Добавляем корень проекта в path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from sqlalchemy.orm import Session
from app.data.database import engine, Base, SessionLocal
from app.models.station import Station, station_lines
from app.models.line import Line


# ---------------------------------------------------------------------------
# Настройки
# ---------------------------------------------------------------------------

STATIONS_JSON = ROOT_DIR / "app" / "static" / "css" / "stations.json"

# Цвета для линий — берутся из map-elements.json, но можно переопределить
LINE_COLORS = {
    "line-red": "#F24822",
    "line-blue": "#3DADFF",
    "line-green": "#14EF10",
}


# ---------------------------------------------------------------------------
# CONNECTIONS (Соединения между станциями)
# ---------------------------------------------------------------------------
#
# Seed НЕ создаёт Connections — этот файл отвечает только за линии и станции.
#
# Чтобы добавить соединения, тебе нужно:
#
# 1. Создать JSON-файл (например, scripts/connections.json) с массивом объектов:
#
#    [
#      {"from": "владивосток", "to": "первая_речка", "line": "line-red", "travel_time": 2.0},
#      {"from": "первая_речка", "to": "владивосток", "line": "line-red", "travel_time": 2.0},
#      ...
#    ]
#
# 2. Поля:
#    - "from" / "to" — строковый id станции из stations.json (поле "id")
#    - "line" — имя линии (line-red, line-blue, line-green)
#    - "travel_time" — время в минутах (float)
#
# 3. ВАЖНО: в БД соединения хранятся ДВУНАПРАВЛЕННО
#    (если от A к B можно проехать, то и от B к A тоже).
#    Каждое ребро — отдельная запись в connections.json.
#
# 4. Как добавить в seed:
#
#    def seed_connections(session: Session, connections_data: list, stations_map: dict, lines_map: dict):
#        from app.models.route import Connection
#        count = 0
#        for conn_data in connections_data:
#            from_station = stations_map.get(conn_data["from"])
#            to_station = stations_map.get(conn_data["to"])
#            if not from_station or not to_station:
#                print(f"  ⚠️  Станция не найдена: {conn_data.get('from')} → {conn_data.get('to')}")
#                continue
#            line = lines_map.get(conn_data["line"])
#            connection = Connection(
#                from_station_id=from_station.id,
#                to_station_id=to_station.id,
#                line_id=line.id if line else None,
#                travel_time=conn_data.get("travel_time", 1.0)
#            )
#            session.add(connection)
#            count += 1
#        session.commit()
#        print(f"✓ Добавлено {count} соединений")
#
#    И вызвать в main():
#        with open(ROOT_DIR / "scripts" / "connections.json") as f:
#            conn_data = json.load(f)
#        seed_connections(db, conn_data, stations_map, lines_map)
#


# ---------------------------------------------------------------------------
# Загрузка данных
# ---------------------------------------------------------------------------

def load_stations_json() -> list:
    """Загрузка данных из stations.json."""
    if not STATIONS_JSON.exists():
        print(f"❌ Файл не найден: {STATIONS_JSON}")
        sys.exit(1)
    with open(STATIONS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Очистка БД
# ---------------------------------------------------------------------------

def clear_db(session: Session):
    """Очистка всех таблиц (порядок важен из-за внешних ключей)."""
    # Удаляем соединения, если таблица существует
    from app.models.route import Connection
    session.query(Connection).delete()
    # Очищаем ассоциативную таблицу station_lines
    session.execute(station_lines.delete())
    session.query(Station).delete()
    session.query(Line).delete()
    session.commit()
    print("✓ База данных очищена")


# ---------------------------------------------------------------------------
# Линии
# ---------------------------------------------------------------------------

def extract_lines_from_stations(stations_data: list) -> list:
    """Извлечь уникальные линии из данных станций."""
    seen = set()
    lines = []
    for station in stations_data:
        for line_name in station.get("lines", []):
            if line_name not in seen:
                seen.add(line_name)
                lines.append({
                    "name": line_name,
                    "color": LINE_COLORS.get(line_name, ""),
                })
    return lines


def seed_lines(session: Session, lines_data: list) -> dict:
    """Добавление линий. Возвращает мапу {name: Line}."""
    lines_map = {}
    for line_data in lines_data:
        line = Line(
            name=line_data["name"],
            color=line_data.get("color", ""),
        )
        session.add(line)
        lines_map[line.name] = line
    session.commit()
    print(f"✓ Добавлено {len(lines_data)} линий: {', '.join(l['name'] for l in lines_data)}")
    return lines_map


# ---------------------------------------------------------------------------
# Станции
# ---------------------------------------------------------------------------

def seed_stations(session: Session, stations_data: list, lines_map: dict) -> dict:
    """Добавление станций.

    Возвращает мапу {json_id: Station}, где json_id — строковый id из JSON.
    Это нужно для последующего создания Connection.
    """
    stations_map = {}

    for station_data in stations_data:
        json_id = station_data["id"]              # строка, например "владивосток"
        station_lines_list = station_data.get("lines", [])
        is_transfer = len(station_lines_list) > 1

        station = Station(
            # id не указываем — автоинкремент
            name=station_data["name"],
            is_transfer=is_transfer,
            latitude=station_data.get("y"),        # y → latitude
            longitude=station_data.get("x"),        # x → longitude
            svg_id=json_id,                         # строковый id из JSON → svg_id
        )

        # Связываем станции с линиями
        for line_name in station_lines_list:
            if line_name in lines_map:
                station.lines.append(lines_map[line_name])

        session.add(station)
        # Форсируем flush, чтобы получить сгенерированный id
        session.flush()
        stations_map[json_id] = station

    session.commit()
    print(f"✓ Добавлено {len(stations_data)} станций")
    return stations_map


# ---------------------------------------------------------------------------
# Верификация
# ---------------------------------------------------------------------------

def verify_graph(stations_map: dict, connections_data: list = None):
    """Проверка целостности графа.

    Если connections_data не передан — проверяет только станции.
    """
    print("\n🔍 Проверка...")

    if not connections_data:
        # Проверяем только станции
        transfer_stations = [s for s in stations_map.values() if s.is_transfer]
        print(f"  Станций всего: {len(stations_map)}")
        if transfer_stations:
            print(f"  Пересадочных узлов: {len(transfer_stations)}")
            for ts in transfer_stations[:5]:
                line_names = ", ".join([l.name for l in ts.lines])
                print(f"    - {ts.name} (линии: {line_names})")
        print("  ✓ Станции загружены")
        return

    from collections import defaultdict, deque

    graph = defaultdict(set)
    for conn in connections_data:
        graph[conn["from"]].add(conn["to"])
        graph[conn["to"]].add(conn["from"])

    # Поиск конечных станций (степень 1)
    terminal_stations = [
        name for name, neighbors in graph.items()
        if len(neighbors) == 1
    ]
    if terminal_stations:
        print(f"  Конечные станции: {', '.join(terminal_stations)}")

    # Проверка связности через BFS
    if graph:
        start = next(iter(graph.keys()))
        visited = set()
        queue = deque([start])

        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            queue.extend(graph[node] - visited)

        all_stations = set(graph.keys())
        unreachable = all_stations - visited

        if unreachable:
            print(f"  ⚠️  Найдены изолированные станции: {unreachable}")
        else:
            print(f"  ✓ Граф связный ({len(visited)} станций в компоненте)")

    # Проверка пересадок
    transfer_stations = [s for s in stations_map.values() if s.is_transfer]
    if transfer_stations:
        print(f"  ✓ Пересадочных узлов: {len(transfer_stations)}")
        for ts in transfer_stations[:5]:
            line_names = ", ".join([l.name for l in ts.lines])
            print(f"    - {ts.name} (линии: {line_names})")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Основная функция seed."""
    print("🚇 Запуск seed транспорта...\n")

    # Создание таблиц
    Base.metadata.create_all(bind=engine)
    print("✓ Таблицы созданы/проверены\n")

    # Загрузка данных
    stations_data = load_stations_json()
    print(f"  Загружено {len(stations_data)} станций из stations.json\n")

    # Создание сессии
    db = SessionLocal()

    try:
        # Очистка БД
        clear_db(db)

        # Извлечение линий из данных станций
        lines_data = extract_lines_from_stations(stations_data)

        # Seed линий
        lines_map = seed_lines(db, lines_data)

        # Seed станций
        stations_map = seed_stations(db, stations_data, lines_map)

        # Верификация (без соединений)
        verify_graph(stations_map)

        print("\n✅ Seed завершен успешно!")
        print()
        print("💡 Соединения (Connection) не добавлены.")
        print("   См. раздел CONNECTIONS в seed_transport.py, чтобы добавить их.")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка при seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()