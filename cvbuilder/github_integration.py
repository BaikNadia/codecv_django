import time

import requests
from django.conf import settings
from requests.exceptions import RequestException


class GitHubAPI:
    """Класс для работы с GitHub API"""

    BASE_URL = "https://api.github.com"

    def __init__(self, token=None):
        """
        Инициализация GitHub API клиента

        Args:
            token: Personal Access Token для GitHub API
        """
        self.token = token or getattr(settings, "GITHUB_API_TOKEN", None)
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CodeCV-App",
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def _make_request(self, method, endpoint, **kwargs):
        """
        Выполнение HTTP запроса к GitHub API
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"

        try:
            response = requests.request(
                method=method, url=url, headers=self.headers, timeout=10, **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            raise Exception("Превышено время ожидания GitHub API")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise Exception("Пользователь GitHub не найден")
            elif e.response.status_code == 403:
                # Проверяем лимит запросов
                if "X-RateLimit-Remaining" in e.response.headers:
                    remaining = e.response.headers["X-RateLimit-Remaining"]
                    if remaining == "0":
                        reset_time = e.response.headers.get("X-RateLimit-Reset", 0)
                        wait_time = max(0, int(reset_time) - time.time())
                        raise Exception(
                            f"Лимит GitHub API исчерпан. Попробуйте через {int(wait_time / 60)} минут"
                        )
                raise Exception("Доступ запрещен. Проверьте токен GitHub")
            else:
                raise Exception(f"GitHub API ошибка: {e.response.status_code}")
        except RequestException as e:
            raise Exception(f"Ошибка сети: {str(e)}")

    def get_user_data(self, username):
        """
        Получение данных пользователя GitHub
        """
        response = self._make_request("GET", f"users/{username}")
        return response.json()

    def get_user_repos(self, username, limit=10):
        """
        Получение репозиториев пользователя
        """
        repos = []
        page = 1
        per_page = min(limit, 100)

        while len(repos) < limit:
            params = {
                "per_page": per_page,
                "page": page,
                "sort": "updated",
                "direction": "desc",
                "type": "owner",
            }

            response = self._make_request(
                "GET", f"users/{username}/repos", params=params
            )
            page_repos = response.json()

            if not page_repos:
                break

            repos.extend(page_repos)
            page += 1

            if len(page_repos) < per_page:
                break

        return repos[:limit]

    def analyze_languages(self, repos):
        """
        Анализ языков программирования из репозиториев
        """
        languages = {}
        for repo in repos:
            if repo.get("language"):
                lang = repo["language"]
                languages[lang] = languages.get(lang, 0) + 1
        return languages

    def get_repo_languages(self, owner, repo_name):
        """
        Получение языков конкретного репозитория
        """
        response = self._make_request("GET", f"repos/{owner}/{repo_name}/languages")
        return response.json()
