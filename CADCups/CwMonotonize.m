%to make a sorted vector strictly monotone by epsilon-perturbation
%the input x maybe singular at the beginning but not at the end

function y = CwMonotonize(x, epsilon)

assert( all( x(2:end) -x(1:(end-1)) >= -0.025 ) );

y = x;
for i = 2 : length(x)
    y(i) = max( y(i-1) + epsilon, x(i) );
end

end
