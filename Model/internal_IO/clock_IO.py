import datetime
import threading
from typing import Optional
from Model.binio import Bin_IO
from View.binio_frames.binio_view_default import BinIODefault

class Clock_IO(Bin_IO):
    """
    A binary I/O that changes its status based on time conditions.
    When the current time matches the target time, the status becomes True for one minute.
    """
    
    def __init__(self, 
                 name: str = "clock",
                 target_time: str = "00:00",
                 days_of_week: Optional[list] = None,
                 result_true: str = "Time condition met",
                 result_false: str = "Time condition not met",
                 mapping_view=None):
        """
        Initialize the Clock_IO.
        
        Args:
            name: Name of the clock instance
            target_time: Time in 'HH:MM' format when the status should become True
            days_of_week: List of weekdays (0-6, where 0 is Monday) when the clock should be active.
                         If None, the clock is active every day.
            result_true: Description when the clock is active
            result_false: Description when the clock is inactive
            mapping_view: The mapping view canvas where the clock tile will be displayed
        """
        super().__init__(name, result_true, result_false)
        self._target_time = datetime.datetime.strptime(target_time, "%H:%M").time()
        self._days_of_week = set(days_of_week) if days_of_week is not None else None
        self._last_triggered = None
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._time_check_loop, daemon=True)
        
        # Create a tile in the mapping view if provided
        self._tile = None
        if mapping_view:
            self._create_mapping_tile(mapping_view, name)
        
        self._thread.start()
    
    def _create_mapping_tile(self, mapping_view, name: str) -> None:
        """Create a visual representation of this clock in the mapping view."""
        try:
            canvas = mapping_view.get_mappingview()
            if canvas:
                self._tile = BinIODefault(
                    parent=canvas,
                    binio_name=f"clock_{name}",
                    x_position=200,
                    y_position=200
                )
        except Exception as e:
            print(f"Error creating clock tile: {e}")
    
    def _time_check_loop(self) -> None:
        """Background thread that checks the time and triggers evaluation when needed."""
        while not self._stop_event.is_set():
            now = datetime.datetime.now()
            current_time = now.time()
            
            # Check if today is an active day
            active_day = (self._days_of_week is None or now.weekday() in self._days_of_week)
            
            # Check if current time is exactly the target time (within the same minute)
            if (active_day and 
                current_time.hour == self._target_time.hour and 
                current_time.minute == self._target_time.minute):
                
                # If we haven't triggered yet this minute
                if self._last_triggered != now.replace(second=0, microsecond=0):
                    self._last_triggered = now.replace(second=0, microsecond=0)
                    # Schedule evaluation to set status to True
                    self.evaluate()
                    # Schedule status reset after 1 minute
                    threading.Timer(60.0, self._schedule_reset).start()
            
            # Sleep until next second for more precise timing
            self._stop_event.wait(1.0)
    
    def _schedule_reset(self) -> None:
        """Schedule a reset of the status to False."""
        self.evaluate()
    
    def _evaluate_impl(self) -> None:
        """
        Implementation of the evaluation logic.
        This is called automatically when the status needs to be updated.
        """
        now = datetime.datetime.now()
        current_time = now.time()
        
        # Determine if we should be in the active minute
        active_minute = (current_time.hour == self._target_time.hour and 
                        current_time.minute == self._target_time.minute)
        
        # Check if today is an active day
        active_day = (self._days_of_week is None or now.weekday() in self._days_of_week)
        
        # Calculate new status
        new_status = active_day and active_minute
        
        # Update status if changed
        if new_status != self._status:
            self._status = new_status
            status_str = "True" if self._status else "False"
            print(f"[{datetime.datetime.now()}] {self._name}: Status changed to {status_str}")
            
            # Update tile appearance if it exists
            if hasattr(self, '_tile') and self._tile:
                try:
                    self._tile.frame.configure(
                        bg="green" if self._status else "red",
                        text=f"clock_{self._name}\n{status_str}"
                    )
                except Exception as e:
                    print(f"Error updating clock tile: {e}")
            
            # Notify all subscribers
            with self._lock:
                subscribers = list(self._subscribers)
            
            for subscriber in subscribers:
                try:
                    subscriber.evaluate()
                except Exception as e:
                    print(f"Error notifying subscriber {subscriber._name}: {e}")
    
    def cleanup(self) -> None:
        """Clean up resources when the clock is no longer needed."""
        self._stop_event.set()
        self._thread.join(timeout=1.0)
        # Clean up the tile if it exists
        if hasattr(self, '_tile') and self._tile:
            try:
                self._tile.frame.destroy()
            except Exception as e:
                print(f"Error cleaning up clock tile: {e}")
        if hasattr(super(), 'cleanup'):
            super().cleanup()
