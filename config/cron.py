from datetime import datetime

from movies.models   import MovieTheater

def DeleteObjects():
    MovieTheater.objects.filter(start_time__lte = datetime.now()).delete()
    print("====================")
    print("Success To Delete")
    print(datetime.now())
    return