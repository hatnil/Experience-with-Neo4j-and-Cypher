from qwikidata.sparql  import return_sparql_query_results
import os
query_string = """

 SELECT ?universityLabel ?UniversityfoundIn ?universityplaceLabel ?universitycountryLabel ?personLabel  ?birthplaceLabel  ?birthcountryLabel ?organisationLabel ?organisationlocationLabel ?orgplaceLabel ?instanceOfLabel ?organisationfoundInLabel
WHERE
{
  # Properity:P31 instance of, Q3918 -  University
  ?university wdt:P31 wd:Q3918 .
  ?university wdt:P17 wd:Q34 .
 
  # Properity:P69 educated at
  ?person wdt:P69 ?university .
  # Properity:P571 inception
  ?university wdt:P571 ?UniversityfoundIn .
  ?university wdt:P276 ?universityplace.
  ?university wdt:P17 ?universitycountry.
  

  # Properity:P19 place of birth 
  ?person wdt:P19 ?birthplace .
  # Properity:P17  country
  ?birthplace wdt:P17 ?birthcountry .
  
  # Properity:P108  employer
  ?person wdt:P108 ?organisation.
  ?organisation wdt:P276 ?orgplace.
  ?organisation wdt:P17 ?organisationlocation.
  BIND(IF(exists{?organisation wdt:P31 wd:Q3918},"university","not university") as ?instanceOf).
  ?organisation wdt:P571 ?organisationfoundIn .

 
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  }
  """

results = return_sparql_query_results(query_string)
file= open("/Users/nilu/Desktop/nilu/SP4/DIT873/Assignments/A5/results.txt","w+")
file.write("CREATE \n")

dict_of_org={}
dict_of_place={}
dict_of_person={}
i=0

for result in results["results"]["bindings"]:
  
  person = str(result['personLabel']['value'])
  birthplace = str(result['birthplaceLabel']['value'])
  birthcountry = str(result['birthcountryLabel']['value'])
  organisation = str(result['organisationLabel']['value'])
  organisationlocation = str(result['organisationlocationLabel']['value']) #country
  organisationplace = str(result['orgplaceLabel']['value'])
  instanceOf = str(result['instanceOfLabel']['value'])
  organisationfoundIn = str(result['organisationfoundInLabel']['value'])[0:4]

  university = str(result['universityLabel']['value'])
  universityfoundIn = str(result['UniversityfoundIn']['value'])[0:4]

  unicountry = str(result['universitycountryLabel']['value']) #country
  uniplace = str(result['universityplaceLabel']['value'])
  if i!=0:file.write(",\n")
  file.write("(`"+str(i)+"` :`Person` {personName:\""+person+"\"}) ,\n")
  dict_of_person[person]=i


  if birthplace  not in dict_of_place.keys():
    i=i+1 
    file.write("(`"+str(i)+"` :`Place`{placeName:\""+birthplace+"\" ,countryName:\""+birthcountry+"\"}) ,\n")
    dict_of_place[birthplace]=i


  if university not in dict_of_org.keys():
    i=i+1
    file.write("(`"+str(i)+"` :`Organisation`{organisationName:\""+university+"\", yearFounded:\""+universityfoundIn+"\"}) ,\n")
    dict_of_org[university]=i
    
    if uniplace not in dict_of_place.keys():
      i=i+1
      file.write("(`"+str(i)+"` :`Place`{placeName:\""+uniplace+"\" ,countryName:\""+unicountry+"\"}) ,\n")
      dict_of_place[uniplace]=i
    file.write("(`"+str(dict_of_org[university])+"`)-[:`locatedIn` ]->(`"+str(dict_of_place[uniplace])+"`),\n")

  if organisation not in dict_of_org.keys():
    if instanceOf=="university":
      i=i+1
      file.write("(`"+str(i)+"` :`Organisation`{organisationName:\""+organisation+"\", yearFounded:\""+organisationfoundIn+"\"}) ,\n")
      dict_of_org[organisation]=i

    else:
      i=i+1
      file.write("(`"+str(i)+"` :`Organisation`{organisationName:\" "+organisation+"\"}) ,\n")
      dict_of_org[organisation]=i

    if organisationplace  not in dict_of_place.keys():
      i=i+1
      file.write("(`"+str(i)+"` :`Place`{placeName:\""+organisationplace+"\" ,countryName:\""+organisationlocation+"\"}) ,\n")
      dict_of_place[organisationplace]=i
    file.write("(`"+str(dict_of_org[organisation])+"`)-[:`locatedIn` ]->(`"+str(dict_of_place[organisationplace])+"`),\n")
      
  i=i+1

  file.write("(`"+str(dict_of_person[person])+"`)-[:`bornIn` ]->(`"+str(dict_of_place[birthplace])+"`),\n")
  file.write("(`"+str(dict_of_person[person])+"`)-[:`employeeOf` ]->(`"+str(dict_of_org[organisation])+"`),\n")
  file.write("(`"+str(dict_of_person[person])+"`)-[:`alumnusOf` ]->(`"+str(dict_of_org[university])+"`)")
  
 


file.close()


