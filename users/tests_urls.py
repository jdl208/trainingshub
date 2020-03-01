from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users import views as uv
from django.contrib.auth import views as av


class TestUrls(SimpleTestCase):
    def test_if_user_list_is_resolved(self):
        url = reverse("user_list")
        self.assertURLEqual(resolve(url).func, uv.userlist)

    def test_if_user_search_is_resolved(self):
        url = reverse("user-search")
        self.assertURLEqual(resolve(url).func, uv.user_search)

    def test_if_register_is_resolved(self):
        url = reverse("register")
        self.assertURLEqual(resolve(url).func, uv.register)

    def test_if_login_is_resolved(self):
        url = reverse("login")
        print(resolve(url))
        self.assertURLEqual(resolve(url).func.view_class, av.LoginView)

    def test_if_logout_is_resolved(self):
        url = reverse("logout")
        self.assertURLEqual(resolve(url).func, uv.logout)

    def test_if_account_is_resolved(self):
        url = reverse("account")
        self.assertURLEqual(resolve(url).func, uv.account)

    def test_if_profile_is_resolved(self):
        url = reverse("profile")
        self.assertURLEqual(resolve(url).func, uv.profile)

    def test_if_password_reset_is_resolved(self):
        url = reverse("password_reset")
        self.assertURLEqual(resolve(url).func.view_class, av.PasswordResetView)

    def test_if_password_reset_done_is_resolved(self):
        url = reverse("password_reset_done")
        self.assertURLEqual(resolve(url).func.view_class, av.PasswordResetDoneView)

    def test_if_password_reset_confirm_is_resolved(self):
        url = reverse("password_reset_confirm", args=["uid64", "token"])
        self.assertURLEqual(resolve(url).func.view_class, av.PasswordResetConfirmView)

    def test_if_password_reset_complete_is_resolved(self):
        url = reverse("password_reset_complete")
        self.assertURLEqual(resolve(url).func.view_class, av.PasswordResetCompleteView)

    def test_if_user_detail_is_resolved(self):
        url = reverse("user-detail", args=[1])
        self.assertURLEqual(resolve(url).func, uv.user_detail)
