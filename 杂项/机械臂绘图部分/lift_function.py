import numpy as np


def lift_function(q):
    """
    增强版升维函数 (Feature Library) - 针对 Robot.m 优化

    修改说明:
    1. 清理: 移除了人为噪声组 (a14, a16, a17, a18)。
    2. 增强: 新增 a22 组，专门针对 robot.m 中关节2的科氏力耦合项进行物理建模。

    输入: q - (m x 6) 数组，每行为 [q1, dq1, q2, dq2, q3, dq3]
    输出: y - (m x D) 特征矩阵
    """
    # --- 1. 提取状态 ---
    q1 = q[:, 0]
    dq1 = q[:, 1]
    q2 = q[:, 2]
    dq2 = q[:, 3]
    q3 = q[:, 4]
    dq3 = q[:, 5]

    m = q.shape[0]
    ones_vec = np.ones(m)

    # --- 2. 基础项 (a1: 7 terms) ---
    a1 = np.column_stack([q1, dq1, q2, dq2, q3, dq3, ones_vec])

    # --- 3. 三角函数辅助变量 (a2, a3) ---
    c1 = np.cos(q1)
    s1 = np.sin(q1)
    c2 = np.cos(q2)
    s2 = np.sin(q2)
    c3 = np.cos(q3)
    s3 = np.sin(q3)
    c2p3 = np.cos(q2 + q3)
    s2p3 = np.sin(q2 + q3)
    c2m3 = np.cos(q2 - q3)
    s2m3 = np.sin(q2 - q3)

    # a2: 16 terms
    a2 = np.column_stack([
        s1, c1, s2, c2, s3, c3, c2p3, s2p3, c2m3, s2m3,
        c2 * s2, c3 * s3, c2p3 * s2p3, s2 * s3, c2 * c3, s2 * s2p3
    ])

    # 更多三角函数
    c2q2 = np.cos(2 * q2)
    s2q2 = np.sin(2 * q2)
    c2q3 = np.cos(2 * q3)
    s2q3 = np.sin(2 * q3)
    c3q2 = np.cos(3 * q2)
    s3q2 = np.sin(3 * q2)
    c3q3 = np.cos(3 * q3)
    s3q3 = np.sin(3 * q3)
    c2q2p3 = np.cos(2 * q2 + q3)
    s2q2p3 = np.sin(2 * q2 + q3)
    c2q2m3 = np.cos(2 * q2 - q3)
    s2q2m3 = np.sin(2 * q2 - q3)
    cq2p2q3 = np.cos(q2 + 2 * q3)
    sq2p2q3 = np.sin(q2 + 2 * q3)
    c2q2p2q3 = np.cos(2 * q2 + 2 * q3)
    s2q2p2q3 = np.sin(2 * q2 + 2 * q3)

    # a3: 24 terms
    a3 = np.column_stack([
        c2q2, s2q2, c2q3, s2q3, c3q2, s3q2, c3q3, s3q3,
        c2q2p3, s2q2p3, c2q2m3, s2q2m3, cq2p2q3, sq2p2q3,
        c2q2p2q3, s2q2p2q3,
        np.cos(q1 + q2), np.sin(q1 + q2), np.cos(q1 + q3), np.sin(q1 + q3),
        np.cos(q1 + q2 + q3), np.sin(q1 + q2 + q3),
        np.cos(2 * (q2 + q3)), np.sin(2 * (q2 + q3))
    ])

    # --- 4. 物理特征组 (a4-a13) ---
    # a4: 22 terms
    a4 = np.column_stack([
        c2 ** 2, c3 ** 2, c2p3 ** 2, c2m3 ** 2,
        c2 * c3, c2 * c2p3, c3 * c2p3, c2 * c2m3,
        s2 ** 2, s3 ** 2, s2p3 ** 2, s2m3 ** 2,
        s2 * s3, s2 * s2p3, c2q2 * c2q3,
        (c2 ** 2) * (c2p3 ** 2), c2 ** 3, c2p3 ** 3, c3 ** 3,
        c2 * c3 ** 2, c2p3 * c3 ** 2, c3 ** 4
    ])

    # a5: 26 terms
    a5 = np.column_stack([
        s2q2, s2q2p3, np.sin(2 * q2 + 2 * q3), s2q2m3, np.sin(2 * (q2 - q3)),
        c2 * s2, c3 * s3, c2p3 * s2p3, c2m3 * s2m3,
        c2 * s2p3, s2 * c2p3, c2 * s3, s3 * c2p3,
        c2 ** 2 * c2p3, c2 * c2p3 ** 2, c2 ** 2 * c3, c3 ** 2 * c2p3,
        c2 * c3 * c2p3, s2 * s3 * s2p3,
        c2q2 * c3, c2 * c2q3, s2q2 * s3, s3 * c2q3, s2q3 * c2,
        np.sin(q2) * np.cos(q2) * np.cos(q3), np.sin(q3) * np.cos(q2 + q3)
    ])

    # a6: 27 terms
    a6 = np.column_stack([
        dq1 * c2, dq1 * s2, dq1 * c3, dq1 * s3,
        dq1 * c2p3, dq1 * s2p3, dq1 * c2m3, dq1 * s2m3,
        dq1 * c2 ** 2, dq1 * c2p3 ** 2, dq1 * c2 * c2p3, dq1 * c2 * c3,
        dq1 * c2 * s2, dq1 * s2q2, dq1 * s2q2p3, dq1 * s3,
        dq1 * c2q2, dq1 * c2q3, dq1 * s2q3, dq1 * c3 * s3,
        dq1 ** 2 * c2, dq1 ** 2 * c2p3, dq1 ** 2 * s2, dq1 ** 2 * c3,
        dq1 * c3 ** 2, dq1 * s3 ** 2, dq1 * c2q3
    ])

    # a7: 35 terms
    a7 = np.column_stack([
        dq1 * s2, dq2 * s2, dq3 * s2, dq1 * s3, dq2 * s3, dq3 * s3,
        dq1 * s2p3, dq2 * s2p3, dq3 * s2p3, dq1 * s2m3, dq2 * s2m3, dq3 * s2m3,
        dq1 * c2, dq2 * c2, dq3 * c2, dq1 * c3, dq2 * c3, dq3 * c3,
        dq2 * s2q2, dq3 * s2q3, dq2 * c2q2, dq3 * c2q3,
        dq1 * s2q2p3, dq2 * s2q2p3, dq3 * s2q3, dq3 * c3q3,
        dq2 ** 2 * s2, dq3 ** 2 * s3, dq2 ** 2 * c2, dq3 ** 2 * c3,
        dq1 * dq2 * s2, dq2 * dq3 * s3, dq3 * s3 ** 2, dq3 * c3 ** 2,
        dq2 * c2 * c3, dq3 * s2 * s3
    ])

    # a8: 29 terms
    a8 = np.column_stack([
        dq1 * dq2, dq1 * dq3, dq2 * dq3,
        s3 * dq1 * dq2, s3 * dq2 * dq3, s3 * dq1 * dq3,
        s2 * dq1 * dq2, s2 * dq2 * dq3, s2 * dq1 * dq3,
        s2q2 * dq1 * dq2, s2q2 * dq2 * dq3, s2q3 * dq2 * dq3,
        c2 * dq1 * dq2, c3 * dq2 * dq3, c2p3 * dq1 * dq3,
        dq1 * dq2 * dq3, dq1 * dq2 * s2p3, dq2 * dq3 * c3,
        (dq1 * dq2) * c2 ** 2, (dq2 * dq3) * c3 ** 2,
        (dq1 * dq3) * c2p3, dq1 * dq2 * c2 * c3,
        dq2 * dq3 * s2 * s3, (dq1 * dq2 * dq3) * s3,
        c3 * dq1 * dq3, s3 * dq1 * dq3 ** 2, dq2 * dq3 * c3 ** 2,
        dq2 * dq3 * s3 ** 2, c2q3 * dq2 * dq3
    ])

    # a9: 30 terms
    a9 = np.column_stack([
        dq1 ** 2, dq2 ** 2, dq3 ** 2,
        dq1 ** 2 * c2, dq1 ** 2 * s2, dq2 ** 2 * c3, dq2 ** 2 * s3, dq3 ** 2 * c3, dq3 ** 2 * s3,
        s3 * dq3 ** 2, s3 * dq2 ** 2, s2 * dq1 ** 2,
        dq1 ** 3, dq2 ** 3, dq3 ** 3,
        dq1 ** 2 * dq2, dq1 ** 2 * dq3, dq2 ** 2 * dq3,
        np.sqrt(np.abs(dq2)), np.sqrt(np.abs(dq3)),
        np.sign(dq2) * dq2 ** 2, np.sign(dq3) * dq3 ** 2,
        dq2 ** 2 * c2 ** 2, dq3 ** 2 * c3 ** 2,
        dq3 ** 2 * s3 ** 2, dq3 ** 2 * c2q3, dq3 ** 3 * s3, dq3 ** 3 * c3,
        np.abs(dq3) ** 1.5, dq3 ** 2 * np.sign(dq3)
    ])

    # a10: 22 terms
    a10 = np.column_stack([
        q1 ** 2, q2 ** 2, q3 ** 2, q1 * q2, q1 * q3, q2 * q3,
        q1 * dq1, q2 * dq2, q3 * dq3, q1 * dq2, q1 * dq3, q2 * dq1,
        q2 ** 3, q3 ** 3, q2 * q3 ** 2, q3 ** 4,
        q2 ** 2 * dq2, q3 ** 2 * dq3, (q2 + q3) * dq2, q3 * dq2,
        q3 ** 2 * dq2, q3 ** 3 * dq3
    ])

    # a11: 21 terms
    a11 = np.column_stack([
        c2, c2p3, c3, c2 + c2p3, c2 - c2p3,
                      q2 * c2, q3 * c2p3, q3 * c3,
                      dq2 * c2, dq3 * c2p3, c2 * c2p3, s2 * s2p3,
                      dq2 * s2, dq3 * s3, (c2 + c2p3) ** 2,
                      q3 * s3, q3 ** 2 * c3, dq3 * c3, dq3 * s2p3,
                      c3 * (c2 + c2p3), s3 * (s2 + s2p3)
    ])

    # a12: 22 terms
    sd1 = np.sign(dq1)
    sd2 = np.sign(dq2)
    sd3 = np.sign(dq3)
    a12 = np.column_stack([
        sd1 * dq1, sd2 * dq2, sd3 * dq3,
        sd1 * np.abs(dq1), sd2 * np.abs(dq2), sd3 * np.abs(dq3),
        dq1 * np.abs(dq1), dq2 * np.abs(dq2), dq3 * np.abs(dq3),
        np.tanh(10 * dq1), np.tanh(10 * dq2), np.tanh(10 * dq3),
        dq1 / (1 + np.abs(dq1)), dq2 / (1 + np.abs(dq2)), dq3 / (1 + np.abs(dq3)),
        np.maximum(dq2, 0), np.maximum(dq3, 0), np.minimum(dq2, 0), np.minimum(dq3, 0),
        np.tanh(5 * dq3), np.tanh(20 * dq3), sd3 * np.abs(dq3) ** 1.5
    ])

    # a13: 23 terms
    a13 = np.column_stack([
        dq1 * c2 ** 2, dq1 * c2p3 ** 2, dq1 * c2 * c2p3, dq1 * c3 ** 2,
        dq2 * c3, dq2 * c3 ** 2, dq3 * c3, dq3 * c3 ** 2,
        dq2 * (c2 + c2p3), dq3 * (c2 + c2p3),
        sd1 * dq1 * c2, sd2 * dq2 * c3, sd3 * dq3 * c3,
        dq1 * dq2 * c2, dq2 * dq3 * c3,
        np.abs(dq2) * c2, np.abs(dq3) * c3, dq2 * np.abs(dq2) * s2,
        dq3 * c3 ** 3, dq3 * s3 ** 2, np.abs(dq3) * s3,
        dq3 * (c2 + c2p3), sd3 * dq3 * s3
    ])

    # 注: a14 (噪声) 已移除

    # a15: 23 terms
    a15 = np.column_stack([
        q2 * dq2 ** 2, q3 * dq3 ** 2, q2 * dq3 ** 2,
        dq1 ** 2 * dq2, dq1 ** 2 * dq3, dq2 * dq3 ** 2, dq1 * dq2 ** 2,
        q2 * c2 * dq2, q3 * c3 * dq3, q2 * s2 * dq2,
        c2 * dq1 * dq2, c3 * dq2 * dq3, s2 * dq1 ** 2,
        dq1 * dq2 * s2p3, dq1 * dq3 * c2p3,
        q2 * dq2 * c2, q3 * dq3 * c3, dq2 ** 2 * s2q2,
        q3 * dq3 ** 2 * c3, q3 * dq3 ** 2 * s3, q3 ** 2 * dq3 * c3,
        dq3 ** 2 * c3, dq1 * dq3 ** 2
    ])

    # 注: a16, a17, a18 (噪声) 已移除

    # a19: 30 terms (物理耦合)
    trig_basis_c = np.column_stack([s3, s2q2, s2q2p2q3, s2q2p3, c2 * s2p3])
    vel_basis_c = np.column_stack([dq1 ** 2, dq2 ** 2, dq3 ** 2, dq1 * dq2, dq1 * dq3, dq2 * dq3])

    a19_list = []
    for i in range(trig_basis_c.shape[1]):
        for j in range(vel_basis_c.shape[1]):
            a19_list.append(trig_basis_c[:, i] * vel_basis_c[:, j])
    a19 = np.column_stack(a19_list)

    # a20: 100 terms (高阶多项式)
    a20_g1 = np.column_stack([q2 ** 4, q3 ** 4, dq1 ** 4, dq2 ** 4, dq3 ** 4])
    a20_g2 = np.column_stack([q2 ** 5, q3 ** 5, dq1 ** 5, dq2 ** 5, dq3 ** 5])
    a20_g3 = np.column_stack([q2 ** 3 * dq1, q2 ** 3 * dq2, q2 ** 3 * dq3,
                              q3 ** 3 * dq1, q3 ** 3 * dq2, q3 ** 3 * dq3])
    a20_g4 = np.column_stack([q2 * dq1 ** 3, q2 * dq2 ** 3, q2 * dq3 ** 3,
                              q3 * dq1 ** 3, q3 * dq2 ** 3, q3 * dq3 ** 3])
    a20_g5 = np.column_stack([q2 ** 2 * dq1 ** 2, q2 ** 2 * dq2 ** 2, q2 ** 2 * dq3 ** 2,
                              q3 ** 2 * dq1 ** 2, q3 ** 2 * dq2 ** 2, q3 ** 2 * dq3 ** 2])
    a20_g6 = np.column_stack([
        dq1 ** 3 * dq2, dq1 ** 3 * dq3, dq2 ** 3 * dq1, dq2 ** 3 * dq3, dq3 ** 3 * dq1, dq3 ** 3 * dq2,
        dq1 ** 2 * dq2 ** 2, dq1 ** 2 * dq3 ** 2, dq2 ** 2 * dq3 ** 2, dq1 * dq2 * dq3 ** 2
    ])
    a20_g7 = np.column_stack([
        dq1 ** 4 * dq2, dq1 ** 4 * dq3, dq2 ** 4 * dq1, dq2 ** 4 * dq3, dq3 ** 4 * dq1, dq3 ** 4 * dq2,
        dq1 ** 3 * dq2 ** 2, dq1 ** 2 * dq2 ** 3, dq1 ** 3 * dq3 ** 2,
        dq1 ** 2 * dq3 ** 3, dq2 ** 3 * dq3 ** 2, dq2 ** 2 * dq3 ** 3
    ])
    a20_g8 = np.column_stack([q2 ** 4, q3 ** 4, q2 ** 3 * q3, q2 ** 2 * q3 ** 2, q2 * q3 ** 3])
    a20_g9 = np.column_stack([q2 ** 5, q3 ** 5, q2 ** 4 * q3, q2 ** 3 * q3 ** 2,
                              q2 ** 2 * q3 ** 3, q2 * q3 ** 4])

    trig_basis_simple = np.column_stack([s2, c2, s3, c3, s2p3, c2p3])
    vel_basis_3 = np.column_stack([dq1 ** 3, dq2 ** 3, dq3 ** 3])
    a20_g10_list = []
    for i in range(trig_basis_simple.shape[1]):
        for j in range(vel_basis_3.shape[1]):
            a20_g10_list.append(trig_basis_simple[:, i] * vel_basis_3[:, j])
    a20_g10 = np.column_stack(a20_g10_list)

    trig_basis_simple_sq = np.column_stack([s2 ** 2, c2 ** 2, s3 ** 2, c3 ** 2, s2p3 ** 2, c2p3 ** 2])
    vel_basis_2 = np.column_stack([dq1 ** 2, dq2 ** 2, dq3 ** 2])
    a20_g11_list = []
    for i in range(trig_basis_simple_sq.shape[1]):
        for j in range(vel_basis_2.shape[1]):
            a20_g11_list.append(trig_basis_simple_sq[:, i] * vel_basis_2[:, j])
    a20_g11 = np.column_stack(a20_g11_list)

    a20 = np.hstack([a20_g1, a20_g2, a20_g3, a20_g4, a20_g5,
                     a20_g6, a20_g7, a20_g8, a20_g9, a20_g10, a20_g11])

    # a21: 90 terms (G, H 物理交叉项)
    g_basis = np.column_stack([c2, c2p3])
    h_basis = np.column_stack([c2 ** 2, c2p3 ** 2, c2 * c2p3, c3, c2 * c3, c2p3 * c3])
    vel_basis_3b = np.column_stack([
        dq1 ** 3, dq2 ** 3, dq3 ** 3, dq1 ** 2 * dq2, dq1 * dq2 ** 2,
        dq1 ** 2 * dq3, dq1 * dq3 ** 2, dq2 ** 2 * dq3, dq2 * dq3 ** 2
    ])
    trig_basis_simple_b = np.column_stack([s2, s3, s2p3])

    a21_list = []
    # G * vel_poly
    for i in range(g_basis.shape[1]):
        for j in range(vel_basis_c.shape[1]):
            a21_list.append(g_basis[:, i] * vel_basis_c[:, j])
    # H * vel_poly
    for i in range(h_basis.shape[1]):
        for j in range(vel_basis_c.shape[1]):
            a21_list.append(h_basis[:, i] * vel_basis_c[:, j])
    # G * vel_poly_cubic
    for i in range(g_basis.shape[1]):
        for j in range(vel_basis_3b.shape[1]):
            a21_list.append(g_basis[:, i] * vel_basis_3b[:, j])
    # H * vel_poly_cubic
    for i in range(3):
        for j in range(3):
            a21_list.append(h_basis[:, i] * vel_basis_3b[:, j])
    # H * G
    for i in range(g_basis.shape[1]):
        for j in range(h_basis.shape[1]):
            a21_list.append(g_basis[:, i] * h_basis[:, j])
    # H * simple_trig
    for i in range(h_basis.shape[1]):
        for j in range(trig_basis_simple_b.shape[1]):
            a21_list.append(h_basis[:, i] * trig_basis_simple_b[:, j])
    a21_array = np.column_stack(a21_list)
    a21 = a21_array[:, :90]

    # --- 8. [新增] a22: Robot.m 专属增强项 ---
    # 针对关节2速度 (dq2) 拟合差的问题进行物理修复
    # 关键点:
    # 1. 关节1对关节2的离心力项: a1 * dq1^2，其中 a1 包含 sin(2*q2+q3) 等项
    # 2. 惯量矩阵逆的调制: H_inv 与 cos(q3) 相关

    # 提取 robot.m 中 a1 的核心角度组合
    term_a1_1 = np.sin(2 * q2)  # 来自 p(2)*cos(x3)*sin(x3)
    term_a1_2 = np.sin(2 * (q2 + q3))  # 来自 p(3)*cos(x3+x5)*sin(x3+x5)
    term_a1_3 = np.sin(2 * q2 + q3)  # 来自 p(4)*sin(2*x3+x5)

    # 提取 robot.m 中 a3 的核心角度
    term_a3 = np.sin(q3)  # 来自 p(4)*sin(x5)

    # 构造精确的力项 (Forces)
    # F1: 关节1运动导致的离心力 (作用于关节2)
    F_centrifugal_2_from_1 = np.column_stack([
        term_a1_1 * dq1 ** 2,
        term_a1_2 * dq1 ** 2,
        term_a1_3 * dq1 ** 2
    ])

    # F2: 关节3运动导致的科氏力 (作用于关节2)
    # 对应 -a3*dq3*dq2 - a3*(dq2+dq3)*dq3
    F_coriolis_2_from_3 = np.column_stack([
        term_a3 * dq2 * dq3,
        term_a3 * dq3 ** 2
    ])

    # 惯量调制 (Inertia Modulation)
    # 因为 acceleration = inv(H) * Forces
    # inv(H) 近似展开依赖于 cos(q3) 的幂次
    modulator = np.cos(q3)

    # 组合增强特征: 原始力 + 经惯量调制后的力
    a22 = np.column_stack([
        F_centrifugal_2_from_1,
        F_coriolis_2_from_3,
        F_centrifugal_2_from_1 * modulator[:, np.newaxis],  # 广播乘法
        F_coriolis_2_from_3 * modulator[:, np.newaxis]
    ])

    # --- 9. 组合所有特征 ---
    y = np.hstack([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10,
                   a11, a12, a13, a15, a19, a20, a21, a22])

    return y