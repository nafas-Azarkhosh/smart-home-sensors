from abc import ABC, abstractmethod

# 1. Abstraction (انتزاع) 
# کلاس پایه برای همه سنسور ها 
class Sensor(ABC):
    def __init__(self, sensor_id, location):
        self.sensor_id = sensor_id
        self.location = location

    @abstractmethod
    def read_data(self):
        """هر سنسور باید این متد را خودش پیاده‌سازی کند"""
        pass

# 2. Mixin (برای وراثت چندگانه) 
class AlertMixin:
    def check_alert(self, current_val, threshold):
        if current_val > threshold:
            return "!!! ALERT !!!"
        else:
            return "STATUS: OK"

#  3. Inheritance & Encapsulation (وراثت و کپسوله‌سازی) 

class TemperatureSensor(Sensor):
    def __init__(self, sensor_id, location, initial_temp=20.0):
        super().__init__(sensor_id, location)
        self._value = initial_temp  #متغیر خصوصی 
        self._threshold = 30.0      

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_val):
        
        if new_val < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._value = new_val

    def read_data(self):
        return f"[{self.sensor_id}] Temp at {self.location}: {self._value}°C"

# وراثت چند گانه
class AlertTemperatureSensor(TemperatureSensor, AlertMixin):
    def read_data(self):
        base_info = super().read_data()
        status = self.check_alert(self.value, self._threshold)
        return f"{base_info} | {status}"

class MotionSensor(Sensor):
    def __init__(self, sensor_id, location):
        super().__init__(sensor_id, location)
        self._is_motion = False

    @property
    def is_motion(self):
        return self._is_motion

    @is_motion.setter
    def is_motion(self, val):
        self._is_motion = val

    def read_data(self):
        status = "MOTION DETECTED!" if self._is_motion else "No motion."
        return f"[{self.sensor_id}] Motion at {self.location}: {status}"

class HumiditySensor(Sensor):
    def __init__(self, sensor_id, location):
        super().__init__(sensor_id, location)
        self._humidity = 50.0

    @property
    def humidity(self):
        return self._humidity

    @humidity.setter
    def humidity(self, val):
        if 0 <= val <= 100:
            self._humidity = val
        else:
            print("Error: Humidity must be between 0 and 100!")

    def read_data(self):
        return f"[{self.sensor_id}] Humidity at {self.location}: {self._humidity}%"

class CameraSensor(Sensor):
    def __init__(self, sensor_id, location):
        super().__init__(sensor_id, location)
        self._recording = False

    @property
    def recording(self):
        return self._recording

    @recording.setter
    def recording(self, val):
        self._recording = val

    def read_data(self):
        status = "RECORDING..." if self._recording else "IDLE"
        return f"[{self.sensor_id}] Camera at {self.location}: {status}"


#  4. Main Program (بخش تعاملی برای اجرا) 

if __name__ == "__main__":
    sensors = [
        AlertTemperatureSensor("TEMP-01", "Living Room", 25.0),
        MotionSensor("MOTION-01", "Garage"),
        HumiditySensor("HUM-01", "Garden"),
        CameraSensor("CAM-01", "Front Door")
    ]

    print("=== Welcome to Smart Home System ===")
    
    try:
        # تست سنسور دما
        print("\n--- Step 1: Temperature Update ---")
        temp_val = float(input("Enter temperature (e.g. 25 or 35): "))
        sensors[0].value = temp_val

        # تست سنسور حرکت
        print("\n--- Step 2: Motion Update ---")
        motion_input = input("Is there motion? (yes/no): ").lower()
        sensors[1].is_motion = (motion_input == "yes")

        # تست رطوبت
        print("\n--- Step 3: Humidity Update ---")
        hum_val = float(input("Enter humidity % (0-100): "))
        sensors[2].humidity = hum_val

        # تست دوربین
        print("\n--- Step 4: Camera Update ---")
        cam_input = input("Start recording? (yes/no): ").lower()
        sensors[3].recording = (cam_input == "yes")

        # نمایش گزارش نهایی
        print("\n" + "="*40)
        print("       FINAL SENSOR REPORT")
        print("="*40)
        for s in sensors:
            # نمایش اطلاعات همه سنسور ها 
            print(s.read_data())
        print("="*40)

    except ValueError as e:
        print(f"\n[!] ERROR: {e}")
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")

    print("\nProgram execution finished.")
