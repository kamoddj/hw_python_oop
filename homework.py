from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Возвращает строку сообщения"""
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки.

    Класс Training принимает:

    action -  количество совершённых действий.
    (число шагов при ходьбе и беге либо гребков — при плавании);
    duration - длительность тренировки;
    weight - вес спортсмена.

    Для расчета добавлены атрибуты класса:

    LEN_STEP — расстояние за один шаг или гребок.
    Один шаг — это 0.65 метра, один гребок при плавании — 1.38 метра.
    M_IN_KM — константа для перевода значений из метров в километры.
    HOUR_TO_M: int = 60 - константа для перевода часов в минуты

    Методы классов, которые отвечают за обработку данных:
    расчёт дистанции за тренировку: get_distance();
    расчёт средней скорости движения во время тренировки: get_mean_speed();
    расчёт количества потраченных калорий за тренировку: get_spent_calories();
    создание объекта сообщения о результатах тренировки: show_training_info().

    """
    M_IN_KM = 1000  # Растояние в метрах.
    LEN_STEP = 0.65  # Расстояние за один шаг.
    HOUR_TO_M = 60  # Константа для перевода часов в минуты

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

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
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег.

    CALORIE_MULTIPLIER = 18 - Константа для расчета калорий.
    CALORIE_DIFF = 20 - Константа для расчета калорий.

    """
    CALORIE_MULTIPLIER = 18
    CALORIE_DIFF = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_m: float = self.duration * self.HOUR_TO_M
        calories: float = (self.CALORIE_MULTIPLIER * self.get_mean_speed()
                           - self.CALORIE_DIFF) * self.weight / \
            self.M_IN_KM * duration_m
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.

    Конструктор этого класса принимает дополнительный параметр:
    height — рост спортсмена.

    CALORIE_MULTIPLIER = 0.035 - Константа для расчета калорий.
    CALORIE_DIFF = 0.029 - Константа для расчета калорий.

    """
    CALORIE_MULTIPLIER = 0.035
    CALORIE_DIFF = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_m: float = self.duration * self.HOUR_TO_M
        calories: float = (self.CALORIE_MULTIPLIER
                           * self.weight + (self.get_mean_speed()**2
                                            // self.height)
                           * self.CALORIE_DIFF * self.weight) * duration_m
        return calories


class Swimming(Training):
    """Тренировка: плавание.

    Конструктор класса Swimming принимает еще два параметра:
    length_pool — длина бассейна в метрах;
    count_pool — сколько раз пользователь переплыл бассейн.

    Имеет собственный атрибут LEN_STEP.
    LEN_STEP = 1.38  # Расстояние за один гребок.

    CALORIE_MULTIPLIER = 1.1 - Константа для расчета калорий.
    CALORIE_DIFF = 2 - Константа для расчета калорий.

    """
    LEN_STEP = 1.38
    CALORIE_MULTIPLIER = 1.1
    CALORIE_DIFF = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = (self.get_mean_speed()
                           + self.CALORIE_MULTIPLIER) * self.CALORIE_DIFF\
            * self.weight
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
