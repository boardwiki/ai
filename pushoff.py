import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

# 기본 데이터 입력
mass = 67.5  # kg (라이더 + 보드 무게)
initial_speed = 5.5  # m/s (푸쉬오프 속력)
rolling_resistance = 0.002  # 구름 저항 계수
air_density = 1.225  # kg/m³ (공기 밀도)
drag_coefficient = 0.9  # 항력 계수 (라이딩 자세에 따라 다름)
frontal_area = 0.5  # m² (몸과 보드의 공기 저항 면적)

# 공기 저항력 & 구름 저항력 계산
def calculate_forces(speed):
    rolling_friction = rolling_resistance * mass * 9.81
    air_drag = 0.5 * air_density * drag_coefficient * frontal_area * speed ** 2
    return rolling_friction + air_drag

# 감속 계산
time_step = 0.1  # 초 단위 시뮬레이션
time_values = [0]
speed_values = [initial_speed]
distance_values = [0]

speed = initial_speed
distance = 0
while speed > 0:
    force_total = calculate_forces(speed)
    acceleration = -force_total / mass
    speed += acceleration * time_step
    distance += speed * time_step
    if speed < 0:
        speed = 0
    time_values.append(time_values[-1] + time_step)
    speed_values.append(speed)
    distance_values.append(distance)

# 그래프 출력
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(time_values, speed_values, label="속도 변화 (m/s)", color="blue")
plt.xlabel("시간 (s)")
plt.ylabel("속도 (m/s)")
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(time_values, distance_values, label="주행 거리 (m)", color="red")
plt.xlabel("시간 (s)")
plt.ylabel("거리 (m)")
plt.legend()
plt.grid()

plt.show()
