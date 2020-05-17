import os
from flask import Flask, request, abort, jsonify, Response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def afterResponse(response) :
    response.headers.add("Access-Control-Allow-Header", '*')
    response.headers.add('Access-Control-Allow-Methods', 'PUT,DELETE,POST,GET')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/categories")
  def getAllCategories():
    categories = Category.query.all()
    formattedCategories = [category.format()['type'] for category in categories ]
    print(formattedCategories)
    return jsonify(
        { 
        'success' : True,
        'categories': formattedCategories
        }
      )


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route("/questions")
  def getQuestions():
    page = request.args.get('page', 2 ,int)
    start = (page-1)*QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    print(page)
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
    categories = Category.query.all()
    print(categories)
    formatted_categories = [category.format()['type'] for category in categories ]
    return jsonify(
      {
        'success' : True,
        'questions' : formatted_questions[start:end],
        'total_questions' : len(formatted_questions),
        'categories' : formatted_categories
      }
    )


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:id>", methods = ['DELETE'])
  def deleteQuestion(id):
    question = Question.query.get(id)
    if question is None :
      abort(422)
    question.delete()
    return jsonify (
      {
        'success': True
      }
    )


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route("/questions", methods = ['POST'])
  def submitQuestion():
    req = request.json
    question = Question(question = req['question'],answer = req['answer'], category = req['category'], difficulty = req['difficulty'])
    question.insert()
    return jsonify( {'success': True}), 201

    

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route("/questions/search", methods = ['POST'])
  def searchQuestion():
    search_term = request.json['searchTerm']
    search_phrase = '%{}%'.format(search_term)
    print(search_phrase)
    questions = Question.query.filter(Question.question.like(search_phrase)).all()
    formatted_questions = [question.format() for question in questions]
    return jsonify({
      'questions': formatted_questions,
      'totalQuestions': len(formatted_questions)
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route("/categories/<int:category_id>/questions")
  def getQuestionsForCategory(category_id):
    print(category_id)

    category = Category.query.get(category_id+1)
    questions = Question.query.filter_by(category=category.id).all()
    print(category)
    print(questions)
    formatted_questions = [question.format() for question in questions]
    return jsonify({
      'questions' : formatted_questions,
      'totalQuestions' : len(formatted_questions),
      'currentCategory': category.type

    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route("/quizzes", methods=['POST'])
  def playQuiz():
    previous_questions = request.json['previous_questions']
    quiz_category = request.json['quiz_category']
    quiz_category_id = int(quiz_category['id']) + 1
    print(quiz_category)
    print(quiz_category_id)
    questions = Question.query.filter_by(category = quiz_category_id).all()
    formatted_questions = [question.format() for question in questions]
    response_question = None
    for question in formatted_questions:
      if question['id'] not in previous_questions:
        response_question = question
        break
      else:
        pass
    return jsonify({
        'question' : response_question
    })
  
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def notFound(error):
    return jsonify({
      'success': False,
      'error' : '404',
      'message' : 'Not Found'
    }), 404
    
  @app.errorhandler(422)
  def nonProcessable(error):
    return jsonify({
      'success': False,
      'error' : '422',
      'message' : 'unprocessable'
    }), 422

  return app

    