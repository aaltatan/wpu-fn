from apps.faculties.models import Faculty
from rich import print

def run() -> None:
    
    qs = Faculty.objects.values('id', 'name')
    print(qs)