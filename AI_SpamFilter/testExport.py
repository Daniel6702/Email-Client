import json
import re

# Import relevant variables from file
with open('AI_SpamFilter\\info.json', 'r') as file:
   info = json.load(file)

p_spam = info[0]
p_ham = info[1]
parameters_spam = info[2]
parameters_ham = info[3]

#------------------------
# Classifying function
def classify(message):
   message = re.sub('\W', ' ', message)
   message = message.lower().split()

   p_spam_given_message = p_spam
   p_ham_given_message = p_ham

   for word in message:
      if word in parameters_spam:
         p_spam_given_message *= parameters_spam[word]

      if word in parameters_ham: 
         p_ham_given_message *= parameters_ham[word]

   if p_ham_given_message >= p_spam_given_message:
      return 'ham'
   elif p_ham_given_message < p_spam_given_message:
      return 'spam'
   

print(classify('free money big money prize'))