using EulerCharacteristic
filename = ARGS[1]
dim = parse(Int64, ARGS[2])
fpath = ARGS[3]
data = Array{UInt8, 3}(undef, dim, dim, dim)
open(filename) do io read!(io, data) end
data = Bool.(data)
data = .!data
volume = dim*dim*dim
density = euler_characteristic(data)/volume
open(fpath, "w") do file
    write(file, string(density))
end
