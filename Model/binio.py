
class Bin_IO:
    """
    This class represents a binary input/output element of a MOSTwo system. It is the main component of the machine
    algorithm.

    A binary input/output element is a device that can have two states: true or false ('Status`).

    Attributes:
    name (str): The name of the binary input/output element.
    result_true (str): A descriptive string when the element is true.
    result_false (str): A descriptive string when the element is false.
    status (bool): The status of the element. True if it's on, False if it's off.
    subscribers (list): A list of instances that have subscribed to this binio.
    subscriptions (list): A list of binio where this instance is subscribed to.
    _bin_io_collection (list): A collection of all instances of type Bin_IO.
    """
    #collection of all instances of this type
    _bin_io_collection = list()

    def __init__(self, name: str, result_true: str, result_false: str, status: bool) -> None:

        self._name = name
        self._result_true = result_true
        self._result_false = result_false
        self._status = status #creates status property and sets it to given initial value
        self._subscribers = list() #collection of instances that have subscribed to this binio
        self._subscriptions = list() #collection of binio where this instance is subscribed to.
        Bin_IO._bin_io_collection.append(self)

    def __del__(self):
        Bin_IO._bin_io_collection.remove(self)

    def __str__(self) -> str:
        return f"{self._name} {self._result_true} {self._result_false} {self._status}"

    def __iter__(self):
        return iter(self._bin_io_collection)

    def __next__(self):
        try:
            item = self._bin_io_collection[self.current]
        except IndexError:
            raise StopIteration()
        self.current += 1
        return item

    def evaluate(self) -> None:
        pass

    def add_subscriber(self, subscriber) -> None:
        self._subscribers.append(subscriber)

    def del_subscriber(self, subscriber) -> None:
        self._subscribers.remove(subscriber)

    def inform_subscribers(self) -> None:
        for subscriber in self._subscribers:
            subscriber.evaluate()

    def add_subscription(self, subscription: type['Bin_IO']) -> None:
        subscription.add_subscriber(self)
        self._subscriptions.append(subscription)

    def remove_subscription(self, subscription: type['Bin_IO']) -> None:
        subscription.del_subscriber(self)
        self._subscriptions.remove(subscription)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def result_true(self) -> str:
        return self._result_true

    @result_true.setter
    def result_true(self, result_true: str) -> None:
        self._result_true = result_true

    @property
    def result_false(self) -> str:
        return self._result_false

    @result_false.setter
    def result_false(self, result_false: str) -> None:
        self._result_false = result_false

    @property
    def status(self) -> bool:
        return self._status

    @status.setter
    def status(self, status: bool) -> None:
        self._status = status

