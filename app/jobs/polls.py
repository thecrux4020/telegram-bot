import random
import telegram
from app.repository.quiz import QuizRepo

class Poll():

    def __init__(self, bot, channel_id, config):
        self.bot = bot
        self.channel_id = channel_id
        self.config = config
        self.repository = QuizRepo(self.config)
    
    @classmethod
    def setup(self, bot, channel_id, config):
        """ Dummy setup function to create Poll object """
        return Poll(bot, channel_id, config)

    def _get_all_quizzes(self):
        """ Get all not previously used quizzes from repository """
        return self.repository.get_not_used_quizzes()

    def _generate_random(self, start, end):
        """ Generate a random number between end and start params """
        return random.randint(start, end)

    def _send_quiz_to_channel(self, quiz):
        """ Send quiz to telegram channel """
        self.bot.send_poll(
            chat_id=self.channel_id,
            question=quiz.question,
            options=quiz.options,
            type=telegram.Poll.QUIZ,
            correct_option_id=quiz.correct_option,
            explanation=quiz.explanation
        )

    def _mark_quiz_as_used(self, quiz):
        """ mark quiz as used and update into repository """
        quiz.has_been_used = True
        self.repository.update(quiz)

    def start_job(self):
        """ Main function of the job """
        quizzes = self._get_all_quizzes()
        
        if len(quizzes) == 0:
            return
        elif len(quizzes) == 1:
            quiz = quizzes[0]
        else: 
            # pickup quiz based on a pseudo random generated number
            quiz = quizzes[ self._generate_random(0, len(quizzes)) ]
        
        self._send_quiz_to_channel(quiz)
        self._mark_quiz_as_used(quiz)
