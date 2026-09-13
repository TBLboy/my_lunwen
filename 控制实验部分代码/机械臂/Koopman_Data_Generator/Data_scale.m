function [scaler,dc,Data_Union]=Data_scale(Data)
Data_max=max(Data);
Data_min=min(Data);
dc=(Data_max+Data_min)./2;
scaler=(Data_max-Data_min)./2;
Data_Union=(Data-dc)./scaler;
end