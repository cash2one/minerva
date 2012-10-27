

# Load the AlchemyAPI module code.
import AlchemyAPI

query = raw_input()
# Create an AlchemyAPI object.
alchemyObj = AlchemyAPI.AlchemyAPI()


# Load the API key from disk.
alchemyObj.loadAPIKey("api_key.txt")


# Extract a ranked list of named entities from a web URL.
#result = alchemyObj.URLGetRankedNamedEntities("http://www.techcrunch.com/");
#print (result)


# Extract a ranked list of named entities from a text string.
result = alchemyObj.TextGetRankedNamedEntities(query)
print (result)


# Load a HTML document to analyze.
#htmlFileHandle = open("data/example.html", 'r')
#htmlFile = htmlFileHandle.read()
#htmlFileHandle.close()


# Extract a ranked list of named entities from a HTML document.
#result = alchemyObj.HTMLGetRankedNamedEntities(htmlFile, "http://www.test.com/");
#print (result)


