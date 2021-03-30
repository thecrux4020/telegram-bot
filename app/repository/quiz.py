import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from app.helpers import objectview

class QuizRepo:

    def __init__(self, config):
        self.config = config
        self.table_name = config["database"]["table_name"]
        self.client = boto3.client('dynamodb')

    def _deserialize(self, quiz, type_deserializer = TypeDeserializer()):
        quiz = type_deserializer.deserialize({"M": quiz})
        quiz["correct_option"] = int(quiz["correct_option"] )
        return objectview(quiz)

    def _serialize(self, quiz, type_serializer = TypeSerializer()):
        # quiz = type_serializer.serialize({"M": quiz.__dict__})
        quiz = {k: type_serializer.serialize(v) for k,v in quiz.__dict__.items()}
        return quiz

    def get_not_used_quizzes(self):
        """ Get all questions from dynamo table, that was not previously used """
        quizzes = self.client.scan(TableName=self.table_name)
        quizzes = [ 
            self._deserialize(quiz) 
            for quiz in quizzes["Items"] 
            if not quiz["has_been_used"]["BOOL"] 
        ]
        return quizzes

    def update(self, quiz):
        raw_quiz = self._serialize(quiz)
        self.client.update_item(
            TableName=self.table_name,
            Key={
                "question_id": raw_quiz["question_id"]
            },
            UpdateExpression="set has_been_used = :r",
            ExpressionAttributeValues={
                ":r": {"BOOL": quiz.has_been_used}
            },
            ReturnValues="UPDATED_NEW"
        )
