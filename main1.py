from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List, Optional
from pydantic import BaseModel
import pandas as pd

api=FastAPI(title="Shoe Company Questionary",description="Satish Goli",version=0.1)
security = HTTPBasic()

#Checking whether the API is working or not
@api.get("/App_Working")
def app_functioning():
    return {"message":"FASTAPI is working"}

#Reading the CSV file using pandas DataFrame
question_df = pd.read_csv("questions.csv")

#get function to get the questions based on input
@api.get("/questions")
def get_questions(use:str,subjects:str,number_of_question:int):
    questions=question_df[(question_df['use']==use) & (question_df['subjects']==subjects)]
    shuff_ques=questions.sample(frac=1)
    print(shuff_ques.head(number_of_question))
    return shuff_ques.to_json(orient="records")
   

#Thread to post a question
@api.post("/Post_Question_Only_by_Admin")
def create_question(
    question: str,
    subjects: str,
    use: str,
    correct: str,
    responseA: str,
    responseB: str,
    responseC: str,
    responseD: Optional[str] = None,
    remark: Optional[str] = None,
    credentials: HTTPBasicCredentials = Depends(security)
):
    # Authenticate the user using credentials
    admin_credentials = {
         "admin":"4dm1N",
    }

    if credentials.username not in admin_credentials or credentials.password != admin_credentials[credentials.username]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Access the global variable 'question_df'
    global question_df

    # Create a new question dictionary
    new_question = {
        "question": question,
        "subjects": subjects,
        "correct": correct,
        "use": use,
        "responseA": responseA,
        "responseB": responseB,
        "responseC": responseC,
        "responseD": responseD,
        "remark": remark
    }

    # Append the new question to the DataFrame
    question_df = question_df.append(new_question, ignore_index=True)

    # Save the updated DataFrame back to the CSV file
    question_df.to_csv("questions.csv", index=False)

    # Return a success message
    return {"message": "Question created successfully"}


user_credentials={
        "alice":"wonderland",
        "bob":"builder",
        "clementine":"mandarine",
        "admin":"4dm1N"
    }


@api.post("/User's_Login")
def login(credentials: HTTPBasicCredentials=Depends(security)):
    if credentials.username not in user_credentials or credentials.password != user_credentials[credentials.username]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials",headers={"WWW-Authenticate":"Basic"})
    return{"Message":"Login successful",credentials.username:credentials.password}
