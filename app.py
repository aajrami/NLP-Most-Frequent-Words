# @uthor Ahmed Alajrami

from flask import Flask, request
from model import Model
from flask_jsonpify import jsonify

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
m = Model()
index, freq_wrds = m.build() # build the model and get the index the frequency of words

@app.route('/')
def main_form():
    # form to select the number of most common words to show
    return '<div style="text-align:center;"><form action="submit" method="post"> <h3>Please select the number of most common words </h3><select name="words_no" style="padding:2px; 10px"><option value="5">5</option><option value="10">10</option><option value="15">15</option><option value="20">20</option><option value="25">25</option><option value="30">30</option></select> <input type="submit" value="Submit" style="padding:4px 8px;"></form></div>'

@app.route('/submit', methods=['POST'])
def submit_textarea():
    result = {}
    words_no = request.form["words_no"]
    for word, counts in freq_wrds.most_common(int(words_no)+1): # iterate over the most common words
        if word =="":   # ignore empty word
            continue
        result[word] = index[word] # get a sub index for the most common words from the whole index
    return jsonify(result) # display the nested dictionary as a JSON

if __name__ == '__main__':
    app.run(debug=True)
