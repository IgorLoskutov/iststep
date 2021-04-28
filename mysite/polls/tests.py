from datetime import timedelta
import json

from django.test import TestCase, Client
from django.test.utils import setup_test_environment

from django.utils import timezone
from django.shortcuts import redirect
from .models import *


class QuestionModelTest(TestCase):

    # env=setup_test_environment()
    client = Client()


    def _create_question(self, delta):

        return Question(
            pub_date=timezone.now()+timedelta(days=delta), 
            question_text="French Fries, Mazafaka?"
            )

    def _create_choice(self, question, text):
        return Choice(question=question, chice_text=text)

    def test_was_published_resently_with_future_questions(self):
        """was_published_resently() must return False
         for the questions with pub_date in future"""


        future_question = self._create_question(15)

        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_resently_with_old_questions(self):
        """was_published_resently() must return False
         for the questions with pub_date older than 2 day ago"""


        future_question = self._create_question(-15)

        self.assertIs(future_question.was_published_recently(), False)
    
    def test_urls_index(self):

        lates_question = self._create_question(-0.5)
        lates_question.save()

        responce = self.client.get(reverse('polls:index'))

        self.assertContains(responce, lates_question.question_text)

    def test_vote_choice(self):
        lates_question = self._create_question(-0.5)
        lates_question.save()
        choice1 = self._create_choice(lates_question, "Yes please!")
        choice1.save()
        
        responce = self.client.post(
            reverse('polls:vote', kwargs={'question_id':lates_question.id}),
            data={'id':choice1.id},
            )

        self.assertNotEqual(Choice.objects.filter(id=choice1.id).get().votes, 0)
 
