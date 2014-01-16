from django.db import models
from django.contrib.auth.models import User

# these models are elements of the mangal data specification

M_NAME = 400
D_NAME = 1000

# taxa
class Taxa(models.Model):
   name = models.CharField(max_length=M_NAME, unique=True, help_text = "The scientific name of the taxa")
   owner = models.ForeignKey(User, related_name ="%(app_label)s_%(class)s_owner")
   vernacular = models.CharField(max_length=M_NAME, help_text = "The vernacular name of the taxa, in English", blank=True, null=True)
   description = models.CharField(max_length=D_NAME,blank=True,null=True, help_text = "A short description of the taxa")
   ncbi = models.IntegerField(blank=True,null=True, unique=True, help_text = "The NCBI Taxonomy identifier of the taxa")
   gbif = models.IntegerField(blank=True,null=True, unique=True, help_text = "The GBIF identifier of the taxa")
   bold = models.IntegerField(blank=True,null=True, unique=True, help_text = "The BOLD identifier of the taxa")
   itis = models.IntegerField(blank=True,null=True, unique=True, help_text = "The ITIS identifier of the taxa")
   eol = models.IntegerField(blank=True,null=True, unique=True, help_text = "The EOL identifier of the taxa")
   def __unicode__(self):
       na = self.name
       if len(self.vernacular) > 0:
           na += " ("+self.vernacular+")"
       return na

# population
class Population(models.Model):
   taxa = models.ForeignKey(Taxa)
   name = models.CharField(max_length=M_NAME, help_text = "A name allowing to identify the population")
   owner = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_owner", help_text = "The identifier of the uploader")
   description = models.CharField(max_length=D_NAME,blank=True,null=True, help_text = "A short description of the population")
   def __unicode__(self):
       return u'%s, of taxa %s' % (self.name, self.taxa)

# trait
class Trait(models.Model):
   name = models.CharField(max_length=M_NAME, help_text  = "The name of the measured trait")
   owner = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_owner", help_text = "The identifier of the uploader")
   value = models.CharField(help_text = "The value of the trait", max_length=50)
   units = models.CharField(max_length=50, help_text = "Units in which the trait was measured", blank=True, null=True)
   description = models.CharField(max_length=D_NAME,blank=True,null=True, help_text = "A longer description of the trait")
   def __unicode__(self):
       return u'%s (%.4f %s)' % (self.name, self.value, self.units)

# item
class Item(models.Model):
   STAGE_CHOICES = (
           ('seed', 'Seed'),
           ('juvenile', 'Juvenile'),
           ('adult', 'Adult'),
           ('dead', 'Dead'),
           ('larva', 'Larva'),
           ('all', 'All'),
           )
   public = models.BooleanField(default=True)
   owner = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_owner", help_text = "The identifier of the uploader")
   population = models.ForeignKey(Population)
   level = models.CharField(max_length=50, choices = (('individual', 'Individual'), ('population', 'Population'),), help_text = "Whether the item is a single individual, or a population")
   name = models.CharField(max_length=M_NAME, help_text = "A name for the item, useful to identify it later")
   stage = models.CharField(max_length=50, choices = STAGE_CHOICES, default = 'all', help_text = "The stage of the item, to be selected in the list of allowed values")
   traits = models.ManyToManyField(Trait,blank=True,null=True)
   size = models.FloatField(blank=True,null=True, help_text = "If the item is a population, the number of individuals or biomass")
   units = models.CharField(max_length=50,blank=True,null=True, help_text = "Units in which the population size is measured")
   description = models.CharField(max_length=D_NAME,blank=True,null=True, help_text = "A short description of the population")
   def __unicode__(self):
       return u'%s (%s) - belongs to %s' % (self.name, self.level, self.population)

