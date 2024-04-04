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
    elseif (method == "sv")
        v = surfvoid(data, 0)
        if (normalize == 1)
            res = [v[DirX()]/v[DirX()][1], v[DirY()]/v[DirY()][1], v[DirZ()]/v[DirZ()][1]]
        else
            res = [v[DirX()], v[DirY()], v[DirZ()]]
        end
    elseif (method == "sss")
        v = surf3(data, 0, planes = AbstractPlane[PlaneXY(), PlaneXZ(), PlaneYZ()])
        if (normalize == 1)
            res = [v[PlaneXY()]/v[PlaneXY()][1], v[PlaneXZ()]/v[PlaneXZ()][1], v[PlaneYZ()]/v[PlaneYZ()][1]]
        else
            res = [v[PlaneXY()], v[PlaneXZ()], v[PlaneYZ()]]
        end
    elseif (method == "ssv")
        v = surf2void(data, 0)
        if (normalize == 1)
            res = [v[DirX()]/v[DirX()][1], v[DirY()]/v[DirY()][1], v[DirZ()]/v[DirZ()][1]]
        else
            res = [v[DirX()], v[DirY()], v[DirZ()]]
        end
    elseif (method == "svv")
        v = surfvoid2(data, 0)
        if (normalize == 1)
            res = [v[DirX()]/v[DirX()][1], v[DirY()]/v[DirY()][1], v[DirZ()]/v[DirZ()][1]]
        else
            res = [v[DirX()], v[DirY()], v[DirZ()]]
        end
    elseif (method == "cl")
        v = chord_length(data, 0, directions = AbstractDirection[DirX(), DirY(), DirZ()])
        res0 = v.hist
        res = res0.weights
        #if (normalize == 1)
        #    res = [v[DirX()]/dim, v[DirY()]/dim, v[DirZ()]/dim]
        #else
        #    res = [v[DirX()], v[DirY()], v[DirZ()]]
        #end 
    elseif (method == "ps")
        v = chord_length(data, 0)
        res0 = v.hist
        res = res0.weights
        #if (normalize == 1)
        #    res = [v[DirX()]/dim, v[DirY()]/dim, v[DirZ()]/dim]
        #else
        #    res = [v[DirX()], v[DirY()], v[DirZ()]]
        #end
    elseif (method == "cc")
        v = cross_correlation(data, 0, 1)
        res = v
        if (normalize == 1)
            n = count(i->(i== 0), data)
            p = n/dim/dim/dim
            res = [v[DirX()]/p/(1-p), v[DirY()]/p/(1-p), v[DirZ()]/p/(1-p)]
        else
            res = [v[DirX()], v[DirY()], v[DirZ()]]
        end
    elseif (method == "c3")
        v = c3(data, 0)
        #if (normalize == 1)
        #    n = count(i->(i== 0), data)
        #   p = n/dim/dim/dim
        #    res = [v[DirX()]/p/p/p, v[DirY()]/p/p/p, v[DirZ()]/p/p/p]
        #else
        #    res = [v[DirX()], v[DirY()], v[DirZ()]]
        #end
    elseif (method == "s3")
        v = s3(data, 0)
        #if (normalize == 1)
        #    n = count(i->(i== 0), data)
        #    p = n/dim/dim/dim
        #    res = [v[DirX()]/p/p/p, v[DirY()]/p/p/p, v[DirZ()]/p/p/p]
        #else
        #    res = [v[DirX()], v[DirY()], v[DirZ()]]
        #end
    else
        throw(DomainError(method, "unknown method"))
    end
    return res
end
