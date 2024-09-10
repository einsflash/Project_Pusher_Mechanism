import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

# 已知点和边长 / Given points and lengths
B = np.array([1, 2])
D = np.array([4, 5])
BC = 2
CD = 3

def calculate_C_Position(B, D, BC, CD):
    """
    计算三角形BCD中两个可能的C点的坐标，并根据叉乘结果选择一个。
    Calculate the coordinates of the two possible C points in triangle BCD
    and select one based on the cross product result.
    """

    # 计算向量 BD / Calculate vector BD
    BD_vector = D - B
    BD_length = np.linalg.norm(BD_vector)
    BD_unit_vector = BD_vector / BD_length

    # 计算垂直于 BD 的法向量 / Calculate the normal vector perpendicular to BD
    normal_vector_toBD = np.array([-BD_unit_vector[1], BD_unit_vector[0]])

    # 三角形的边长 / Triangle side lengths
    a = BC
    b = CD
    c = BD_length

    # 使用海伦公式计算三角形的面积，然后用面积公式计算高度 h
    # Use Heron's formula to calculate the area of the triangle, 
    # then use the area to calculate the height h
    s = (a + b + c) / 2
    area = np.sqrt(s * (s - a) * (s - b) * (s - c))
    h = 2 * area / c

    # 计算从点 C 到 BD 的距离（沿着 BD 方向的投影长度）
    # Calculate the distance from point C to BD (the projection length along BD direction)
    projection_length = np.sqrt(BC ** 2 - h ** 2)

    # 计算两个可能的 C 点位置 / Calculate the two possible positions of point C
    C1 = B + projection_length * BD_unit_vector + h * normal_vector_toBD
    C2 = B + projection_length * BD_unit_vector - h * normal_vector_toBD

    # 选择 C1 和 C2 之间的正确点 / Choose the correct point between C1 and C2
    BC1_vector = C1 - B
    cross_product_1 = BD_vector[0] * BC1_vector[1] - BD_vector[1] * BC1_vector[0]

    # 根据叉乘的结果选择正确的 C 点 / Select the correct C point based on the result of the cross product
    if cross_product_1 > 0:
        C_positive, C_negative = C1, C2
    else:
        C_positive, C_negative = C2, C1

    # 返回结果，确保 C1 始终为正 / Return the result, ensuring C1 is always positive
    return C_positive, C_negative

# 计算两个可能的C点 / Calculate the two possible C points
C1, C2 = calculate_C_Position(B, D, BC, CD)

# 可视化三角形 BCD 和两个可能的 C 点
# Visualize triangle BCD and the two possible C points
plt.figure(figsize=(6, 6))
plt.plot([B[0], D[0]], [B[1], D[1]], 'k-', label='BD')
plt.plot([B[0], C1[0]], [B[1], C1[1]], 'r--', label='BC1 (Positive Cross Product)')
plt.plot([D[0], C1[0]], [D[1], C1[1]], 'r--', label='DC1')

plt.plot([B[0], C2[0]], [B[1], C2[1]], 'b--', label='BC2 (Negative Cross Product)')
plt.plot([D[0], C2[0]], [D[1], C2[1]], 'b--', label='DC2')

# 标记点 B, D, C1 和 C2 / Mark points B, D, C1, and C2
plt.scatter([B[0], D[0], C1[0], C2[0]], [B[1], D[1], C1[1], C2[1]], color=['black', 'black', 'red', 'blue'])
plt.text(B[0], B[1], 'B', fontsize=12, ha='right')
plt.text(D[0], D[1], 'D', fontsize=12, ha='right')
plt.text(C1[0], C1[1], 'C1', fontsize=12, ha='right', color='red')
plt.text(C2[0], C2[1], 'C2', fontsize=12, ha='right', color='blue')

plt.title('Visualization of Triangle BCD with Two Possible Positions of C')
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()
plt.show()