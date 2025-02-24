from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from task_manager.tasks.models import Tasks
from task_manager.statuses.models import Statuses


class TasksTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Создание тестового пользователя, исполнителя и статуса"""
        cls.user = get_user_model().objects.create(
            username="volkovor777228",
            first_name="Lev",
            last_name="Smith",
        )
        cls.user.set_password("1234")
        cls.user.save()

        cls.executor = get_user_model().objects.create(
            username="Slava",
            first_name="Slava",
            last_name="Petrov",
        )
        cls.executor.set_password("1234")
        cls.executor.save()

        cls.status = Statuses.objects.create(name="oka")

    def setUp(self):
        """Логиним пользователя перед каждым тестом"""
        login_successful = self.client.login(username="volkovor777228", password="1234")
        self.assertTrue(login_successful, "Не удалось залогинить пользователя!")


    def test_create_task(self):
        """Проверка создания задачи"""
        data_task = {
            "name": "enjoy",
            "description": "gsgsd",
            "status": self.status.pk,  
            "executor": self.executor.pk,
        }
        response = self.client.post(reverse("tasks:create"), data_task)

        self.assertRedirects(response, reverse("tasks:list"))

        task = Tasks.objects.get(name=data_task["name"])
        self.assertEqual(task.name, data_task["name"])
        self.assertEqual(task.description, data_task["description"])
        self.assertEqual(task.status.pk, data_task["status"])
        self.assertEqual(task.executor.pk, data_task["executor"])

    def test_update_task(self):
        """Проверка обновления задачи"""
        data_task = {
            "name": "enjoy",
            "description": "gsgsd",
            "status": self.status.pk,
            "executor": self.executor.pk,
        }
        self.client.post(reverse("tasks:create"), data_task)

        task = Tasks.objects.get(name=data_task["name"])
        self.assertEqual(task.name, data_task["name"])

        data_task_update = {
            "name": "enjoy_updated",
            "description": "new description",
            "status": self.status.pk,
            "executor": self.executor.pk,
        }
        response = self.client.post(
            reverse("tasks:update", args=[task.pk]), data_task_update
        )

        self.assertRedirects(response, reverse("tasks:list"))

        updated_task = Tasks.objects.get(pk=task.pk)
        self.assertEqual(updated_task.name, data_task_update["name"])
        self.assertEqual(updated_task.description, data_task_update["description"])

    def test_delete_task(self):
        """Проверка удаления задачи"""
        data_task = {
            "name": "enjoy",
            "description": "gsgsd",
            "status": self.status.pk,
            "executor": self.executor.pk,
        }
        self.client.post(reverse("tasks:create"), data_task)
        task = Tasks.objects.get(name=data_task["name"])

        self.assertEqual(task.name, data_task["name"])

        response = self.client.post(reverse("tasks:delete", args=[task.pk]))

        self.assertRedirects(response, reverse("tasks:list"))

        with self.assertRaises(ObjectDoesNotExist):
            Tasks.objects.get(name=data_task["name"])