class OrganizationMixin:
    def create_organization(self, **data):
        """Функция создаёт организацию"""
        url = "/api/organizations/"
        data = {
            "title": data.get("title", ""),
            "inn": data.get("inn", ""),
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
        return response.data

    def get_organization_data(self, organization_id):
        """Функция возвращает данные организации"""
        url = "/api/organizations/"
        response = self.client.get(
            f"{url}{organization_id}/", format='json')
        return response.data

    def get_organization_balance(self, inn):
        """Функция возвращает ИНН и баланс организации"""
        url = "/api/organizations/"
        response = self.client.get(
            f"{url}{inn}/balance/", format='json')
        return response.data
