import sqlalchemy
from pprint import pprint

engine = sqlalchemy.create_engine('postgresql://bd_hw4:pass@localhost:5432/bd_hw4')
connection = engine.connect()

# количество исполнителей в каждом жанре;
case1 = connection.execute('''
    SELECT genre.title, COUNT(executor.name) FROM genre
    LEFT JOIN executor_genre ON genre.id = executor_genre.genre_id
    LEFT JOIN executor ON executor_genre.executor_id = executor.id
    GROUP BY title;
    ''').fetchall()
# pprint(case1)

# количество треков, вошедших в альбомы 2019-2020 годов;
case2 = connection.execute('''
    SELECT album.title, COUNT(track.title) FROM album
    JOIN track ON album.id = track.album_id
    WHERE album.year >= 2019 AND album.year <= 2020
    GROUP BY album.title;
    ''').fetchall()
# pprint(case2)

# средняя продолжительность треков по каждому альбому;
case3 = connection.execute('''
    SELECT album.title, ROUND(AVG(track.duration), 1) FROM album
    LEFT JOIN track ON album.id = track.album_id
    GROUP BY album.title;
    ''').fetchall()
# pprint(case3)

# все исполнители, которые не выпустили альбомы в 2020 году;
case4 = connection.execute('''
    SELECT executor.name FROM executor
    LEFT JOIN executor_album ON executor.id = executor_album.executor_id
    LEFT JOIN album ON executor_album.album_id = album.id
    WHERE NOT album.year = 2020;
    ''').fetchall()
# pprint(case4)

# названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
case5 = connection.execute('''
    SELECT collection.title FROM collection
    JOIN track_collection ON collection.id = track_collection.collection_id
    JOIN track ON track_collection.track_id = track.id
    JOIN album ON track.album_id = album.id
    JOIN executor_album ON album.id = executor_album.album_id
    JOIN executor ON executor_album.executor_id = executor.id
    WHERE executor.name = 'the offspring'
    GROUP BY collection.title;
    ''').fetchall()
# pprint(case5)

# название альбомов, в которых присутствуют исполнители более 1 жанра;
case6 = connection.execute('''
    SELECT album.title FROM album
    JOIN executor_album ON album.id = executor_album.album_id
    JOIN executor ON executor_album.executor_id = executor.id
    JOIN executor_genre ON executor.id = executor_genre.executor_id
    JOIN genre ON executor_genre.genre_id = genre.id
    GROUP BY album.title
    HAVING COUNT(genre.title) > 1;
    ''').fetchall()
# pprint(case6)

# наименование треков, которые не входят в сборники;
case7 = connection.execute('''
    SELECT track.title FROM track
    LEFT JOIN track_collection ON track.id = track_collection.track_id
    LEFT JOIN collection ON track_collection.collection_id = collection.id
    GROUP BY track.title
    HAVING COUNT(collection.title) = 0;
    ''').fetchall()
# pprint(case7)

# исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
case8 = connection.execute('''
    SELECT e.name FROM executor e
    JOIN executor_album ea ON e.id = ea.executor_id
    JOIN album a ON ea.album_id = a.id
    JOIN track t ON a.id = t.album_id
    GROUP BY e.name
    HAVING MIN(t.duration) = 
        (
            SELECT MIN(duration) FROM track
        );
    ''').fetchall()
# pprint(case8)

# название альбомов, содержащих наименьшее количество треков.
case9 = connection.execute('''
    SELECT album.title FROM album
    JOIN track ON album.id = track.album_id
    GROUP BY album.title
    HAVING COUNT(track.title) =
        (
            SELECT MIN(count_track) FROM
                (
                    SELECT COUNT(track.title) count_track FROM album
                    JOIN track ON album.id = track.album_id
                    GROUP BY album.title
                ) x
        );
    ''').fetchall()
pprint(case9)