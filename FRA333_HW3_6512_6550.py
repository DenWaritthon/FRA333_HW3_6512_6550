# file สำหรับเขียนคำตอบ
# ในกรณีที่มีการสร้าง function อื่น ๆ ให้ระบุว่า input-output คืออะไรด้วย
'''
ชื่อ_รหัส(ธนวัฒน์_6461)
1. ชยณัฐ_6512
2. วริทธิ์ธร_6550
'''
# import library
from HW3_utils import FKHW3
import numpy as np

#=============================================<คำตอบข้อ 1>======================================================#
def endEffectorJacobianHW3(q:list[float])->list[float]:

    # Call funtion Forward Kinematics by configuration q
    R,P,R_e,p_e = FKHW3(q)

    # Initial Linear and Angular Jacobian
    J_v = np.empty((3, 3))
    J_w = np.empty((3, 3))

    for i in range(3):
        # calculate Rotation joint i
        r = np.dot(R[:,:,i],[[0],[0],[1]])
        r = r.reshape(3,)

        # Calculate Linear joint i
        d = p_e - P[:,i]
        
        # Calculate Linear Jacobian joint i
        j_trans = np.cross(r,d)

        # Set Linear Jacobian 
        J_v[0][i] = j_trans[0]
        J_v[1][i] = j_trans[1]
        J_v[2][i] = j_trans[2]

        # Set Angular Jacobian
        J_w[0][i] = r[0]
        J_w[1][i] = r[1]
        J_w[2][i] = r[2]

    # Concatenate Linear and Angular Jacobian to full Jacobian
    J = np.concatenate((J_v, J_w), axis=0)

    return J
#==============================================================================================================#

#=============================================<คำตอบข้อ 2>======================================================#
def checkSingularityHW3(q:list[float])->bool:
    
    # Initial epsilon
    e = 0.001

    # Call funtion endEffectorJacobian by configuration q
    J = endEffectorJacobianHW3(q)

    # Reduce Jacobian
    J_reduce = J[:3, :3]

    # Calculate value to predict Singularity 
    m = np.linalg.det(J_reduce)

    # Check Singularity
    if m < e :
        # Singularity
        flag = True
    else:
        # Not Singularity
        flag = False
    
    return flag
#==============================================================================================================#

#=============================================<คำตอบข้อ 3>======================================================#
#code here
def computeEffortHW3(q:list[float], w:list[float])->list[float]:

    # Call funtion endEffectorJacobian by configuration q
    J = endEffectorJacobianHW3(q)

    # Reduce Jacobian
    J_reduce = J[:3, :3]

    # Reduce Wrench for Linear Fort
    w = np.array(w).reshape(6,1)
    w_f = w[3:, :]

    # Calculate effort from joint
    tau = np.dot(np.transpose(J_reduce),w_f)
    return tau
#==============================================================================================================#