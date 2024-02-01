import pandas as pd

data = pd.read_excel('data/db_parimate.xlsx')

xlsx = pd.ExcelFile('data/db_parimate.xlsx')
users = pd.read_excel(xlsx, 'parimate_users')
reports = pd.read_excel(xlsx, 'parimate_reports')
chats = pd.read_excel(xlsx, 'parimate_chats')
notifications = pd.read_excel(xlsx, 'parimate_notifications')


personal_data = users[['user_id', 'name', 'age', 'sex', 'username', 'date_registration']] # Таблица с ПД
habit_data = users[['user_id', 'habit_category', 'habit_choice', 'habit_frequency', 
                    'habit_report', 'habit_mate_sex', 'habit_notification_day', 'habit_notification_time', 
                    'habit_week']] # Таблица с информацией о привычках
pari_data = users[['user_id', 'pari_mate_id', 'pari_chat_link', 'pari_reports', 
                    'time_find_start', 'time_pari_start', 'time_pari_end']] # Таблица с информацией о созданных чатах


personal_data.to_csv('pers_data.csv', index=False)
habit_data.to_csv('habit_data.csv', index=False)
pari_data.to_csv('pari_data.csv', index=False)