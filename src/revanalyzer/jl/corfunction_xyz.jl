using CorrelationFunctions.Directional
using CorrelationFunctions.Utilities
using StatsBase
function compute_cf(addr, dim, normalize, method)
    volume = dim*dim*dim
    data = unsafe_wrap(Array{UInt8}, Ptr{UInt8}(addr), volume)
    data = reshape(data, (dim, dim, dim))
    if (method == "c2")
        n = count(i->(i== 0), data)
        if (n == 0)
            res = [[NaN], [NaN], [NaN]]
            return res
        end
        v = c2(data, 0)
        if (normalize == 1)            
            p = n/volume
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
            p = n/volume
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
    elseif (method == "sv")
        v = surfvoid(data, 0)
        if (normalize == 1)
            res = [v[DirX()]/v[DirX()][1], v[DirY()]/v[DirY()][1], v[DirZ()]/v[DirZ()][1]]
        else
            res = [v[DirX()], v[DirY()], v[DirZ()]]
        end
    elseif (method == "cl")
        res = chord_length(data, 0)
    elseif (method == "ps")
        res = pore_size(data, 0)
    elseif (method == "cc")
        v = cross_correlation(data, 0, 1)
        if (normalize == 1)
            n = count(i->(i== 0), data)
            p = n/volume
            vx1 = [elem/p/(1-p) for elem in v[DirX()]]
            vy1 = [elem/p/(1-p) for elem in v[DirY()]]
            vz1 = [elem/p/(1-p) for elem in v[DirZ()]]
            res = [vx1, vy1, vz1]
        else
            res = [v[DirX()], v[DirY()], v[DirZ()]]
        end
    else
        throw(DomainError(method, "unknown method"))
    end
    return res
end
