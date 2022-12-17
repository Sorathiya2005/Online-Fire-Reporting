from django.db import models

# Create your models here.
class Teams(models.Model):
    teamName = models.CharField(max_length=200, null=True)
    teamLeaderName = models.CharField(max_length=250, null=True)
    teamLeadMobno = models.CharField(max_length=15, null=True)
    teamMembers = models.CharField(max_length=300, null=True)
    postingDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.teamName

class Firereport(models.Model):
    FullName = models.CharField(max_length=250, null=True)
    MobileNumber = models.CharField(max_length=12, null=True)
    Location = models.CharField(max_length=200, null=True)
    Message = models.CharField(max_length=200, null=True)
    AssignTo = models.ForeignKey(Teams, on_delete=models.CASCADE, null=True)
    Status = models.CharField(max_length=150, null=True)
    Postingdate = models.DateTimeField(auto_now_add=True)
    AssignedTime = models.CharField(max_length=150, null=True)
    UpdationDate = models.DateTimeField(null=True)

    def __str__(self):
        return self.FullName

class Firetequesthistory(models.Model):
    firereport = models.ForeignKey(Firereport, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=200, null=True)
    remark = models.CharField(max_length=250, null=True)
    postingDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status



