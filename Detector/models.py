from django.db import models

class Pacient(models.Model):
    NSS = models.CharField(max_length=10)
    Prenume = models.CharField(max_length=100)
    Nume = models.CharField(max_length=100)
    Email = models.EmailField()
    Vârstă = models.IntegerField()
    Sex = models.IntegerField(choices=[(1, 'Bărbat'), (2, 'Femeie')])
    Înălțime = models.FloatField()
    Greutate = models.FloatField()
    TAS = models.IntegerField()
    TAD = models.IntegerField()
    Colesterol = models.IntegerField(choices=[(1, 'Normal'), (2, 'Above Normal'), (3, 'Well Above Normal')])
    Glucoză = models.IntegerField(choices=[(1, 'Normal'), (2, 'Above Normal'), (3, 'Well Above Normal')])
    Fumător = models.IntegerField(choices=[(0, 'Nu'), (1, 'Da')])
    Băutor = models.IntegerField(choices=[(0, 'Nu'), (1, 'Da')])
    Activitate = models.IntegerField(choices=[(0, 'Nu'), (1, 'Da')])
    Risc_Boală = models.FloatField(blank=True, default=None)
    Dată_Adăugare = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Pacient"
        verbose_name_plural = "Pacienți"
    
    def __str__(self):
        return f'{self.Prenume} {self.Nume}'