# interaction
class Interaction(models.Model):
   TYPE_CHOICES = (
           ('predation', 'Predation'),
           ('ectoparasitism', 'Ectoparasitism'),
           ('endoparasitism', 'Endoparasitism'),
           ('intra-cellular parasitism', 'Intra-Cellular parasitism'),
           ('parasitoidism', 'Parasitoidism'),
           ('mycoheterotrophy', 'Mycoheterotrophy'),
           ('antixenosis', 'Anitxenosis'),
           ('teletoxy', 'Teletoxy'),
           ('amensalism', 'Amensalism'),
           ('antibiosis', 'Antibiosis'),
           ('allelopathy', 'Allelopathy'),
           ('competition', 'Competition'),
           ('facilitation', 'Facilitation'),
           ('refuge creation', 'Refuge creation'),
           ('inquilinism', 'Inquilinism'),
           ('phoresis', 'Phoresis'),
           ('epibiosis', 'Epibiosis'),
           ('pollination', 'Pollination'),
           ('mutualistic symbiosis', 'Mutualistic symbiosis'),
           ('zoochory', 'Zoochory'),
           ('mutual protection', 'Mutual protection'),
        )
   OBSERVATION_CHOICES = (
           ('unspecified', 'Unspecified'),
           ('observation', 'Observation'),
           ('litterature', 'Litterature'),
           ('absence', 'Confirmed absence'),
           ('inferred', 'Inferred'),
           )
   link_type = models.CharField(max_length=50, choices = TYPE_CHOICES, help_text  ="The type of interaction")
   obs_type = models.CharField(max_length=50, choices = OBSERVATION_CHOICES, help_text  ="How the interaction was observed")
   owner = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_owner")
   taxa_from = models.ForeignKey(Taxa, related_name='taxa_from')
   taxa_to = models.ForeignKey(Taxa, related_name='taxa_to')
   pop_from = models.ForeignKey(Population, related_name='pop_from', blank=True, null=True)
   pop_to = models.ForeignKey(Population, related_name='pop_to', blank=True, null=True)
   item_from = models.ForeignKey(Item, related_name='item_from', blank=True, null=True)
   item_to = models.ForeignKey(Item, related_name='item_to', blank=True, null=True)
   strength_f = models.FloatField(blank=True,null=True, help_text = "The strength of the interaction for the item ESTABLISHING the interaction")
   strength_t = models.FloatField(blank=True,null=True, help_text = "The strength of the interaction for the item RECEVING the interaction")
   units_f = models.CharField(max_length=50,blank=True,null=True, help_text = "Units in which the interaction strength is measured")
   units_t = models.CharField(max_length=50,blank=True,null=True, help_text = "Units in which the interaction strength is measured")
   description = models.CharField(max_length=D_NAME,blank=True,null=True, help_text = "A description of the interaction")
   def __unicode__(self):
       From = self.taxa_from
       To = self.taxa_to
       if self.pop_from :
          From = self.pop_from
       if self.pop_to:
          To = self.pop_to
       if self.item_from :
          From = self.item_from
       if self.item_to:
          To = self.item_to
       return u'%s of %s by %s'% (self.ecotype, To, From)


# environment
class Environment(models.Model):
   name = models.CharField(max_length=M_NAME, help_text = "The environmental property being measured")
   owner = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_owner")
   value = models.CharField(help_text = "The value of the environmental property", max_length = 50)
   units = models.CharField(max_length=50, help_text = "The units in which the environmental property is measured", blank=True, null=True)
   description = models.CharField(max_length=D_NAME,blank=True,null=True, help_text = "A description of the environmental property")
   def __unicode__(self):
      return u'%s (%.4f %s)' % (self.name, self.value, self.units)

# network
class Network(models.Model):
   public = models.BooleanField(default=True)
   owner = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_owner")
   name = models.CharField(max_length=M_NAME, help_text = "The name of the network")
   description = models.CharField(max_length=D_NAME,blank=True,null=True, help_text = "A short description of the network")
   interactions = models.ManyToManyField(Interaction)
   date = models.CharField(max_length=10,blank=True,null=True, help_text = "The date at which the network was sampled")
   latitude = models.CharField(max_length=20,blank=True,null=True, help_text = "Latitude")
   longitude = models.CharField(max_length=20,blank=True,null=True, help_text = "Longitude")
   environment = models.ManyToManyField(Environment,blank=True,null=True)
   def __unicode__(self):
       return self.name

# reference
class Ref(models.Model):
   doi = models.CharField(max_length=200, blank=True, null=True, help_text = "DOI of the reference object")
   owner = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_owner")
   jstor = models.CharField(max_length=200, blank=True, null=True, help_text = "JSTOR identifier of the reference object")
   pmid = models.CharField(max_length=200, blank=True, null=True, help_text = "PubMed ID of the reference object")
   url = models.CharField(max_length=200, blank=True, null=True, help_text = "URL of the reference object")

# dataset
class Dataset(models.Model):
   public = models.BooleanField(default=True)
   owner = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_owner")
   name = models.CharField(max_length=M_NAME, help_text = "The name of the dataset")
   description = models.CharField(max_length=D_NAME,blank=True,null=True, help_text = "A short description of the dataset")
   papers = models.ManyToManyField(Ref, related_name='papers',blank=True,null=True)
   data = models.ManyToManyField(Ref, related_name='data',blank=True,null=True)
   networks = models.ManyToManyField(Network,blank=True,null=True)
   def __unicode__(self):
       return self.name