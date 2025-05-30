from logs.models import Log


STATUS_MAP = {'failure': 'Неудачная попытка зачисления средств.',
              'success': 'Успешное зачисление средств на баланс организации.',
              'already_existed': 'Попытка повторного зачисления средств.'}


class LogService:
    """Сервис для логирования платежей"""
    @staticmethod
    def create_log(status: str, data: dict, exception: Exception = None):
        """Фиксирует логи действий в системе"""
        action = STATUS_MAP.get(status, 'Неизвестный статус')

        data = f"Данные: {data}\n"
        if exception:
            data += f"Ошибка: {str(exception)}"

        Log.objects.create(
            action=action,
            data=data
        )
