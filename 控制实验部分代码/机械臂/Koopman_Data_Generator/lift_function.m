function y = lift_function_augmented(q)
% 从输入矩阵中分离状态
% q 是一个 N x 6 矩阵, N 是样本数
q1=q(:,1);
dq1=q(:,2);
q2=q(:,3);
dq2=q(:,4);
q3=q(:,5);
dq3=q(:,6);

% --- 原始基函数 (a1, a2, a3, a4, a6) ---
c1=cos(q1); c2=cos(q2); c3=cos(q3);
s1=sin(q1); s2=sin(q2); s3=sin(q3);

% a1: 状态 (States) + 偏置 (Bias)
a1=[q1, dq1, q2, dq2, q3, dq3, ones(size(q1,1),1)];

% a2: 基础三角函数 (Basic Trig)
a2=[s1, c1, s2, c2, s3, c3];

% a3: 基础三角函数的二次组合 (Quadratic Trig)
a3=[s2.^2, s3.^2, c2.^2, c3.^2, c2.*c3, s2.*s3, c2.*s3, s2.*c3];

% a4: 基础速度-角度耦合 (Basic Velocity-Angle Coupling)
a4=[dq1.*s2, dq2.*s2, dq3.*s2, dq1.*s3, dq2.*s3, dq3.*s3, dq1.*sin(q2+q3), dq2.*sin(q2+q3), dq3.*sin(q2+q3)];

% a5: (已移除/注释) 基于q1的耦合项，对于动力学可能不是必需的
% a5=[s1.*c2, c1.*s2, s1.*c2.*c3, s1.*s2.*s3, c1.*s2.*s3, c1.*c2.*c3];

% a6: 状态的二次多项式 (Quadratic Polynomials)
a6=[q1.^2, q2.^2, q3.^2, dq1.^2, dq2.^2, dq3.^2, ...
    q1.*q2, q1.*q3, q1.*dq1, q1.*dq2, q1.*dq3, ...
    q2.*q3, q2.*dq1, q2.*dq2, q2.*dq3, ...
    q3.*dq1, q3.*dq2, q3.*dq3, ...
    dq1.*dq2, dq1.*dq3, dq2.*dq3];

% --- 增补的基函数 (a7, a8, a9) ---

% 辅助变量 (Helpers for EOM terms)
c2p3 = cos(q2+q3); % cos(q2+q3)
s2p3 = sin(q2+q3); % sin(q2+q3)
s2q2 = sin(2*q2);  % sin(2*q2)
s2q2p3 = sin(2*q2+q3); % sin(2*q2+q3)
s2q2p2q3 = sin(2*q2+2*q3); % sin(2*q2+2*q3)
c2s2p3 = c2.*s2p3; % cos(q2)*sin(q2+q3)

% a7: 关键动力学项 (Key EOM Trig Terms)
% (来自 G, H, C 矩阵的精确非线性项)
a7 = [c2p3, s2p3, c2.*c2p3, c2p3.^2, s2q2, s2q2p3, s2q2p2q3, c2s2p3];

% a8: 关键的速度-角度耦合 (Key Coriolis/Centrifugal Terms)
% (C矩阵元素 * 速度项 的示例)
a8 = [s3.*dq1.*dq2, s3.*dq1.*dq3, s3.*dq2.*dq3, s3.*dq3.^2, ...
      s2q2.*dq1.*dq2, s2q2.*dq1.*dq3, s2q2.*dq2.*dq3];

% a9: 三次多项式 (Cubic Polynomials) - (示例)
% (用于通用逼近)
a9 = [q2.^3, q3.^3, dq1.^3, dq2.^3, dq3.^3, ...
      dq1.*dq2.*dq3, q2.*dq2.^2, q3.*dq3.^2];

% --- 最终组合 ---
% 组合所有你认为有用的基函数
% 注意：维度会非常高，可能需要特征选择或正则化(Regularization)
y = [a1, a2, a3, a4, a6, a7, a8, a9];
end