clear;clc;
load('train_data.mat')
q_scaler =  train_data.q_scaler;
q_dc = train_data.q_dc;
u_scaler = train_data.u_scaler;
u_dc = train_data.u_dc;
n = 6;
X = train_data.x;
Y = train_data.y;
U = train_data.u;

X_lifted = lift_function(X);
Y_lifted = lift_function(Y);
X_extended = [X_lifted,U];
Y_extended = [Y_lifted,U];

K = (X_extended'*X_extended)\(X_extended'*Y_lifted);

K=K';
A=K(1:size(X_lifted,2),1:size(X_lifted,2));
B=K(1:size(X_lifted,2),size(X_lifted,2)+1:end);
C=[eye(n),zeros(n,size(X_lifted,2)-n)];
save('A.mat',"A")
save('B.mat',"B")
save('C.mat','C')