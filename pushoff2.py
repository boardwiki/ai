import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 기본 데이터 입력
mass_board = 5  # kg (보드 무게)
mass_rider = 64  # kg (라이더 무게)
total_mass = mass_board + mass_rider  # 총 질량
acceleration = 1.5  # m/s^2 # 가속도 (1.5배 가속도를 가정)
push_force = total_mass * acceleration  # N 푸쉬오프 힘 계산 (F = ma)
push_time = 0.4  # 푸쉬오프 지속 시간 (초)

rolling_resistance = 0.002  # 구름 저항 계수
air_density = 1.225  # kg/m³ (공기 밀도)
drag_coefficient = 0.9  # 항력 계수 (라이딩 자세에 따라 다름)
frontal_area = 0.5  # m² (몸과 보드의 공기 저항 면적)

# 푸쉬오프에 의한 가속도 계산 (F = ma)
push_acceleration = push_force / total_mass  # 푸쉬오프 순간 가속도

# 푸쉬오프 후 속도 변화 (v = u + at, u = 0 (초기속도))
initial_speed = push_acceleration * push_time  # 푸쉬오프 후 순간 속도

# 공기 저항력 & 구름 저항력 계산
def calculate_forces(speed):
    rolling_friction = rolling_resistance * total_mass * 9.81
    air_drag = 0.5 * air_density * drag_coefficient * frontal_area * speed ** 2
    return rolling_friction + air_drag

# 푸쉬오프의 효과 감소 (속도가 빨라질수록 푸쉬오프가 점차 비효율적으로 됨)
def adjusted_push_force(speed):
    # 속도가 빠를수록 푸쉬오프 힘이 덜 효과적으로 작용하도록 설정
    efficiency_factor = max(0.1, 1 - 0.01 * speed)  # 속도가 증가할수록 푸쉬오프의 효율 감소
    return push_force * efficiency_factor

# 감속 계산
time_step = 0.1  # 초 단위 시뮬레이션
time_values = [0]
speed_values = [initial_speed]
distance_values = [0]

speed = initial_speed
distance = 0
total_time = 0  # 전체 시간

# 푸쉬오프 3번 (푸쉬 주기는 0초, 3초, 6초)
push_count = 3  # 푸쉬 횟수
push_times = [0, 3, 6]  # 푸쉬가 발생하는 시간 (초)

# 푸쉬 후 속도 변화 기록을 위한 리스트
push_speed_increase = []  # 각 푸쉬 후 속도 증가 기록

# 3번 푸쉬오프 후 감속 시작
push_done = 0  # 푸쉬 횟수 추적
while total_time < 120:  # 2분 동안 시뮬레이션 (120초)
    # 푸쉬오프 적용 (총 3번)
    if push_done < push_count:
        # 푸쉬오프가 발생하는 시간 체크
        if total_time >= push_times[push_done]:
            effective_push_force = adjusted_push_force(speed)
            push_acceleration = effective_push_force / total_mass  # 푸쉬오프 후 가속도
            speed += push_acceleration * push_time  # 푸쉬오프가 적용된 순간 속도
            time_values.append(total_time)
            speed_values.append(speed)
            distance_values.append(distance)
            push_speed_increase.append(speed)  # 푸쉬 후 속도 증가 기록
            push_done += 1
        else:
            # 푸쉬가 발생하기 전까지는 감속을 적용
            force_total = calculate_forces(speed)
            acceleration = -force_total / total_mass
            speed += acceleration * time_step
            distance += speed * time_step
            total_time += time_step
            if speed < 0:
                speed = 0
            time_values.append(total_time)
            speed_values.append(speed)
            distance_values.append(distance)
    else:
        # 푸쉬 후 감속 (가속도와 속도 업데이트)
        force_total = calculate_forces(speed)
        acceleration = -force_total / total_mass
        speed += acceleration * time_step
        distance += speed * time_step
        total_time += time_step
        if speed < 0:
            speed = 0
        time_values.append(total_time)
        speed_values.append(speed)
        distance_values.append(distance)

# 그래프 출력
plt.figure(figsize=(10, 6))

# 전체 속도 변화 그래프
plt.subplot(2, 1, 1)
plt.plot(time_values, speed_values, label="전체 속도 변화 (m/s)", color="green")
plt.xlabel("시간 (s)")
plt.ylabel("속도 (m/s)")
plt.legend()
plt.grid()

# 주행 거리 그래프
plt.subplot(2, 1, 2)
plt.plot(time_values, distance_values, label="주행 거리 (m)", color="red")
plt.xlabel("시간 (s)")
plt.ylabel("거리 (m)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
