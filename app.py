from flask import Flask,render_template,request
from text_summarizer import summarizer

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze',methods=['GET','POST'])
def analyze():
    if request.method=='POST':
        rawtext = request.form['rawtext']
        summary, doc, len_orig,len_summary = summarizer(rawtext)

    return render_template('summary.html', summary=summary, doc=rawtext ,len_orig=len_orig,len_summary=len_summary )

if __name__ == "__main__":
    app.run(debug=True)