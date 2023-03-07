using CorrelationFunctions.Directional
using StatsBase
function vectorize(str_args)
    filename = str_args[1]
    method = str_args[2]
    dim = parse(Int64, str_args[3])
    normalize = parse(Int64, str_args[4])
    data = Array{UInt8, 3}(undef, dim, dim, dim)
    open(filename) do io read!(io, data) end
    if (method == "c2")
        n = count(i->(i== 0), data)
        if (n == 0)
            res = [[NaN], [NaN], [NaN]]
            return res
        end
        v = c2(data, 0)
        if (normalize == 1)            
            p = n/dim/dim/dim
            vx1 = [(elem - p*p)/p/(1-p) for elem in v[:x]]
            vy1 = [(elem - p*p)/p/(1-p) for elem in v[:y]]
            vz1 = [(elem - p*p)/p/(1-p) for elem in v[:z]]
            res = [vx1, vy1, vz1]
        else
            res = [v[:x], v[:y], v[:z]]
        end        
    elseif (method == "s2")
        v = s2(data, 0)
        if (normalize == 1)
            n = count(i->(i== 0), data)
            p = n/dim/dim/dim
            vx1 = [(elem - p*p)/p/(1-p) for elem in v[:x]]
            vy1 = [(elem - p*p)/p/(1-p) for elem in v[:y]]
            vz1 = [(elem - p*p)/p/(1-p) for elem in v[:z]]
            res = [vx1, vy1, vz1]
        else
            res = [v[:x], v[:y], v[:z]]
        end
    elseif (method == "l2")
        v = l2(data, 0)
        if (normalize == 1)
            res = [v[:x]/v[:x][1], v[:y]/v[:y][1], v[:z]/v[:z][1]]
        else
            res = [v[:x], v[:y], v[:z]]
        end
    elseif (method == "ss")
        v = surfsurf(data, 0)
        if (normalize == 1)
            res = [v[:x]/v[:x][1], v[:y]/v[:y][1], v[:z]/v[:z][1]]
        else
            res = [v[:x], v[:y], v[:z]]
        end
    else
        throw(DomainError(method, "unknown method"))
    end
    return res
end
