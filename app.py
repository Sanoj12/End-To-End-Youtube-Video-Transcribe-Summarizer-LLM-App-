import os
import streamlit as st

from dotenv import load_dotenv


load_dotenv()

import google.generativeai as genai

from youtube_transcript_api import YoutubeTranscriptApi



genai.config(api_key=os.getenv('GOOGLE_API_KEY'))


prompt ="""you are youtube video summarizer .you will be taking the transcript text
       and summarizing the entire video and providing the important information
"""



def extract_transcript_details(youtube_video_url):
        try: 
                video_id  = youtube_video_url.split("=")[1]
                transcript_text = YoutubeTranscriptApi.get_transcript(video_id)
                

                transcript = ""
                for i in transcript_text:
                        transcript += " " + i["text"]
                
                return transcript

        except Exception as e:
                raise e
              




def generate_gemini_content(transcript_text,prompt):
        model = genai.GenerativeModel("gemini-pro")

        response = model.generate_content(prompt + transcript_text)

        return response.text






##streamlit

st.title("Youtube Transcript to detailed")

youtube_link = st.text_input("enter youtube video link")

if youtube_link:
        video_id  = youtube_link.split("=")[1]

        ##display thumbnail video image

        st.image("http://img.youtube.com/vi/{video_id}/0.jpg" ,use_column_width = True)

        
        if st.button("get details"):
           
           transcript_text = extract_transcript_details(youtube_link)

           if transcript_text:
                 summary =  generate_gemini_content(transcript_text,prompt)
                 st.markdown("detailed notes:")
                 st.write(summary)
                  


               




        
