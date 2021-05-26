import json # Interpreting results from Scrapy
import os # Check if file exists

# Create a simple OWL class declaration 
# Input : rdfId - Name of the class
# Output : String - Declaration 
def owlClassTag(rdfId):
    openTag = "<owl:Class rdf:ID=\"" + rdfId + "\" />" + '\n' 
    closeTag = "</owl:Class>" + '\n'
    return openTag + closeTag

# Get a dictionnary from scrapped resources
# Input : 
# Output : resourcesDictionnary - Python Dict
def getResources():
    try:
        resourcesFile = open("res/resources.json")
    except OSError:
        print("You need to generate resources with the scrapy spider first !")
        sys.exit()
    resourcesDictionnary = json.load(resourcesFile)[0] # json.load put my dict in an array
    return resourcesDictionnary

# Open a file to create our ontology, if file
# is already present, we override it.
# Input :
# Output : ontologyFile - File object
def createOntologyFile():
    ontologyFilePath = "res/ec2-ontology.owl"
    try:
        os.remove(ontologyFilePath)
    except OSError:
        pass
    ontologyFile = open(ontologyFilePath,"w")
    return ontologyFile

# We iterate over the dictionnary keys appending the corresponding
# OWL class tag declarations to the ontologyFile
# Input : ontologyFile - File object
#         resourcesDictionnary - Python Dict
# Output : 
def defineClasses(ontologyFile, resourcesDictionnary):
    for owlClassId in resourcesDictionnary.keys():
        ontologyFile.write(owlClassTag(owlClassId))

# We get the key of our dictionnary that correspond to
# the OWL Class of our ontology and we define them in
# our ontology file.
# Input : ontologyFile - File object
# Ouput : 
def createClasses(ontologyFile):
    resourcesDictionnary = getResources()
    defineClasses(ontologyFile, resourcesDictionnary)

# Main function call
def createOntology():
    ontologyFile = createOntologyFile()
    createClasses(ontologyFile)
    ontologyFile.close()
    print("Ontology generation has ended !")

createOntology()
