# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class Menu:
    def __init__(self):
        pass
    def user_input(self):
        while True:
            action = input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n")
            today = datetime.today()
            if action == "1":
                rows = session.query(Table).filter(Table.deadline == today.date()).all()
                print("Today", " ", today.day, " ", today.strftime("%b"), ":", sep="")
                if not rows:
                    print("Nothing to do!\n")
                else:
                    for index, row in enumerate(rows):
                        print(f"{index + 1}. {row.task}")
            elif action == "2":
                rows = session.query(Table).filter(Table.deadline == today.date()).all()
                print("\n", today.strftime('%A'), " ", today.day, " ", today.strftime("%b"), ":", sep="")
                if not rows:
                    print("Nothing to do!")
                else:
                    for index, row in enumerate(rows):
                        print(f"{index + 1}. {row.task}")
                next_day = today
                for i in range(6):
                    next_day = next_day + timedelta(days=1)
                    rows = session.query(Table).filter(Table.deadline == next_day.date()).all()
                    print("\n", next_day.strftime('%A'), " ", next_day.day, " ", next_day.strftime("%b"), ":", sep="")
                    if not rows:
                        print("Nothing to do!")
                    else:
                        for index, row in enumerate(rows):
                            print(f"{index + 1}. {row.task}")
            elif action == "3":
                print("All tasks:")
                rows = session.query(Table).order_by(Table.deadline).all()
                for index, row in enumerate(rows):
                        print(f"{index + 1}. {row.task}. {row.deadline.strftime('%-d %b')}")
            elif action == "4":
                rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
                print("Missed tasks:")
                if not rows:
                    print("Nothing is missed!")
                else:
                    for index, row in enumerate(rows):
                        print(f"{index + 1}. {row.task}. {row.deadline.strftime('%-d %b')}")
                    print("")
            elif action == "5":
                my_task = input("Enter task")
                task_date = input("Enter deadline")
                print("The task has been added!")
                new_row = Table(task = my_task, deadline=datetime.strptime(task_date, "%Y-%m-%d").date())
                session.add(new_row)
                session.commit()
            elif action == "6":
                rows = session.query(Table).order_by(Table.deadline).all()
                if not rows:
                    print("Nothing to delete")
                else:
                    print("Choose the number of the task you want to delete:")
                    for index, row in enumerate(rows):
                        print(f"{index + 1}. {row.task}. {row.deadline.strftime('%-d %b')}")
                    to_delete = int(input())
                    specific_row = rows[to_delete-1]
                    session.delete(specific_row)
                    session.commit()
                    print("The task has been deleted!")
            elif action == "0":
                print("Bye!")
                break

go = Menu()
go.user_input()