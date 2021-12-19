# DSentimentModel2

The default sentiment model is a fast regex sentiment detection model without using machine learning models. The sentiment scores are determined by summing the log of weighted positive words + emoji and negative words + emoji.

This approach could comparing the sentiment in a fixed scale and the scores would not be affected by the length of sentences.