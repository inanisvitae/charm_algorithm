import praw
import re
import nltk
# nltk.download('punkt')
# nltk.download('stopword')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# limit = input('Enter number of posts to scrape')

def scrape_data():
    reddit = praw.Reddit(client_id="XdEnLPkLpMETVw",  # my client id
                         client_secret="YLeYBcQN6NL9ZH7CipCVmqisfZu8aw",  # your client secret
                         user_agent="Reddit:Data_Scraper:0.1 (by /u/Mysterious_Middle690)",  # user agent name
                         username="mysterious_middle690",  # your reddit username
                         password="Mysterious_Middle690")  # your reddit password

    sub = ['Wallstreetbets']
    corpus = []
    for s in sub:
        subreddit = reddit.subreddit(s)
        for submission in subreddit.new(limit=100):
            # Fetches the posts from DDs
            try:
                # if submission.link_flair_template_id == '5692ce02-b860-11e5-b542-0edc7016bbd3':
                corpus.append(submission.title)
                corpus.append(submission.selftext)
                for comment in submission.comments.replace_more():
                    corpus.append(comment.body)
            except:
                print('Error')
    return corpus


def clean_data(corpus):
    for i in range(len(corpus)):
        curr_text = corpus[i]

        # Remove urls
        curr_text = re.sub(r'http\S+', '', curr_text, flags=re.MULTILINE)

        # lowercase
        curr_text = curr_text.lower()

        # Remove numbers
        curr_text = re.sub(r'\d+', '', curr_text)

        # Remove punctuation
        curr_text = re.sub(r'[^\w\s]', '', curr_text)

        # Remove \n, \t
        curr_text = re.sub(r'\s+', ' ', curr_text)

        # Remove whitespaces
        curr_text = curr_text.strip()

        curr_text = word_tokenize(curr_text)

        curr_text = [word for word in curr_text if not word in stopwords.words()]

        corpus[i] = curr_text
    return corpus

def flip_data(corpus):
    # Turns it into form for charm algorithm and write to text file
    corpus_dict = {}
    count = 0
    for i in corpus:
        corpus_dict[count] = list(i)
        count += 1
    corpus_word_dict = {}
    for i in range(len(corpus)):
        for word in corpus_dict[i]:
            if word in corpus_word_dict:
                if i not in corpus_word_dict[word]:
                    corpus_word_dict[word].append(i)
            else:
                corpus_word_dict[word] = [i]
    items = corpus_word_dict.items()
    items_lst = []
    for key, value in items:
        items_lst.append([key, value])
    items_lst.sort(key=lambda x:len(x[1]), reverse=True)
    # Writes to file
    with open('corpus_result.txt', 'w') as f:
        for i in items_lst:
            f.write(i[0] + '\t' + ','.join(map(lambda x:str(x), i[1])) + '\n')

flip_data(clean_data(scrape_data()))
