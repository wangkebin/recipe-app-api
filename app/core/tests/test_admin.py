from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="testadmin@abc.com", password="adminpass"
        )

        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="test@abc.com", password="pass", name="test user"
        )

    def test_user_listed(self):
        """Test that users are listed on user page"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_create_page(self):
        """Test that the user create page works"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
