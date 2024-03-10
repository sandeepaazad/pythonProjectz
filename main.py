import pandas as pd
import requests
#here using bs4 for pulling the data out of html and xlsx file...it help to navigate ,search  and modify the file.
from bs4 import BeautifulSoup
#os help to interact with the operating sysytem.
import os
#firstly we are extracting the url form the given input file .There after we are proceeding further.
def extract_text_from_url(url):
    #sending a request to get the URL
    response=requests.get(url)
    #if the response is successful it parser(resolve it into varios sub component) the URL received.
    #here the response status code indicate the stauts of file it is returned by server when client request for it.
    if response.status_code==200:
        soup=BeautifulSoup(response.content,'html.parser')
        title=soup.find('title').get_text()
        text_data=[]
        #for this it searches all the paragraph  and for each paragraph found it appends it to text_data.
        for paragraph in soup.find_all('p'):
            text_data.append(paragraph.get_text())
        return title,'\n'.join(text_data)
    #if response status code is not 200 it print an error message indicating the faliure to retrive the webpage.
    else:
        print("failed to retrive the web page ,Code:",response.status_code)
        return None,None
#path is specified and contets are read through  panda dataframe.
input_file = "/Users/sandeepkumaraazad/Downloads/Input.xlsx"
df = pd.read_excel(input_file)
#this path check if it exist and if do not it creat a directory using os.makedirs.
output_dir="extracted_articles"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
#in this loop it iterate over each data frame.It retrive each url_id and url if successful it xtract the title and article from it if not print a failure message.
for index,row in df.iterrows():
    url_id=row['URL_ID']
    url=row['URL']
    title,article_text=extract_text_from_url(url)
    if title and article_text:
        filename=os.path.join(output_dir,f"{url_id}.txt")
        with open(filename,'w',encoding='utf-8') as file:
            file.write(title+'\n\n')
            file.write(article_text)
        print(f"Article{url_id} extracted successfully.")
    else:
        print(f"failed to extact article{url_id}.")
print ("All articles extracted and saved")
