import sys
import time

class RfidState:
    def update_state(self):
        pass

    def description(self):
        pass

class RfidAckFailedState(RfidState):
    def update_state(self):
        pass

    def description(self):
        return "Ack failed"

class RfidAckSuccessState(RfidState):
    def update_state(self):
        pass

    def description(self):
        return "Ack Success"

class RfidIsReadyState(RfidState):
    def update_state(self):
        pass

    def description(self):
        return "RFID is ready"

class RfidNotConnectedState(RfidState):
    def update_state(self):
        pass

    def description(self):
        return "RFID is not connected"

class RfidConnectedState(RfidState):
    def update_state(self):
        pass

    def description(self):
        return "RFID is connected"

class RfidTrigger:
    def __init__(self, alert_manager, num_device=1):
        self.state = RfidIsReadyState()
        self.alert_manager = alert_manager
        self.num_device = num_device
        self.listener = None

    def read(self):
        if self.state.description() == "RFID is connected":
            pass  # Ajoutez le code pour lire les données RFID
        return False

    def check_rfid_connection(self):
        if self.listener:
            self.state = RfidConnectedState()
        else:
            self.state = RfidNotConnectedState()

    def check_rfid_is_ready(self):
        if self.state.description() == "RFID is ready":
            return True
        else:
            return False

class RFIDAlertManager:
    def __init__(self, alert_func):
        self.alert_func = alert_func

    def alert(self, msg):
        self.alert_func(msg)

def check_rfid_connection(rfid_obj, timeout):
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        rfid_obj.check_rfid_connection()
        if rfid_obj.state.description() == "RFID is connected":
            return True
        time.sleep(1)
    return False

def check_rfid_is_ready(rfid_obj, timeout):
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        if rfid_obj.check_rfid_is_ready():
            return True
        time.sleep(1)
    return False

def rfid_trouble(msg):
    print(f"RFID Trouble: {msg}")

