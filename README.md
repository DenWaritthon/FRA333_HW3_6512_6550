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
- computeEffortHW3 : function สำหรับการหา Effort ของแต่ละ Joint ของแขนกลภายใต้ Joint Configuration และ Wrench ที่มากระทำกับจุดกึ่งกลางของเฟรม $F_e$ ที่กำหนด

## endEffectorJacobianHW3

ในการหา EndEffector Jacobian นั้นมีการกำหนด
- Input : q[3] ซึ่งเป็น array ของ Joint Configuration ที่กำหนด
- Output : $J^{6x6}$ ซี่งเป็น EndEffector Jacobian

โดยในการหา EndEffector Jacobian นั้นมาจากสมการ \
*Joint ทำการหมทุนรอบแกน z

$$ J_e(q)_{6\times3} = 
    \begin{pmatrix}
        Jv_e(q)_{3\times3} \\
        Jw_e(q)_{3\times3}
    \end{pmatrix}
$$

โดย

$$ Jv_e(q)_{3\times3} = 
    \begin{bmatrix}

        R^0_1
        \begin{bmatrix}
            0 \\
            0 \\
            1
        \end{bmatrix}
        \times
        (P^0_e - P^0_1) &

        R^0_2
            \begin{bmatrix}
            0 \\
            0 \\
            1
        \end{bmatrix}
        \times
        (P^0_e - P^0_2) &

        R^0_3
        \begin{bmatrix}
            0 \\
            0 \\
            1
        \end{bmatrix}
        \times
        (P^0_e - P^0_3)

    \end{bmatrix}
$$

และ

$$ Jw_e(q)_{3\times3} = 
    \begin{bmatrix}

        R^0_1
        \begin{bmatrix}
            0 \\
            0 \\
            1
        \end{bmatrix} &

        R^0_2
        \begin{bmatrix}
            0 \\
            0 \\
            1
        \end{bmatrix} &

        R^0_3
        \begin{bmatrix}
            0 \\
            0 \\
            1
        \end{bmatrix}

    \end{bmatrix}
$$

**เนื่องจากแขนกลมีแค่ 3 DoF ทำให้สามารถควบคุมได้แค่ linear velocity เท่านั้นทำให้สามารถลดรูปของ  Jacobian ได้เป็น**

$$ J_{reduce}(q)_{3\times3} = Jv(q)_{3\times3} $$


## checkSingularityHW3

ในการเช็คว่าจาก Joint Configuration ที่กำหนดเกิด Singularity ขึ้นหรือไม่นั้นมีการกำหนด
- Input : q[3] ซึ่งเป็น array ของ Joint Configuration ที่กำหนด
- Output : flang 
  - เป็น True เมื่ออยู่ใกล้สภาวะ Singularity 
  - เป็น False เมื่ออยู่ในสภาวะปกติ

โดยในเช็คว่าเกิด Singularity ไหมนั้นมีการใช้ค่า Manipulability(m) ของแขนกลในการนำมาเปรียบเทียบกับค่า $\varepsilon$ ที่กำหนด

โดย
$$ \varepsilon = 0.0001 $$

และ
$$ m = \det(J_{reduce}) $$

ซึ่งแขนกลจะอยู่ใกล้สภาวะ Singularity ก็ต่อเมื่อ

$$ m < \varepsilon $$


## computeEffortHW3

ในการหา Effort ของแต่ละ Joint นั้นมีการกำหนด
- Input : q[3] ซึ่งเป็น array ของ Joint Configuration ที่กำหนด
- Input : w[6] ซึ่งเป็น array ของ Wrench ที่มากระทำกับจุดกึ่งกลางของเฟรม $F_e$ ที่กำหนด
- Output : $\tau^{3x1}$ ซี่งเป็น Effort ของแต่ละ Joint

โดย Wrench คือ
$$
W_{6\times1} = 
    \begin{bmatrix}
        moment(n^e)_{3\times1} \\
        force(f^e)_{3\times1} \\
    \end{bmatrix}
$$
**เนื่องจากแขนกลมีแค่ 3 DoF ทำให้สามารถควบคุมได้แค่ force เท่านั้นทำให้สามารถลดรูปของ wrench ได้เป็น**

$$ W_{3\times1} = force(f^e)_{3\times1} $$

โดยในการหา Effort ของแต่ละ Joint นั้นมาจากสมการ
$$ \tau_{3x1} = J_{reduce}^T(q)W $$

# Demo

# How to use

# Referent

- [The Ultimate Guide to Jacobian Matrices for Robotics](https://automaticaddison.com/the-ultimate-guide-to-jacobian-matrices-for-robotics/)

