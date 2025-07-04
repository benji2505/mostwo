
import threading
from queue import Queue, Empty
from typing import List, Type, TypeVar, Optional

T = TypeVar('T', bound='Bin_IO')

class Bin_IO:
    """
    This class represents a binary input/output element of a MOSTwo system. It is the main component of the machine
    algorithm.

    A binary input/output element is a device that can have two states: true or false ('Status`).
    This implementation is thread-safe.

    Attributes:
    name (str): The name of the binary input/output element.
    result_true (str): A descriptive string when the element is true.
    result_false (str): A descriptive string when the element is false.
    status (bool): The status of the element. True if it's on, False if it's off.
    subscribers (list): A list of instances that have subscribed to this binio.
    subscriptions (list): A list of binio where this instance is subscribed to.
    _bin_io_collection (list): A collection of all instances of type Bin_IO.
    """
    # Collection of all instances of this type
    _bin_io_collection = list()
    _collection_lock = threading.RLock()  # Lock for thread-safe collection access

    def __init__(self, name: str, result_true: str, result_false: str) -> None:
        self._name = name
        self._result_true = result_true #description of result when true
        self._result_false = result_false #description of result when false
        self._status = bool()  #this is the main property of this instance where everything revolves aroundIt is manipulated in the evaluate method
        self._subscribers = list()  # Collection of instances that have subscribed to this binio
        self._subscriptions = list()  # Collection of binio where this instance is subscribed to
        self._lock = threading.RLock()  # General lock for instance variables
        self._evaluation_queue = Queue()  # Thread-safe queue for evaluation requests
        self._running = True
        self._worker_thread = threading.Thread(target=self._evaluation_worker, daemon=True)
        self._worker_thread.start()
        
        with Bin_IO._collection_lock:
            Bin_IO._bin_io_collection.append(self)

    def _evaluation_worker(self) -> None:
        """Worker thread that processes evaluation requests."""
        while self._running:
            try:
                # Wait for evaluation request with timeout to allow checking self._running
                callback, *args = self._evaluation_queue.get(timeout=0.1)
                callback(*args)
                self._evaluation_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                print(f"Error in evaluation worker for {self._name}: {e}")

    def __del__(self):
        self.cleanup()
        try:
            with Bin_IO._collection_lock:
                Bin_IO._bin_io_collection.remove(self)
        except ValueError:
            pass

    def cleanup(self) -> None:
        """Clean up resources and stop worker threads."""
        self._running = False
        if self._worker_thread.is_alive():
            self._worker_thread.join(timeout=1.0)

    def __str__(self) -> str:
        return f"{self._name} {self._result_true} {self._result_false} {self._status}"

    def __iter__(self):
        return iter(self._bin_io_collection)

    def __next__(self):
        try:
            with Bin_IO._collection_lock:
                item = self._bin_io_collection[self.current]
        except (IndexError, AttributeError):
            self.current = 0
            raise StopIteration()
        self.current += 1
        return item

    def evaluate(self) -> None:
        """Schedule evaluation to run in the worker thread."""
        self._evaluation_queue.put((self._evaluate_impl,))

    def _evaluate_impl(self) -> None:
        """Actual implementation of evaluate that runs in the worker thread."""
        # Your evaluation logic here
        # get value of subscriptions
        # set new value of status for this instance if applicable
        # inform subscribers if status change
        pass

    def add_subscriber(self, subscriber: 'Bin_IO') -> None:
        """Thread-safe addition of a subscriber."""
        with self._lock:
            if subscriber not in self._subscribers:
                self._subscribers.append(subscriber)

    def del_subscriber(self, subscriber: 'Bin_IO') -> None:
        """Thread-safe removal of a subscriber."""
        with self._lock:
            if subscriber in self._subscribers:
                self._subscribers.remove(subscriber)

    def inform_subscribers(self) -> None:
        """Inform all subscribers in separate threads."""
        with self._lock:
            subscribers = list(self._subscribers)  # Create a thread-safe copy
            
        for subscriber in subscribers:
            threading.Thread(
                target=subscriber.evaluate, #triggers the evaluate method for each subscriber
                daemon=True
            ).start()

    def add_subscription(self, subscription: 'Bin_IO') -> None:
        """Add a subscription in a thread-safe manner."""
        subscription.add_subscriber(self)
        with self._lock:
            if subscription not in self._subscriptions:
                self._subscriptions.append(subscription)

    def remove_subscription(self, subscription: 'Bin_IO') -> None:
        """Remove a subscription in a thread-safe manner."""
        subscription.del_subscriber(self)
        with self._lock:
            if subscription in self._subscriptions:
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
    def status(self) -> bool:       # this is the important Property - os this instance of Bin_IO evaluating to True or False
        return self._status

    @status.setter
    def status(self, status: bool) -> None:  #I think this should be private
        self._status = status

