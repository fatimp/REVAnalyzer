using EulerCharacteristic
function euler_density(addr, length)
    volume = length*length*length
    data = unsafe_wrap(Array{UInt8}, Ptr{UInt8}(addr), volume)
    data = Bool.(data)
    data = reshape(data, (length, length, length))
    data = .!data
    res = euler_characteristic(data)
    return res/volume
end
