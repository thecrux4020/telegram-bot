import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
import json
import logging

DYNAMODB_TABLE_NAME = "quizzes_questions"


def setup_logging():
    """ Basic logging setup """
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    return logging

def load_questions():
    with open("questions.json", "r") as f:
        questions = json.loads(f.read())
    return questions


def check_limitations(question):

    if not "explanation" in question:
        raise KeyError(f"explanation key not found in question id: {question['question_id']}")
    elif not "question" in question:
        raise KeyError(f"question key not found in question id: {question['question_id']}")
    elif not "options" in question:
        raise KeyError(f"options key not found in question id: {question['question_id']}")
    elif not "correct_option" in question:
        raise KeyError(f"correct_option key not found in question id: {question['question_id']}")

    if len(question["explanation"]) > 200:
        raise ValueError("explanation value is greater than 200 chars")
    
    if len(question["question"]) > 255:
        raise ValueError("question value is greater than 255 chars")
    
    if len(question["options"]) > 10:
        raise ValueError("options array is greater than 10")

    for option in question["options"]:
        if len(option) > 100:
            raise ValueError(f"option: {option} is grater than 100 chars")

def serialize(question, type_serializer = TypeSerializer()):
    question = {k: type_serializer.serialize(v) for k,v in question.items()}
    return question

def upload_to_dynamo(client, question):
    raw_question = serialize(question)
    client.put_item(
        TableName=DYNAMODB_TABLE_NAME,
        Item=raw_question
    )

def main():
    client_dynamo = boto3.client('dynamodb')
    logger = setup_logging()

    logger.info("loadding questions from questions.json")
    questions = load_questions()

    logger.info("start processing questions")
    for question in questions:
        logger.info(f"check limitations for question id: {question['question_id']} ")
        check_limitations(question)

        logger.info(f"Limitation check pass, start uploading to dynamodb")
        upload_to_dynamo(client_dynamo, question)

if __name__ == "__main__":
    main()