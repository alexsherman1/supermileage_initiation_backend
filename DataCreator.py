import math
import pandas as pd
import numpy as np

def generate_ticks(length: int) -> pd.DataFrame:
  #One millisecond per row
  df = pd.DataFrame({"time (ms)": range(length) })
  return df

def generate_current(length: int) -> pd.DataFrame:
  x = np.arange(length)

  current = (
      123 + 197 * np.exp(-0.02 * (x - 10) ** 2) + 152 * np.exp(-0.05 * (x - 17) ** 2) + 161 * np.exp(-0.05 * (x - 24) ** 2)
  )
  return pd.DataFrame({"current (A)": current})

def generate_voltage(length: int) -> pd.DataFrame:
  x = np.arange(length)

  voltage = (
      12
      + 2.5 * np.sin(2 * np.pi * x / 5000)
      + 0.8 * np.sin(2 * np.pi * x / 700)
  )

  return pd.DataFrame({"voltage (V)": voltage})

def generate_speed(length: int) -> pd.DataFrame:
  dt = 0.001
  max_speed = 50 / 3.6

  speed = np.zeros(length)

  for i in range(1, length):
    t = i * dt

    # Acceleration phase
    if t < 7:
      acceleration = 2.0

    # Cruise
    elif t < 15:
      acceleration = 0.0

    # Gentle braking
    elif t < 20:
      acceleration = -2.5

    # Accelerate again
    else:
      acceleration = 1.5

    speed[i] = speed[i - 1] + acceleration * dt

    # Physical limits
    speed[i] = max(0, min(speed[i], max_speed))

  return pd.DataFrame({
    "speed (km/h)": speed * 3.6
  })

def generate_throttle(length: int) -> pd.DataFrame:
  dt = 0.001  # 1 ms

  throttle = np.zeros(length)
  target = np.zeros(length)

  for i in range(1, length):
    t = i * dt

    # Acceleration
    if t < 7:
      target[i] = 0.75

    # Cruising
    elif t < 15:
      target[i] = 0.25

    # Braking / slowing down
    elif t < 20:
      target[i] = 0.05

    # Accelerating again
    else:
      target[i] = 0.60

    # Smooth throttle response
    response = 0.01
    throttle[i] = throttle[i - 1] + (
        target[i] - throttle[i - 1]
    ) * response

  # Keep throttle between 0 and 100%
  throttle = np.clip(throttle * 100, 0, 100)

  return pd.DataFrame({
    "throttle (%)": throttle
})

def generate_data(length: int) -> pd.DataFrame:
  df = generate_ticks(length)
  df["current (A)"] = generate_current(length)["current (A)"]
  df["voltage (V)"] = generate_voltage(length)["voltage (V)"]
  df["speed (km/h)"] = generate_speed(length)["speed (km/h)"]
  df["throttle (%)"] = generate_throttle(length)["throttle (%)"]
  return df

