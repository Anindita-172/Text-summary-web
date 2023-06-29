import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """Lawrence Mark Sanger (/sæŋər/;[1] born July 16, 1968) is an American Internet project developer and philosopher who co-founded the online encyclopedia Wikipedia along with Jimmy Wales. Sanger coined the name 'Wikipedia', and wrote much of Wikipedia's original governing policy, including "Neutral point of view" and "Ignore all rules". Sanger has worked on other online projects, including Nupedia, Encyclopedia of Earth, Citizendium, WatchKnowLearn, Reading Bear, Infobitt, Everipedia, the Knowledge Standards Foundation and the encyclosphere. He also advised blockchain company Phunware and the nonprofit online American political encyclopedia Ballotpedia.[2]

While studying at college, Sanger developed an interest in using the Internet for educational purposes and joined the online encyclopedia Nupedia as editor-in-chief in 2000. Disappointed with the slow progress of Nupedia, Sanger proposed using a wiki to solicit and receive articles to put through Nupedia's peer-review process; this change led to the development and launch of Wikipedia in 2001. Sanger served as Wikipedia's community leader and was the only editorial employee of Wikipedia in its early stages but was laid off and left the project in 2002. Sanger's status as a co-founder of Wikipedia has been questioned by fellow co-founder Jimmy Wales but is generally accepted.

Since Sanger's departure from Wikipedia, he has been critical of the project, describing it in 2007 as being "broken beyond repair".[3] He has argued that despite its merits, Wikipedia lacks credibility and accuracy due to a lack of respect for expertise and authority. Since 2020, he has criticized Wikipedia for what he perceives as a left-wing and liberal ideological bias in its articles.[4][5][6]

In 2006, he founded Citizendium to compete with Wikipedia. In 2010, he stepped down as editor-in-chief. In 2020, he left Citizendium entirely. In 2017, he joined Everipedia as chief information officer (CTO). He resigned in 2019, to establish the Knowledge Standards Foundation and the encyclosphere. Sanger currently serves as the President and Executive Director of the Knowledge Standards Foundation."""


def summarizer(rawdocs):
    stopword = list(STOP_WORDS)

    nlp = spacy.load('en_core_web_sm')
    #print(nlp)
    doc = nlp(rawdocs)
    #print(doc)
    tokens = [token.text for token in doc]
    #print(tokens)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopword and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text]+=1
    #print(word_freq)


    max_freq = max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    #print(word_freq)

    sent_tokens = [sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]
    #print(sent_scores)

    select_len =int(len(sent_tokens)*0.3)
    #print(select_len)

    summary = nlargest(select_len , sent_scores , key= sent_scores.get)
    #print(summary)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    # print(summary)
    # print(text)
    # print("Length of original text", len(text.split( ' ')))
    # print("Length of summary text", len(summary.split( ' ')))
    
    return summary, doc ,len(rawdocs.split(' ')),len(summary.split(' '))
