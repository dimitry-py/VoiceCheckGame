import time,random,os,sounddevice as sd,speech_recognition as sr
from googletrans import Translator
translator=Translator()
recognizer=sr.Recognizer()
WORDS_BANK={"easy":["кот","собака","яблоко","книга","солнце","вода","дом","друг"],"medium":["компьютер","путешествие","справедливость","приключение","университет","бабочка"],"hard":["достопримечательность","самоотверженность","предприниматель","взаимопонимание"]}
def record_and_recognize(duration=4,fs=44100):
 print("🎤 Запись пошла... Говорите!")
 r=sd.rec(int(duration*fs),samplerate=fs,channels=1,dtype='int16')
 sd.wait()
 print("⏱ Запись завершена. Обработка...")
 try:
  aud=sr.AudioData(r.tobytes(),fs,2)
  return recognizer.recognize_google(aud,language="en-US").lower().strip()
 except:return ""
def get_hint(word_en):
 if len(word_en)<=2:return "Слово слишком короткое для подсказки!"
 return f"Подсказка: Слово начинается на '{word_en[0]}', заканчивается на '{word_en[-1]}' и состоит из {len(word_en)} букв."
def get_best_score():
 if not os.path.exists("stats.txt"):return 0
 b_sc=0
 try:
  with open("stats.txt","r",encoding="utf-8") as f:
   for line in f:
    if "Очки: " in line:
     try:
      parts=line.split("Очки: ")
      score_part=parts[1].split(" ")[0]
      b_sc=max(b_sc,int(score_part))
     except:pass
 except:pass
 return b_sc
def main():
 while True:
  print("="*60)
  print("✨ Добро пожаловать в Voice Voice Lingo! ✨\nПравила: Переводите русские слова на английский своим ГОЛОСОМ.\nЗа правильный ответ ты получаешь баллы. За ошибку — теряешь жизни.\n"+"="*60)
  print("Выберите уровень сложности:\n1. Легкий 🟢 (Слова короче, 5 жизней)\n2. Средний 🟡 (Слова сложнее, 3 жизни)\n3. Сложный 🔴 (Длинные слова, 2 жизни)")
  choice=input("Введи номер (1-3): ").strip()
  if choice=="2":level,lives="medium",3
  elif choice=="3":level,lives="hard",2
  else:level,lives="easy",5
  max_lives=lives
  score,words_pool=0,WORDS_BANK[level].copy()
  random.shuffle(words_pool)
  print(f"\n🎮 Игра началась! У вас {lives} Жизней ❤️. Уровень: {level.upper()}\n")
  while lives>0 and words_pool:
   current_word_ru=words_pool.pop()
   try:
    translation=translator.translate(current_word_ru,src='ru',dest='en')
    correct_translation_en=translation.text.lower().strip()
   except:
    print("❌ Ошибка перевода слова. Пропускаем...")
    continue
   print("-"*40)
   print(f" Слово для перевода: 🤔 【 {current_word_ru.upper()} 】")
   if input("Купить подсказку за 5 баллов? (y/n): ").lower().strip()=='y':
    if score>=5:
     score-=5
     print(f"💰 Покупка успешна! Баллы: {score}\n{get_hint(correct_translation_en)}")
    else:print("❌ Недостаточно баллов для покупки подсказки!")
   print("Приготовьтесь... Запись начнется через 3 секунды.")
   for i in range(3,0,-1):
    print(f"{i}...");time.sleep(1)
   user_speech_en=record_and_recognize(duration=4)
   print(f"🤖 Вы сказали: '{user_speech_en}'")
   if user_speech_en==correct_translation_en:
    score+=10
    print(f"✅ Правильно! +10 баллов! 🎉 (Правильный перевод: {correct_translation_en})")
   else:
    lives-=1
    print(f"❌ Неверно или речь не распознана.\nПравильный ответ был: '{correct_translation_en}'\nОсталось жизней: {'❤️ '*lives}")
   print(f"📊 Текущий счет: {score} баллов.")
  print("\n"+"="*60+"\nИтоги игры:")
  status="ПОБЕДА" if lives>0 else "ПРОИГРЫШ"
  bonus=lives*15
  final_score=score+bonus
  best_score=get_best_score()
  if lives<=0:print("💀 GAME OVER! У вас закончились жизни. 💀")
  else:
   print("🏆 ПОЗДРАВЛЯЕМ! Вы прошли все слова на этом уровне! 🏆")
   print(f"🎁 Бонус за сохраненные жизни ({lives} шт.): +{bonus} баллов!")
  print(f" Финальный результат: {final_score} баллов.")
  if final_score>best_score and best_score>0:print(f"🔥 НОВЫЙ РЕКОРД! Вы побили прошлый лучший результат в {best_score} баллов! 🎉")
  elif best_score>0:print(f"📈 Прошлый лучший рекорд: {best_score} баллов. Есть к чему стремиться!")
  print("="*60)
  with open("stats.txt","a",encoding="utf-8") as f:
   f.write(f"Дата: {time.strftime('%Y-%m-%d %H:%M:%S')} | Уровень: {level.upper()} | Итог: {status} | Очки: {final_score} (Бонус: {bonus}) | Оставшиеся жизни: {lives}/{max_lives}\n")
  print("💾 Результаты игры успешно записаны в файл stats.txt!")
  if input("\n🔄 Хотите сыграть еще раз? (y/n): ").lower().strip()!='y':
   print("👋 Спасибо за игру! До встречи!");break
if __name__=="__main__":main()
