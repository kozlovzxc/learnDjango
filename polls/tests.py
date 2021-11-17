import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    def test_displays_as_string(self):
        question = Question(question_text='test')
        self.assertIs(str(question), 'test')


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = Question.objects.create(question_text="Past question.", pub_date=timezone.now())
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = Question.objects.create(question_text="Past question 1.", pub_date=timezone.now())
        question2 = Question.objects.create(question_text="Past question 2.", pub_date=timezone.now())
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question1, question2],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = Question.objects.create(question_text='Future question.',  pub_date=timezone.now() + datetime.timedelta(days=1))
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = Question.objects.create(question_text='Past Question.', pub_date=timezone.now())
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
