from logic import *

#Defining all the conditions

Rain = Symbol("rain")
HeavyTraffic = Symbol("heavy traffic")
EarlyMeeting = Symbol("early meeting")
Strike = Symbol("strike")
WFH = Symbol("work from home")
Drive = Symbol("drive")
PublicTransport = Symbol("take the public transport")
Appointment = Symbol("doctor's appointment")
RoadConstruction = Symbol("road construction")

#Defining the knowledge base

base_rules = And(
                Implication(Or(Rain, EarlyMeeting),WFH),
                Implication(And(Not(Rain),Not(HeavyTraffic)),Drive),
                Implication(And(Not(Strike),Not(Rain)),PublicTransport),
)

print(base_rules.formula())

#Adding elements to our knowledge based on the actual situation

situation1 = And(
                Rain,
                HeavyTraffic
)

situation1text = "It’s raining, and there’s heavy traffic."

situation2 = And(
                Strike,
                Not(Rain)
)

situation2text = "There’s a public transport strike, and it’s not raining."

situation3 = And(
                Not(Strike),
                Not(Rain),
                Not(HeavyTraffic)
)

situation3text = "There’s no rain, traffic is light, and there’s no strike."

situations = [situation1, situation2, situation3]

situationstext = [situation1text, situation2text, situation3text]

#Making a new knowledge out of it

def knowledge(base_rules, situation):
    return And(base_rules, situation)

#Function to refactor all the queries and print the results nicely

def result(rules, situation_number, query):
    print(situationstext[situation_number-1]+" You should"+(not model_check(knowledge(rules, situations[situation_number-1]), query))*"n't"+" "+query.__repr__()+".")
    return

result(base_rules,1,WFH)
result(base_rules,1,Drive)
result(base_rules,2,PublicTransport)
result(base_rules,3,Drive)
result(base_rules,3,PublicTransport)

#Adding rules to the base ones

new_rules = And(
                Implication(Or(Rain, EarlyMeeting),WFH),
                Implication(Or(Appointment, And(Not(Rain),Not(HeavyTraffic),Not(RoadConstruction))),Drive),
                Implication(And(Not(Strike),Not(Rain)),PublicTransport)
)

#Results should be unchanged as long as situations remain the same

result(new_rules,1,WFH)
result(new_rules,1,Drive)
result(new_rules,2,PublicTransport)
result(new_rules,3,Drive)               #Changes for this one because the model assumes there is road construction by default
result(new_rules,3,PublicTransport)

#Let's see if our new rules work

situations.append(Appointment)
situationstext.append("You have an appointment in the afternoon.")
situations.append(And(situation3, RoadConstruction))
situationstext.append(situation3text+" but there is road construction.")

result(new_rules,4,Drive)
result(new_rules,5,Drive)
result(new_rules,5,PublicTransport)