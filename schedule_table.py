from PyQt5.QtWidgets import QTableWidget,QHeaderView,QVBoxLayout,QTableWidgetItem,QWidget
from PyQt5.QtCore import Qt
import random
import schedule

class ScheduleTable(QWidget):
  def __init__(self,tab_tree_view):
    super().__init__()
    self.tables=[]  #테이블 객체
    self.tab_tree_view=tab_tree_view
    self.schedule_time={}  #{'table_0': ['09:37', '10:43', '14:40', '18:44', '22:19'], 'table_1': ['13:43', '15:37', '16:44', '21:40', '23:44']}
    # 테이블 헤더 설정
    self.table_titles = [
        ["모닝","오전 우편", "오후 우편", "저녁 우편", "밤 우편"],
        ["파괴된성채", "크루마탑", "안타라스","시즌패스", "격전의섬"]
    ]
    
    # 메인 레이아웃
    layout = QVBoxLayout()
    # 두 개의 테이블 생성
    for titles in self.table_titles:
      table = self.create_table(titles)
      self.tables.append(table)
      layout.addWidget(table)
    self.setLayout(layout)
      
  def create_table(self, titles):
    table = QTableWidget(1, 5)  # 1행 5열 테이블 생성
    table.setHorizontalHeaderLabels(titles)  # 열 제목 설정
    table.verticalHeader().setVisible(False)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #수평헤더고 크기가 위젯에 맞춰짐
    table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch) #수직헤더고 크기가 위젯에 맞춰짐
    
    return table
    
  def set_data(self): #데이터를 이 함수를 이용해 세팅해줘야 한다
    pass
  
  def set_schedule_with_time(self, header_title):
    for computer_id in self.tab_tree_view.tab_contents.keys():
      buttons_dict = {
          **self.tab_tree_view.tab_contents[computer_id].tabTreeview_btn_img.dungeon_buttons,
          **self.tab_tree_view.tab_contents[computer_id].tabTreeview_btn_img.routine_buttons,
          **self.tab_tree_view.tab_contents[computer_id].tabTreeview_btn_img.setting_buttons,
      }
      
      for title in buttons_dict.keys():
        if title==header_title:
          button=buttons_dict[title]
          self.tab_tree_view.tab_contents[computer_id].tabTreeview_btn_img.send_to_command(button)  
          break

  # 스케줄 설정 함수
  def setup_schedule(self, schedule_time, table_headers):
    for table_key, times in schedule_time.items():
      table_index = int(table_key.split('_')[1])  # table_0, table_1 등에서 인덱스 추출
      headers = table_headers[table_index]  # 해당 테이블의 헤더 가져오기
    
      for idx, scheduled_time in enumerate(times):
        header_title = headers[idx].split()[-1]  # 현재 컬럼의 헤더 제목
        schedule.every().day.at(scheduled_time).do(self.set_schedule_with_time, header_title).tag('routine')
    
    print("등록된 스케쥴: ", schedule.jobs)

  def schedule_table_time_set(self): 
    print("스케줄 설정 버튼 클릭됨")
    schedule.clear(tag='routine')
    min=[]
    time_list=[]
    for i in range(5):
      min.append(str(random.randint(10, 50))) 
    
    hours_list=[
      ["09","10","14","18","22"],
      ["13","15","16","21","23"] #파괴, 크루마, 안타, 시즌패스, 격섬
    ]

    for idx, table in enumerate(self.tables):
      hours=hours_list[idx]
      for column, hour in enumerate(hours):  
        minutes=random.choice(min)
        time=f"{hour}:{minutes}"
        schedule_time=QTableWidgetItem(time)
        schedule_time.setTextAlignment(Qt.AlignCenter)
        table.setItem(0, column, schedule_time)
        time_list.append(time)
      self.schedule_time[f"table_{idx}"]=time_list
      time_list=[]  #리스트 초기화
    # print(self.schedule_time)
    self.setup_schedule(self.schedule_time, self.table_titles)

    
#시간이 되면 contextmenu가 실행되야 한다.

     
  # schedule.every().day.at(setTimePostbox[1]).do(schedulePostBox,1).tag('routine')