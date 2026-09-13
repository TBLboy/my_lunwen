function snapshotPairs=get_snapShorts(data)
 before.t = data.t(1:end-1 );
 before.q = data.q(1:end-1,:);
 after.t = data.t(2:end);
 after.q = data.q(2:end,:);
 u = data.u( 1:end-1 , : );    % input that happens between before.zeta and after.zeta

 % remove pairs that fall at the boundary between sim/exp trials
 goodpts = find( before.t < after.t );
 before.q = before.q(goodpts,:);
 after.q = after.q(goodpts,:);
 u = u(goodpts,:);

 % set the number of snapshot pairs to be taken
 num_max = size( before.q , 1 ) - 1; % maximum number of snapshot pairs

 % randomly select num snapshot pairs
 total = num_max;
 s = RandStream('mlfg6331_64');
 index = datasample(s , 1:total, num_max , 'Replace' , false);
 
 snapshotPairs.alpha = before.q( index , : );
 snapshotPairs.beta = after.q( index , : );
 snapshotPairs.u = u( index , : );

 
end