from django.db import models


class SliderLocation(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Slider(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to='images/sliders',default ='common/placeholder.png')
    slider_location = models.ForeignKey(to='ui.SliderLocation',on_delete=models.SET_NULL,null=True,blank=True)
    action_url = models.URLField(null=False, blank=True)

    def __str__(self):
        return self.title
        