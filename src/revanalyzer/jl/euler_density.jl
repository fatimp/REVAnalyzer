using EulerCharacteristic
function euler_density(str_args)
    filename = str_args[1]
    dim = parse(Int64, str_args[2])
    data = Array{UInt8, 3}(undef, dim, dim, dim)
    open(filename) do io read!(io, data) end
    data = Bool.(data)
    data = .!data
    volume = dim*dim*dim
    return euler_characteristic(data)/volume
end