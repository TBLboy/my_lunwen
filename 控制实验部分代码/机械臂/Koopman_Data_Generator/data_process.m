%% --- 1. 用户设置 ---

% 请在这里设置您要合并的数据文件总数 'n'
n = 6;  % 示例：假设您工作区中有 data1, data2, data3, data4, data5


%% --- 2. 脚本主程序 ---
% 假设 data1, data2, ..., datan 已经存在于您的工作区中

fprintf('开始合并 %d 个数据文件...\n', n);

% 按照您的要求，初始化一个空的 'data' 结构体
data.q = [];
data.u = []; % 注意：我们将把 'tau' 合并到 'u'
data.t = [];

% 循环处理从 1 到 n 的所有 data 变量
for i = 1:n
    % 构造当前循环要处理的变量名 (例如 'data1', 'data2')
    current_var_name = sprintf('data%d', i);

    % 检查这个变量是否存在于工作区
    if exist(current_var_name, 'var')
        
        % -----------------------------------------------------------------
        % 使用 eval() 从工作区动态获取变量
        % 这是基于您的要求（变量已在工作区）所必需的
        current_data = eval(current_var_name);
        % -----------------------------------------------------------------
        
        % 检查所需的字段 (q, tau, t) 是否存在
        if isfield(current_data, 'q') && isfield(current_data, 'tau') && isfield(current_data, 't')
            
            % 3. 垂直拼接（追加）数据
            data.q = [data.q; current_data.q];
            data.t = [data.t; current_data.t];
            
            % *** 关键步骤：将 dataX.tau 合并到 data.u ***
            data.u = [data.u; current_data.tau];
            
            fprintf('  [成功] 已合并 %s\n', current_var_name);
        else
            warning('  [跳过] 变量 %s 缺少 q, tau, 或 t 字段。', current_var_name);
        end
    else
        warning('  [跳过] 变量 %s 在工作区中未找到。', current_var_name);
    end
end

fprintf('--- 合并完成 ---\n');
[q_scaler,q_dc,q_union]=Data_scale(data.q);
[u_scaler,u_dc,u_union]=Data_scale(data.u);
data.q=q_union;
data.u=u_union;
snap = get_snapShorts(data);
train_data.x=snap.alpha;
train_data.y=snap.beta;
train_data.u=snap.u;
train_data.q_scaler=q_scaler;
train_data.q_dc=q_dc;
train_data.u_scaler=u_scaler;
train_data.u_dc=u_dc;
save('train_data','train_data')