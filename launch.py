import os

def main():
    os.system("python manage.py db init")
    os.system("python manage.py db migrate")
    os.system("python manage.py db upgrade")
    os.system("python app.py")

if __name__ == "__main__":
    main()