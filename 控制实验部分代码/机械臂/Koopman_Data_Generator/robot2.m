function[sys,xm0,str,ts]=robot2(t,xm,u,flag)

switch flag
case 0
    [sys,xm0,str,ts]=mdlInitializeSizes;
case 1
    sys=mdlDerivatives(t,xm,u);    
case 3
    sys=mdlOutputs(t,xm,u);
case {2,4,9}
    sys=[];
otherwise
    error(['Unhandled flag=',num2str(flag)]);
end

function[sys,xm0,str,ts]=mdlInitializeSizes
global p g
sizes=simsizes;
seed = mod(floor(posixtime(datetime('now')) * 1e6), 2^32); % 确保种子�? 0 �? 2^32-1 之间
rng(seed); % 设置随机数种�?
sizes.NumContStates =0;
sizes.NumDiscStates =6;
sizes.NumOutputs =6;
sizes.NumInputs =3;
sizes.DirFeedthrough =0;
sizes.NumSampleTimes =0;
sys=simsizes(sizes);
xm0=[0 0 0.895 0 -1.35 0];


str=[];
ts=[];

p=[3.7*10^(-3) 7*10^(-3) 8*10^(-3) 0.4*10^(-3) 9.1*10^(-3) 5.2*10^(-3) 0.096 0.145 0.055];
g=9.8;
function sys=mdlDerivatives(t,x,u)
global p g 

h11=p(1)+p(2)*cos(x(3))^2+p(3)*cos(x(3)+x(5))^2+2*p(4)*cos(x(3))*cos(x(3)+x(5));
h22=p(2)+p(3)+2*p(4)*cos(x(5));
h23=p(3)+p(4)*cos(x(5));
h32=h23;
h33=p(3);
H=[h11 0 0;
    0 h22 h23;
    0 h32 h33];
a1=p(2)*cos(x(3))*sin(x(3))+p(3)*cos(x(3)+x(5))*sin(x(3)+x(5))+p(4)*sin(2*x(3)+x(5));
a2=p(3)*cos(x(3)+x(5))*sin(x(3)+x(5))+p(4)*cos(x(3))*sin(x(3)+x(5));
a3=p(4)*sin(x(5));
C=[-(a1*x(4)+a2*x(6)) -a1*x(2) -a2*x(2);
    a1*x(2) -a3*x(6) -a3*(x(4)+x(6));
    a2*x(2) a3*x(4) 0];
b1=p(7);
b2=p(8);
b3=p(9);
B=[b1 0 0;
   0 b2 0;
   0 0 b3];
G=[0;p(5)*g*cos(x(3))+p(6)*g*cos(x(3)+x(5));p(6)*g*cos(x(3)+x(5))];
tolm=u(1:3); 



dqm=[x(2);x(4);x(6)];

S=inv(H)*(tolm-C*dqm-B*dqm-G);
% S=inv(H)*(tolm-C*dqm-G);
sys(1)=x(2);
sys(2)=S(1);
sys(3)=x(4);
sys(4)=S(2);
sys(5)=x(6);
sys(6)=S(3);

function sys = mdlOutputs(t,x,u);
sys(1)=x(1);
sys(2)=x(2);
sys(3)=x(3);
sys(4)=x(4);
sys(5)=x(5);
sys(6)=x(6);






