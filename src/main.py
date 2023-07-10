import lcd as l
import time
import machine


def drawGauge(fore, back, cur, total):
    border = 5
    lcd.fill(back)
    w = lcd.width-border*2
    till = w * cur // total
    lcd.rect(border, border, till, lcd.height-border*2, l.BLACK, True)
    lcd.rect(border + till, border, w - till, lcd.height-border*2, fore, True)
    lcd.display()


tick = False


def timeHandler(t):
    global tick
    tick = True


def drawTimer(sec, fore, back):
    global tick
    tim = machine.Timer(period=1000, mode=machine.Timer.PERIODIC, callback=timeHandler)
    for s in range(sec):
        drawGauge(fore, back, s, sec)
        while not tick:
            time.sleep(0.1)
        tick = False
    tim.deinit()
    tick = False


# check if the device woke from a deep sleep
if machine.reset_cause() != machine.PWRON_RESET:
    machine.Pin(25, machine.Pin.OUT, value=0)
    machine.deepsleep(600000)

lcd = l.LCD_0inch96()

drawTimer(25*60, l.RED, l.BLUE)
drawTimer(5*60, l.GREEN, l.BLUE)

lcd.fill(l.BLUE)
lcd.display()
lcd.backlight(0)

lcd.write_cmd(0x10)  # power off

machine.deepsleep(600000)
