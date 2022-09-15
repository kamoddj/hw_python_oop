class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type  # Тип тренировки.
        self.duration = duration  # Продолжительность тренировки.
        self.distance = distance  # Дистанция.
        self.speed = speed  # Скорость.
        self.calories = calories  # Потраченые калории.

    def get_message(self) -> str:
        """Возвращает строку сообщения"""
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.'
                        )
        return message


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000  # Растояние в метрах
    LEN_STEP: float = 0.65  # Расстояние за один шаг.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action  # Количество совершённых действий.
        self.duration = duration  # Длительность тренировки.
        self.weight = weight  # Вес спортсмена.

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65  # Расстояние за один шаг.
    M_IN_KM: float = 1000  # Растояние в метрах

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action  # Количество совершённых действий.
        self.duration = duration  # Длительность тренировки.
        self.weight = weight  # Вес спортсмена.
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_m: float = self.duration * 60
        calories: float = (18 * self.get_mean_speed() - 20)\
            * self.weight / self.M_IN_KM * duration_m
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65  # Расстояние за один шаг.
    M_IN_KM: float = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        self.action = action  # Количество совершённых действий.
        self.duration = duration  # Длительность тренировки.
        self.weight = weight  # Вес спортсмена.
        super().__init__(action, duration, weight)
        self.height = height  # Рост спортсмена.

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_m: float = self.duration * 60
        calories: float = (0.035 * self.weight + (self.get_mean_speed()**2
                           // self.height) * 0.029 * self.weight) * duration_m
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # Расстояние один один гребок.
    M_IN_KM: float = 1000  # Растояние в метрах.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        self.action = action  # Количество совершённых действий.
        self.duration = duration  # Длительность тренировки.
        self.weight = weight  # Вес спортсмена.
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # Длина бассейна в метрах.
        self.count_pool = count_pool  # Cколько раз переплыл басcейн.

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return calories

    def get_mean_speed(self) -> float:
        """Расчет средней скорости при плавании."""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict = {'SWM': Swimming,
            'RUN': Running,
            'WLK': SportsWalking
            }
    return dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
