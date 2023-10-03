import requests
import numpy as np
from bs4 import BeautifulSoup
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from nltk.tokenize import sent_tokenize

headers = {
  "User-Agent": "s3888611@student.rmit.edu.au"#, # remaining fields are optional
   # "Accept-Encoding": "gzip, deflate",
   # "Host": "data.sec.gov"
}

def build_ticker_cik_dict():

    ticker_url = "https://www.sec.gov/include/ticker.txt"
    ticker_cik = requests.get(ticker_url, headers=headers).content.decode("utf-8")
    ticker_cik_list = ticker_cik.split("\n")
    ticker_cik_list = [t.split("\t") for t in ticker_cik_list]
    ticker_cik_dict = {}
    for t in ticker_cik_list:
        ticker_cik_dict[t[0]] = t[1]

    return ticker_cik_dict

def fetch_latest_filing(ticker, form_type = "10-K"):

    ticker_cik_dict = build_ticker_cik_dict()

    ticker = ticker.lower()
    cik = ticker_cik_dict[ticker]

    filings_url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
    company_filings = requests.get(filings_url, headers=headers).json()
    recent_forms = np.array(company_filings["filings"]["recent"]["form"])
    index_of_latest_form = np.where(recent_forms == form_type)[0][0]

    file_num = company_filings["filings"]["recent"]["accessionNumber"][index_of_latest_form]
    accession_num = file_num.replace("-", '')

    form_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_num}/{file_num}.txt"
    form_response = requests.get(form_url, headers=headers)

    soup = BeautifulSoup(form_response.content, "lxml")

    all_docs = soup.find_all("document")

    for doc in all_docs:
        doc_type = doc.type.find(string=True, recursive=False).strip()
        if doc_type == form_type:
            form_text = doc.get_text(" ")

    sentences = sent_tokenize(form_text)
    sentences = [s for s in sentences if len(s)<2000]

    form_text = " ".join(sentences)

    return form_text

def extract_tenK_item7(tenK_text):

    matches = re.compile(r'(item\s(7[\.\s]|8[\.\s])|discussion\sand\sanalysis\sof\s(consolidated\sfinancial|financial)\scondition|(consolidated\sfinancial|financial)\sstatements\sand\ssupplementary\sdata)', re.IGNORECASE)
    item7_8 = [(match.group(), match.start()) for match in matches.finditer(tenK_text)]

    item7_8_concat = []
    for i in range(len(item7_8)-1):
        new_tup = (item7_8[i][0].lower() + item7_8[i+1][0].lower(), item7_8[i][1])
        item7_8_concat.append(new_tup)

    matches_item7 = re.compile(r'(item\s7\.discussion\s[a-z]*)')
    matches_item8 = re.compile(r'(item\s8\.(consolidated\sfinancial|financial)\s[a-z]*)')

    start_pos = []
    end_pos = []

    for tup in item7_8_concat:
        if re.match(matches_item7, tup[0]):
            start_pos.append(tup[1])
        if re.match(matches_item8, tup[0]):
            end_pos.append(tup[1])

    tenK_item7 = tenK_text[start_pos[1]:end_pos[1]]

    tenK_item7 = tenK_item7.strip() # Remove start/end white space
    tenK_item7 = tenK_item7.replace('\n', ' ') # Replace \n with space
    tenK_item7 = tenK_item7.replace('\r', '') # \r => space
    tenK_item7 = tenK_item7.replace(' ', ' ') # " " => space
    tenK_item7 = tenK_item7.replace(' ', ' ') # " " => space
    while '  ' in tenK_item7:
        tenK_item7 = tenK_item7.replace('  ', ' ')

    return tenK_item7

def text_summarization(text, sentence_count=5):

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    stemmer = Stemmer("english")

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words("english")

    summarized_sentences = [str(s) for s in summarizer(parser.document, sentence_count)]

    return summarized_sentences

class user_query:

    def __init__(self, query_text):
        self.query_text = query_text
        self.supporting_evidences = []

def initiate_queries():

    q1 = user_query("Do the company's products and services hold growth potential in demand?")
    q2 = user_query("Is there a plan for lauching new products or services?")
    q3 = user_query("How is the company's Research and Development spending compared to competitors? Does the R&D lead to profit increase?")

    return q1, q2, q3

def retrieve_evidences(text):

    q1, q2, q3 = initiate_queries()
    sentences = sent_tokenize(text)

    evidence_for_q1 = [s for s in sentences if ('growth' in s.lower()) or ('demand' in s.lower())]
    evidence_for_q1 = " ".join(evidence_for_q1)
    evidence_for_q2 = [s for s in sentences if ('new product' in s.lower()) or ('new services' in s.lower())]
    evidence_for_q2 = " ".join(evidence_for_q2)
    evidence_for_q3 = [s for s in sentences if ('research' in s.lower()) or ('develop' in s.lower())]
    evidence_for_q3 = " ".join(evidence_for_q3)

    q1.supporting_evidences += text_summarization(evidence_for_q1)
    q2.supporting_evidences += text_summarization(evidence_for_q2)
    q3.supporting_evidences += text_summarization(evidence_for_q3)

    evi = {
        q1.query_text:q1.supporting_evidences,
        q2.query_text:q2.supporting_evidences,
        q3.query_text:q3.supporting_evidences
        }


    return evi    

# def ans_summarization(text):

#     sentences = sent_tokenize(text)
#     sentences = [s for s in sentences if len(s)<2000]

#     a1_list = [s for s in sentences if ('product' in s.lower()) or ('service' in s.lower())]
#     a1 = " ".join(a1_list)

#     a2_list = [s for s in sentences if ('sale' in s.lower()) or ('revenue' in s.lower())]
#     a2 = " ".join(a2_list)

#     a3_list = [s for s in sentences if ('research' in s.lower()) or ('develop' in s.lower())]
#     a3 = " ".join(a3_list)

#     a1_sum = text_summarization(a1)
#     a2_sum = text_summarization(a2)
#     a3_sum = text_summarization(a3)

#     ans = {"products and services":a1_sum, "sales and revenues":a2_sum, "research and development":a3_sum}

#     return ans




   








