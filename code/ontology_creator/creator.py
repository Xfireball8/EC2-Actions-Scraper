import json # Interpreting results from Scrapy
import os # Check if file exists
import sys # breakpoints


# Create a simple OWL class declaration 
# Input : rdfId - Name of the class
# Output : String - Declaration 
def owlClassTag(rdfId):
    openTag = "<owl:Class rdf:ID=\"" + rdfId + "\" />" + '\n' 
    return openTag

# Get a dictionnary from scrapped resources
# Input : 
# Output : resourcesDictionnary - Python Dict
def getResources():
    try:
        resourcesFile = open("res/resources.json")
    except OSError:
        print("You need to generate resources with the scrapy spider first !")
        sys.exit()
    # ...[0] <- json.load returns an array with your json accesible in the first row
    # ...[0]['res'] <- There can be only one top level object in a json read by json.load
    #                   so 'res' is where there is our array of dict (Actions/Resources/Conditions)
    #....[0]['res'][1] <- index 1 correspond to our Resource Dict
    resourcesDictionnary = json.load(resourcesFile)[0]['res'][1] # json.load put my dict in an array
    return resourcesDictionnary

# Get a dictionnary from scrapped actions
# Input : 
# Output : actionsDictionnary - Python Dict
def getActions():
    try:
        resourcesFile = open("res/resources.json")
    except OSError:
        print("You need to generate resources with the scrapy spider first !")
        sys.exit()
    # ...[0] <- json.load returns an array with your json accesible in the first row
    # ...[0]['res'] <- There can be only one top level object in a json read by json.load
    #                   so 'res' is where there is our array of dict (Actions/Resources/Conditions)
    #....[0]['res'][0] <- index 0 correspond to our Action Dict
    actionsDictionnary = json.load(resourcesFile)[0]['res'][0]
    return actionsDictionnary

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

# Create a simple OWL class declaration 
# Input : rdfId - Name of the class
# Output : String - Declaration 
def owlIndividualTag(owlClassName, rdfId):
    openTag = "<" + owlClassName  +" rdf:ID=\"" + rdfId + "\" />" + '\n' 
    return openTag


# We create individuals of our ontology
# Input : ontologyFile - File handle
#         resourcesDictionnary - Python Dict
# Output : 
def defineIndividuals(ontologyFile, resourcesDictionnary):
    for owlClassId in resourcesDictionnary.keys():
        individuals = resourcesDictionnary[owlClassId]
        for owlIndividualId in individuals:
            ontologyFile.write(owlIndividualTag(owlClassId, owlIndividualId))

# We get the data we just scrapped in a Dict form
# and we call the functions to build our ontology
# accordingly to these data
# Input : ontologyFile - File Handle
# Output :
def defineOntology(ontologyFile):
    resourcesDictionnary = getResources()
    actionsDictionnary = getActions()
    defineClasses(ontologyFile, resourcesDictionnary)
    defineClasses(ontologyFile, actionsDictionnary)
    defineIndividuals(ontologyFile, resourcesDictionnary)
    defineIndividuals(ontologyFile, actionsDictionnary)

# Main function call
def createOntology():
    ontologyFile = createOntologyFile()
    defineOntology(ontologyFile)
    ontologyFile.close()
    print("Ontology generation has ended !")

createOntology()
