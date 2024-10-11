# file สำหรับตรวจคำตอบ
# ในกรณีที่มีการสร้าง function อื่น ๆ ให้ระบุว่า input-output คืออะไรด้วย
'''
ชื่อ_รหัส(ex: ธนวัฒน์_6461)
1. ชยณัฐ_6512
2. วริทธิ์ธร_6550
'''
# Import library
import numpy as np
from FRA333_HW3_6512_6550 import endEffectorJacobianHW3 ,checkSingularityHW3 ,computeEffortHW3

# Set up Input Variable

# Define joint angle ranges for q1 - q3
theta1_range = np.linspace(-np.pi ,np.pi ,10)  # Joint 1
theta2_range = np.linspace(-np.pi ,np.pi ,10)  # Joint 2
theta3_range = np.linspace(-np.pi ,np.pi ,10)  # Joint 3

#===========================================<ตรวจคำตอบ>====================================================#

for theta1 in theta1_range:
    for theta2 in theta2_range:
        for theta3 in theta3_range:
            
            # Set list q
            q = [theta1 ,theta2 ,theta3]

            # Random wrench list
            w = np.random.rand(1,6)

            # Call funtion find EndEffector Jacobian < ข้อ 1 >
            J_e = endEffectorJacobianHW3(q)

            # Call funtion check Singularity  < ข้อ 2 >
            flag = checkSingularityHW3(q)

            # Call funtion compute Effort  < ข้อ 3 >
            tau = computeEffortHW3(q ,w)

            # Input show
            print(f'Joint Configuration : {q}')
            print(f'Wrench at EndEffector : {w}')

            # แสดงผล ข้อ 1
            print(f'--------ข้อ 1--------')
            print(f'Jacobian :\n{J_e}')
            print(f'Reduce Jacobian :\n{J_e[:3, :3]}')

            # แสดงผล ข้อ 2
            print(f'--------ข้อ 2--------')
            print(f'Singularity : {flag}')

            # แสดงผล ข้อ 3
            print(f'--------ข้อ 3--------')
            print(f'Joint Effort :\n{tau}')

            print('-'*30)
