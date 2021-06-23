import mido
from mido import Message
import config as cfg


class MIDIControl():
    def __init__(self):
        self.outport = None

    def open_output(self, port_name: str):
        self.outport = mido.open_output(port_name)
        #print(type(self.outport))

    def __limit(self, value: int, min_: int, max_: int): 
        if value < min_:
            value = min_
        if value > max_:
            value = max_
        return value

    # def note_on(self, note:int):
    #     if note < 30 or 100 < note:
    #         return
    #     msg = Message('note_on', note=note, velocity=127)
    #     self.outport.send(msg)

    def send_control_change(self, ch: int, ctrl: int, value: int):
        value = self.__limit(value, 0, 127)
        msg = Message('control_change', channel=ch, control=ctrl, value=value)
        self.outport.send(msg)
    
    def __del__(self):
        if isinstance(self.outport, mido.backends.rtmidi.Output):
            self.outport.close()

if __name__ == "__main__":
    m = MIDIControl()
    m.open_output(cfg.PORTNAME)
    # m.note_on(60)
    m.send_control_change(0, 50, 100)