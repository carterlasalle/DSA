import calendar as cal
import random
import time

def random_date():
  year = random.randint(1582,2582)
  month = random.randint(1,12)
  day = random.randint(1,31)

  # Feb short month but bEST month
  if month == 2:
    if cal.isleap(year):
      day = min(day,29) 
    else:
      day = min(day,28)

  # April, June, Sept, Nov
  elif month in [4,6,9,11]:
    day = min(day,30)

  # equivalent new Datetime(....)
  return cal.datetime.datetime(year,month,day)

  
def ask_question_Random():
  test_date = random_date()
  print(f"What day of the week was {test_date.strftime('%m/%d/%Y')} ?")

  # record start time
  t_start = time.time()
  user_response = input("type < mo, tu, we, th, fr, sa, su >")
  t_end = time.time()

  response_time = t_end - t_start

  user_response = user_response.lower() # "Mo".lower()
  
  correct = test_date.weekday() #0= monday, 1=tuesday
  correct_day_code = ["mo","tu","we","th","fr","sa","su"][correct]     
  is_user_correct = (user_response == correct_day_code)

  result = { 'date': test_date,
           'is_correct': is_user_correct,
           'time': response_time,
           'correct_answer': correct_day_code,
           'user_answer': user_response }

  
  return result

def start_quiz():
  quiz_results = []
  for i in range(1):
    quiz_results.append(ask_question_Random())
  return quiz_results

  
quiz_results = start_quiz();

total_correct = 0
total_time = 0
for date in quiz_results:
    print(f"{date['date'].strftime('%m/%d/%Y')} - {'CORRECT' if date['is_correct'] else 'INCORRECT, Correct: ' + date['correct_answer'].upper() +  ', You Said: ' + date['user_answer'].upper()} - {date['time']:.3f} seconds")
    if date['is_correct']:
        total_correct += 1
    total_time += date['time']

total_questions = len(quiz_results)
print("-----------------------------------")
print(f"TOTAL: {(total_correct/total_questions) * 100:.2f}%, Average Time: {total_time/total_questions:.2f} avg. seconds")




    #print(f"Total: {for da} ")
  # print(date['date'].strftime('%m/%d/%Y'))
  # print(date['is_correct'])
  # if date['is_correct'] == False:
  #   print("")




# prompt the user with a date
# get the response
# user_response = ask_question()

# if user_response['is_correct']:
#   print(f"Correct! It took you {user_response['time']} seconds")
# else:
#   print(f"Incorrect! You said {user_response['user_answer']} the correct answer was {user_response['correct_answer']}")



# check the response
# report back to them the answer



# total = 0
# for result in quiz_results:
#   total += result['time']
#   print(f"Average time = {total/len(quiz_results)}")

