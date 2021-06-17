from DB.DBConnection import DBConnection


class PlayerInfoTable:
    def insert_a_player(self, player):
        name = player['name']
        password = player['password']
        command = "INSERT INTO player_info VALUES ('{}','{}','0','0');".format(name, password)
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
            
    def select_a_player(self, name):
        command = "SELECT * FROM player_info WHERE name='{}';".format(name)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
            
        return [row for row in record_from_db]

    def login_check(self, name, password):
        command = "SELECT * FROM player_info WHERE name='{}' and password='{}';".format(name, password)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
            
        return [row for row in record_from_db]
    
    def delete_a_student(self, stu_id):
        command = "DELETE FROM student_info WHERE stu_id='{}';".format(stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def update_a_player(self, name, win_count, lose_count):
        command = "UPDATE player_info SET win='{}', loss='{}' WHERE name='{}';".format(win_count, lose_count, name)
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def select_all_student(self):
        command = "SELECT * FROM student_info;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
            
            student_list = []
            for row_id, col_name in record_from_db:
                student_list.append({'stu_id': row_id, 'name': col_name})
            
        return student_list