--  1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів


--  2. Знайти студента із найвищим середнім балом з певного предмета
    select full_name, s2.subject_name, avg(score)
    from students s
        join grades g ON s.id = g.student_id
        join subjects s2 ON g.subject_id = s2.id
    where s2.id = 1
    group by s2.subject_name, s.full_name
    order by avg(g.score) desc
    limit 1;


--  3. Знайти середній бал у групах з певного предмета
    select g.group_name, s2.subject_name, ROUND(AVG(g2.score), 2)
    from "groups" g
        join students s on g.id = s.group_id
        join grades g2 on s.id = g2.student_id
        join subjects s2 on g2.subject_id = s2.id
    where s2.id = 1
    group by g.group_name, s2.subject_name
    order by g.group_name;


--  4. Знайти середній бал на потоці (по всій таблиці оцінок)
    select round(avg(score), 2)
    from grades g;


--  5. Знайти які курси читає певний викладач
    select t.full_name, s.subject_name
    from teachers t
        join subjects s ON t.id = s.teacher_id
    where t.id = 3;


--  6. Знайти список студентів у певній групі
    select s.full_name, g.group_name
    from "groups" g
        join students s on g.id = s.group_id
    where g.id = 1
    order by s.full_name;


--  7. Знайти оцінки студентів у окремій групі з певного предмета
    select s.full_name, g.group_name, s2.subject_name, g2.score, g2.score_date
    from "groups" g
        join students s on g.id = s.group_id
        join grades g2 on s.id = g2.student_id
        join subjects s2 on g2.subject_id = s2.id
    where g.id = 1 and s2.id = 1
    order by s.full_name;


--  8. Знайти середній бал, який ставить певний викладач зі своїх предметів
    select t.full_name, s.subject_name, round(avg(g.score), 2)
    from teachers t
        join subjects s on t.id = s.teacher_id
        join grades g on s.id = g.subject_id
    where t.id = 3
    group by t.full_name, s.subject_name
    order by s.subject_name;


--  9. Знайти список курсів, які відвідує певний студент
    select s.full_name, s2.subject_name
    from students s
        join grades g on s.id = g.student_id
        join subjects s2 on g.subject_id = s2.id
    where s.id = 1
    group by s.full_name, s2.subject_name
    order by s.full_name;


--  10. Список курсів, які певному студенту читає певний викладач
    select s.full_name, s2.subject_name, t.full_name
    from students s
        join grades g on s.id = g.student_id
        join subjects s2 on g.subject_id = s2.id
        join teachers t on s2.teacher_id = t.id
    where s.id = 1 and t.id = 3
    group by s.full_name, s2.subject_name, t.full_name
    order by s2.subject_name;


--  11. Середній бал, який певний викладач ставить певному студентові
    select t.full_name, round(avg(g.score), 2), s.full_name
    from students s
        join grades g on s.id = g.student_id
        join subjects s2 on g.subject_id = s2.id
        join teachers t on s2.teacher_id = t.id
    where s.id = 1 and t.id = 3
    group by t.full_name, s.full_name;


--    12. Оцінки студентів у певній групі з певного предмета на останньому занятті
    select s.full_name, g.group_name, s2.subject_name, g2.score, g2.score_date
    from students s
        join "groups" g on s.group_id = g.id
        join grades g2 on s.id = g2.student_id
        join subjects s2 on g2.subject_id = s2.id
    where g.id = 1 and s2.id = 1
        and g2.score_date = (
            select max(g3.score_date)
            from grades g3 join students s3 on g3.student_id = s3.id
            where g3.subject_id = s2.id
                and s3.group_id = g.id
        );






