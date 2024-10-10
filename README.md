# FRA333_HW3_6512_6550

จากโจทย์เป็นการสร้างโปรแกรมสำหรับใช้ในการหาค่า

-  EndEffector Jacobian
-  การเกิด Singularity
-  Effort ของแต่ละ Joint

ภายใต้ Joint Configuration และ Wrench ที่มากระทำกับจุดกึ่งกลางของเฟรม $F_e$ ที่สามารถกำหนดได้

**โดยแขนกลมีลักษณะดังนี้**
![Robot_arm](picture/pic1.png)

# Function Detail
ในโปรแกรมได้แบ่งการทำงานออกเป็น 3 function โดยแต่ละ function มีจุดประสงค์การใช้งานที่แตกต่างกัน

- endEffectorJacobianHW3 : function สำหรับการหา Jacobian ของแขนกลภายใต้ Joint Configuration ที่กำหนด
- checkSingularityHW3 : function สำหรับการเช็คว่าจาก Joint Configuration ที่กำหนดเกิด Singularity ขึ้นหรือไม่
- computeEffortHW3 : function สำหรับการหา Jacobian ของแขนกลภายใต้ Joint Configuration และ Wrench ที่มากระทำกับจุดกึ่งกลางของเฟรม $F_e$ ที่กำหนด

## endEffectorJacobianHW3


## checkSingularityHW3

## computeEffortHW3

# Demo

# How to use

# Referent

- [The Ultimate Guide to Jacobian Matrices for Robotics](https://automaticaddison.com/the-ultimate-guide-to-jacobian-matrices-for-robotics/)

