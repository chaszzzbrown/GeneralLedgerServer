from django.db import models

# Create your models here.
class SessionData(models.Model):
    
    custom_resource_id = models.CharField(max_length=80)
    user_id = models.CharField(max_length=80)
    
    launch_data = models.TextField()    # contains the TPI Launch data for the most recent launch, as a JSON encoded dict
    
    problem_state_data = models.TextField()
                                        # contains the most recently saved student data, encoded as JSON
                                        
    class Meta:
        unique_together = ('custom_resource_id', 'user_id')
        index_together = ('custom_resource_id', 'user_id')
    
    