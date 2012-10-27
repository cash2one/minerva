from calais import Calais

API_KEY = "k6s6cewwwc5zkemjqpw7yhru"
calais = Calais(API_KEY, submitter="python-calais demo")
result = calais.analyze("michelle obama")

print result.print_summary()
print result.print_topics()
print result.print_relations()

