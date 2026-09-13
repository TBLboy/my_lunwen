load("A.mat")
load("B.mat")
load("C.mat")
load("train_data.mat")
load("test_data.mat")
q_scaler = train_data.q_scaler;
q_dc = train_data.q_dc;
u_scaler = train_data.u_scaler;
u_dc = train_data.u_dc;
q_val = test_data.x_test.*q_scaler+q_dc;
tau_val = test_data.u_test.*u_scaler+u_dc;
q_union=q_val;
tau_union=tau_val;

q_pre=q_union(1,:);
q_current=q_union(1,:);
for i=1:size(tau_union,1)-1
    q_lifted=lift_function(q_current);
    q_lifted=(A*q_lifted'+B*tau_union(i,:)')';
    q_current=(C*q_lifted')';
    q_pre=[q_pre;q_current];
end


loss=abs(q_pre-q_val);
loss_sum=zeros(1,6);
for i=1:6
    for j=1:size(loss,1)
        loss_sum(i)=loss_sum(i)+loss(j,i);
    end
end
loss_sum=loss_sum/size(loss,1);

number = 100
t=1:number;
t = t*0.02;
subplot(2,3,1)
plot(t,q_val(1:number,1),'r',t,q_pre(1:number,1),'b');
subplot(2,3,2)
plot(t,q_val(1:number,3),'r',t,q_pre(1:number,3),'b');
subplot(2,3,3)
plot(t,q_val(1:number,5),'r',t,q_pre(1:number,5),'b');
subplot(2,3,4)
plot(t,q_val(1:number,2),'r',t,q_pre(1:number,2),'b');
subplot(2,3,5)
plot(t,q_val(1:number,4),'r',t,q_pre(1:number,4),'b');
subplot(2,3,6)
plot(t,q_val(1:number,6),'r',t,q_pre(1:number,6),'b');