from django.test import TestCase
from mypa.views import *

class PunctuatorTestCases(TestCase):
    def test_punctuation(self):
        input1 = "Hi Shivam What have you done till now I have completed NLP and today I will be working on training well done"
        output1 = "Hi Shivam, What have you done till now? I have completed NLP and today I will be working on training. Well done. "

        input2 = "I read a story there was a gull named johanath we wanted to fly 1000 feet one day he did that and his parent told him that you will die one day if you keep doing it"
        output2 = "I read a story: there was a gull named johanath. We wanted to fly 1000 feet one day. He did that and his parent told him that you will die one day if you keep doing it. "

        input3 = "What do you plan for today I have decided to play cricket beacuse it's been long time since i played cricket after that i will be working on Nlp ok"
        output3 = "What do you plan for today? I have decided to play cricket beacuse. It'S been long time since i played cricket after that, i will be working on Nlp. Ok, "

        self.assertEqual(punctuator(input1), output1)
        self.assertEqual(punctuator(input2), output2)
        self.assertEqual(punctuator(input3), output3)

class SpecialSymbolTrimmer(TestCase):
    def test_special_symbol_trimmer(self):
        input1 = ["Hi", "everybody," , "what", "did", "you", "complete", "yesterday?"]
        output1 = ["Hi", "everybody", "what", "did", "you", "complete", "yesterday?"]

        input2 = ["john,", "done."]
        output2 = ["john", "done"]
        self.assertEqual(trim_sentence(input1), output1)
        self.assertEqual(trim_sentence(input2), output2)

class QuestionSentenceTestCases(TestCase):
    def test_sentence_type(self):
        text1 = ["what", "did", "you", "complete", "yesterday"]
        text2 = ["are", "you", "planning", "holiday", "?"]
        text3 = ["I", "love", "cricket"]

        self.assertEqual(sentence_type_question(text1), True)
        self.assertEqual(sentence_type_question(text2), True)
        self.assertEqual(sentence_type_question(text3), False)


class GetSentenceTestCases(TestCase):
    def test_get_setence_module(self):
        text1 = "Hi shivam, what have you done till now I have completed ajax call what will you do today today i will be working on nlp"
        out1 = [["I", "have", "completed", "ajax", "call"],["I", "will", "be", "working", "on", "nlp"]]

        text2 = "Can we go outside for 1 hour why will you go outside at 1:00PM"
        out2 = []

        self.assertEqual(get_sentences(text1), out1)
        self.assertEqual(get_sentences(text2), out2)

class GetImportantSentenceTestCases(TestCase):
    def test_get_important_sentence(self):
        input1 = "Hi shivam what have you done till now I have completed ajax call what will you do today today i will be working on nlp what did you complete the day before yesterday I played football"
        res = get_sentences(input1)
        output1 = ['I have completed ajax call<br />', 'I will be working on nlp<br />']

        input2 = "What will you do today first i will complete a contest on leetcode after that i will train my application ok fine what will you do at evening I will be playing tt"

        self.assertEqual(get_important_sentence(res), output1)




