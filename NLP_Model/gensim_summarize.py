# -*- coding: utf-8 -*-

text="August 21, 2020 Mr. Abner Kenny Northern Insurance P.O. Box 337 Milwaukee, WI Date of incident: July 12, 2020 Dear Mr. Kenny As you know, I was involved in a collision with a van owned by your insured on Chestnut St. in Waukesha, WI. I was waiting at a stop sign, when the Jenkins Hardware van rear-ended me. I was not injured, but my car suffered a fair amount of damage, which, despite repeated phone calls, Northern Insurance has so far refused to pay for. The Jenkins driver was obviously negligent. He rear-ended someone waiting at a stop sign. It is an open-and-shut case. As a result of this incident, my trunk was caved in. I have a small Honda, and small cars don’t tend to fare very well when they are hit by commercial vans. I brought it to my usual mechanic, who recommended that I go to Waukesha Body Shop, where they gave me an estimate for $4,600 for a full repair. I have attached another copy of the estimate, although I have sent it to you twice before. You also have pictures of the damage. My car is only 2 years old, and is worth far more than that. I understand that your estimator valued the repair costs at $4,000. That is not that far off. I don’t understand why we haven’t been able to agree on a repair price. Taking into account your insured’s absolute liability and my damages in this case, I demand $4,600.00 to settle this case. This is not a complex claim. If I do not hear from you in one week, I will call the Wisconsin Department of Insurance to file a complaint against you. Very truly yours, Fred Smith"
print(text)
print("------------------------------------------")
from gensim.summarization import summarize
from gensim.summarization import keywords
# summarizes the text in 90 words, can just change this word_count
text_summary = summarize(text, word_count=90)
print(text_summary)
# Keywords
text_keywords = keywords(text)
print(text_keywords)

