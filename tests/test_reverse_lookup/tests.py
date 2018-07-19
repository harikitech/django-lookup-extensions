from __future__ import unicode_literals

from django.core.exceptions import FieldError

try:
    from reverse_lookup.models import Poll, User
    from reverse_lookup.tests import ReverseLookupTests as DjangoReverseLookupTests
except ImportError:
    print("Run tests/bootstrap.py before run tests.")
    raise


class ReverseLookupTests(DjangoReverseLookupTests):
    def test_negate_reverse_by_field(self):
        u1 = User.objects.get(
            poll__question__neexact="What's the first question?"
        )
        self.assertEqual(u1.name, "Jim Bo")

        u2 = User.objects.get(
            poll__question__neexact="What's the second question?"
        )
        self.assertEqual(u2.name, "John Doe")

    def test_negate_reverse_by_related_name(self):
        with self.assertRaises(Poll.DoesNotExist):
            Poll.objects.get(poll_choice__name__neexact="This is the answer.")

        p2 = Poll.objects.get(
            related_choice__name__neexact="This is not the answer.")
        self.assertEqual(p2.question, "What's the second question?")

    def test_negate_reverse_field_name_disallowed(self):
        msg = (
            "Cannot resolve keyword 'choice' into field. Choices are: "
            "creator, creator_id, id, poll_choice, question, related_choice"
        )
        with self.assertRaisesMessage(FieldError, msg):
            Poll.objects.get(choice__name__neexact="This is the answer")
