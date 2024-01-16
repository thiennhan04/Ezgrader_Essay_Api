from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import google.generativeai as palm

app = FastAPI()

class GraderInput(BaseModel):
    question: str
    correct_answer: str
    student_answer: str

class GraderOutput(BaseModel):
    result: str

API_KEY = 'AIzaSyBFy5yH5ajJN1hLeBBkwnkNvu1pacJVWdg'
palm.configure(api_key=API_KEY)
model_id = 'models/text-bison-001'

@app.post("/grade", response_model=GraderOutput)
async def grade_assignment(input_data: GraderInput):
    prompt = (
        'From the question: ' + input_data.question +
        'Correct answer: ' + input_data.correct_answer +
        'Student answer: ' + input_data.student_answer +
        ('What percentage of students answered correctly?give me number of percentage')
    )

    completion = palm.generate_text(
        model=model_id,
        prompt=prompt,
        temperature=0.7,
        max_output_tokens=20,
        candidate_count=5
    )

    return GraderOutput(result=completion.result)
