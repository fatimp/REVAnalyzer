using CorrelationFunctions.Directional
using CorrelationFunctions.Utilities
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
            vx1 = [(elem - p*p)/p/(1-p) for elem in v[DirX()]]
            vy1 = [(elem - p*p)/p/(1-p) for elem in v[DirY()]]
            vz1 = [(elem - p*p)/p/(1-p) for elem in v[DirZ()]]
            res = [vx1, vy1, vz1]
        else
            res = [v[DirX()], v[DirY()], v[DirZ()]]
        end        
    elseif (method == "s2")
        v = s2(data, 0)
        if (normalize == 1)
            n = count(i->(i== 0), data)
            p = n/dim/dim/dim
            vx1 = [(elem - p*p)/p/(1-p) for elem in v[DirX()]]
            vy1 = [(elem - p*p)/p/(1-p) for elem in v[DirY()]]
            vz1 = [(elem - p*p)/p/(1-p) for elem in v[DirZ()]]
            res = [vx1, vy1, vz1]
        else
            res = [v[DirX()], v[DirY()], v[DirZ()]]
        end
    elseif (method == "l2")
        v = l2(data, 0)
        if (normalize == 1)
            res = [v[DirX()]/v[DirX()][1], v[DirY()]/v[DirY()][1], v[DirZ()]/v[DirZ()][1]]
        else
            res = [v[DirX()], v[DirY()], v[DirZ()]]
        end
    elseif (method == "ss")
        v = surf2(data, 0)
        if (normalize == 1)
            res = [v[DirX()]/v[DirX()][1], v[DirY()]/v[DirY()][1], v[DirZ()]/v[DirZ()][1]]
        else
            res = [v[DirX()], v[DirY()], v[DirZ()]]
        end
    else
        throw(DomainError(method, "unknown method"))
    end
    return res
end
