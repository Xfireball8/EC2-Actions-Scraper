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
    resourcesDictionnary = json.load(resourcesFile)[0]['res'][1]
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

# Before we can use a set of terms, we need a precise indication of what specific
# vocabularies are being used.
# Hence we include a set of XML namespace declarations in our ontology
# Input : ontologyFile - File handle 
# Output : 
def defineHeader(ontologyFile):
    xmlTag = "<?xml version=\"1.0\"?>\n"
    xmlDOCTYPE = "<!DOCTYPE rdf:RDF [\n\t<!ENTITY owl \"http://www.w3.org/2002/07/owl#\">\n\t<!ENTITY xsd \"http://www.w3.org/2001/XMLSchema#\" >\n]>\n"
    xmlNamespaceTag = "<rdf:RDF\n\txmlns:owl =\"http://www.w3.org/2002/07/owl#\"\n\txmlns:rdf =\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n\txmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n\txmlns:xsd =\"http://www.w3.org/2001/XMLSchema#\">\n"
    
    ontologyTag = "\t<owl:Ontology rdf:about=\"\">\n\t\t<rdfs:comment>A ontology for EC2 IAM RBAC</rdfs:comment>\n\t</owl:Ontology>\n"
    ontologyFile.write(xmlTag)
    ontologyFile.write(xmlDOCTYPE)
    ontologyFile.write(xmlNamespaceTag)
    ontologyFile.write(ontologyTag)

# Close the <rdf:RDF> tag 
# Input : ontologyFile - File Handle
# Output : 
def defineFooter(ontologyFile):
    footer = "\n</rdf:RDF>"
    ontologyFile.write(footer)

# Returns the tag for the subproperty specification
# in a property definition.
# Input : owlSubPropertyOf - The name of the property
# Output : String - The tag that can be used to define the property
def owlSubPropertyOfTag(owlSubPropertyOf):
    if owlSubPropertyOf == "None": 
        return "" 
    else:
        return "\t<rdfs:subPropertyOf rdf:resource=\"#" + owlSubPropertyOf + "\"/>\n"


# Create the property tag with value in the corresponding inputs
# Input :   owlId - String (Name of the property)
#           owlDomain - String (Class on which is applied the property)
#           owlRange - String (Class related to the domain)
#           owlSubclassOf - If a P' property is specified it is inferred by a reasoner
#                           that for this P property : P(x,y) iff P'(x,y).
#                           (Name of the property, String)
# Output : String - The tag that can be used to define the property
def owlPropertyTag(owlId, owlDomain, owlRange, owlSubPropertyOf="None"):
    return ("<owl:ObjectProperty rdf:ID=\"" + owlId  + "\">\n\t" +
                "<rdfs:domain rdf:resource=\"#" + owlDomain + "\"/>\n\t" +
                "<rdfs:range rdf:resource=\"#" + owlRange + "\" />\n" +
                owlSubPropertyOfTag(owlSubPropertyOf) +
            "</owl:ObjectProperty>\n")
                    
# We define the properties of our ontology see
# ontology reference to have a list of them
# Input : ontologyFile - File Handle
# Output : 
def defineProperties(ontologyFile):
    ontologyFile.write(owlPropertyTag("appliesTo","Ec2Actions","Ec2Resources"))
    ontologyFile.write(owlPropertyTag("requires","Ec2Actions","Ec2Resources","appliesTo"))

# We get the data we just scrapped in a Dict form
# and we call the functions to build our ontology
# accordingly to these data
# Input : ontologyFile - File Handle
# Output :
def defineOntology(ontologyFile):
    resourcesDictionnary = getResources()
    actionsDictionnary = getActions()
    defineHeader(ontologyFile)
    defineClasses(ontologyFile, resourcesDictionnary)
    defineClasses(ontologyFile, actionsDictionnary)
    defineProperties(ontologyFile)
    defineIndividuals(ontologyFile, resourcesDictionnary)
    defineIndividuals(ontologyFile, actionsDictionnary)
    defineFooter(ontologyFile)

# Main function call
def createOntology():
    ontologyFile = createOntologyFile()
    defineOntology(ontologyFile)
    ontologyFile.close()
    print("Ontology generation has ended !")

createOntology()
