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

  
def ask_question():
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

# prompt the user with a date
# get the response
user_response = ask_question()

if user_response['is_correct']:
  print(f"Correct! It took you {user_response['time']} seconds")
else:
  print(f"Incorrect! You said {user_response['user_answer']} the correct answer was {user_response['correct_answer']}")



# check the response
# report back to them the answer