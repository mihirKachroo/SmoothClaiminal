text="Lionel Messi has pleaded the board of Barcelona for over two seasons to sign Neymar from Paris Saint-Germain since the former Santos winger left the Camp Nou for a world record fee to France. His departure from Barca was completely unexpected and uncalled for as he performing at an exceptional rate under the guidance of Luis Enrique, however, his sudden exit and the fashion in which he left the club were not taken lightly been many. The skillful winger has not had the best start to life in Paris as he has struggled with injuries all season long and has not had a major impact as expected. Neymar has won three Ligue 1 title medals, however, the Brazilian certainly did not sign just to win the league as the main objective was to win the Champions League. Neymar has stirred a lot of chaos as well, as the Brazilian at one point, was desperate to come back to the Camp Nou to join forces with Lionel Messi and Luis Suarez once again to win the Champions League. However, this season after successfully turning around the tie against Borussia Dortmund in the round of 16 it seems like the Parisian club is the favourites to make it to the final and win their first-ever Champions League trophy. The 28-year-old winger’s contract is set to expire in 2022 with PSG, however, given the club’s recent performance and the guidance by Tuchel, Neymar has reportedly considered signing a new contract with the French club after his current contract expires, according to the Express."
print(text)
print("------------------------------------------")
from gensim.summarization import summarize
from gensim.summarization import keywords
# summarizes the text in 90 words, can just change this word_count
text_summary = summarize(text, word_count=90)
print(sum_text)
# Keywords
text_keywords = keywords(text)
print(text_keywords)


# google cloud probably is still better since it has sentiment analysis and stuff