# secFilingSummarizer

This is a practice on fetching public companies' annual reports (10-K form) via SEC Edgar API and make summarization according to different topics. 
The data pipeline is shown below (LLM module is not implemented yet):

<img width="640" alt="datapipeline" src="https://github.com/zhen-qian101/secFilingSummarizer/assets/90771509/a0fddb4b-bd90-472d-9fc9-18babba02a09">


**How to run the prototype?**

**Step 1**: create an environment and install dependencies with the command below:

pip install -r requirements.txt

**Step 2**: Switch to the flask folder and run the app with the command below:

flask --app app run --debug

**Step 3**: Enter a ticker and click go. It will make summarization with respect to each question.

<img width="320" alt="prototype" src="https://github.com/zhen-qian101/secFilingSummarizer/assets/90771509/921703a6-f702-4e06-8986-3016793c3682">
