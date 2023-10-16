import spidev
import time
from flask import Flask, render_template

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_ph_value():
    adc_channel = 0  # You may need to adjust this based on your wiring.
    raw_value = spi.xfer2([1, (8 + adc_channel) << 4, 0])
    adc_value = ((raw_value[1] & 3) << 8) + raw_value[2]
    voltage = (adc_value * 3.3) / 1023  # Adjust this for your reference voltage
    # Convert voltage to pH value using your sensor's calibration data.
    return voltage
def read_tds():
    try:
        # Send a command to the sensor to request data
        command = 0x23  # Replace with the appropriate command for your sensor
        response = spi.xfer2([command])

        if len(response) >= 3:
            # Process the response to get the TDS value
            # This is a simplified example; real sensors will have their own data format
            tds_value = (response[1] << 8) + response[2]
            return tds_value
        else:
            print("Unexpected response format from the TDS sensor.")
            return None
    except Exception as e:
        print(f"Error reading TDS value: {e}")
        return None




app = Flask(__name__)

@app.route("/")
def index():
    ph_value = read_ph_value()
    tds_value = read_tds()  # Call the function to get TDS value.
    return render_template("ph.html", ph_value=ph_value, tds=tds_value)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
