from flask import Flask, render_template, request, redirect
from flask_cors import CORS, cross_origin
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

app = Flask(__name__)
cors = CORS(app)

s = ""


@app.route('/', methods=['GET', 'POST'])
def index():
    print("loaded...")
    print(request.method)
    if request.method == "POST":
        global s
        s = ""
        text = request.form.get("txt_input")
        if len(text) < 10:
            return "StringERR"
        # Tokenizing the text
        stopWords = set(stopwords.words("english"))
        words = word_tokenize(text)

        freqTable = dict()
        for word in words:
            word = word.lower()
            if word in stopWords:
                continue
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

         # Creating a dictionary to keep the score of each sentence
        sentences = sent_tokenize(text)
        sentenceValue = dict()
        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq
        sumValues = 0
        for sentence in sentenceValue:
            sumValues += sentenceValue[sentence]

        # Average value of a sentence from the original text
        average = int(sumValues / len(sentenceValue))

        # Storing sentences into our summary.
        summary = ''
        for sentence in sentences:
            if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                summary += " " + sentence
        if len(summary) < 3:
            return "ConverstionERR"

        return summary

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
