# File: api_test.sh

# Testing the "App_Working" endpoint
curl -X 'GET' http://127.0.0.1:8000/App_Working

#Testing the get_question endpoint
curl -X 'GET' \
  'http://127.0.0.1:8000/questions?use=Test%20de%20positionnement&subjects=Syst%C3%A8mes%20distribu%C3%A9s&number_of_question=5' \
  -H 'accept: application/json'


#Testing the "Create Question" end point
curl -X 'POST' \
  'http://127.0.0.1:8000/Post_Question_Only_by_Admin?question=What%20is%20the%20vlaue%20of%20PI&subjects=maths&use=maths&correct=A&responseA=3.14&responseB=3.02&responseC=3.2' \
  -H 'accept: application/json' \
  -u 'admin:4dm1N'
    

#Testing the "login" endpoint
curl -X 'POST' \
  'http://127.0.0.1:8000/User'\''s_Login' \
  -H 'accept: application/json' \
  -u 'clementine:mandarine'


