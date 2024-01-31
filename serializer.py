#fork of https://github.com/sininen-taivas/ergo-numerals
#minor fix for incorrect serialization of some numerals
#added deserialization

def serialize(value: int,prefix):
    # ZigZag
    z = (value << 1) ^ (value >> 32)

    # serialize
    v = []
    while z >= 0x80:
        v.append((z & 0x7F) | 0x80)
        z >>= 7
    v.append(z)

    # Convert integer list to hex string
    encoded_string = ''.join([format(byte, '02x') for byte in v])

    # Add prefix
    encoded_string = prefix + encoded_string

    return encoded_string

def deserialize(encoded_string: str):
    # Remove prefix
    encoded_string = encoded_string[2:]

    # Convert hex string to integer list
    v = [int(encoded_string[i:i + 2], 16) for i in range(0, len(encoded_string), 2)]

    # Decode
    z = 0
    shift = 0
    for byte in v:
        z |= (byte & 0x7F) << shift
        shift += 7
        if not byte & 0x80:
            break

    # Correct ZigZag
    n = (z >> 1) ^ (-(z & 1) if z & 1 else 0)

    return n

prefix = "04" #typically refers to which register, but not strictly needed.

#test script
to_serialize=2999189698 # numeral value to serialize
to_deserialize = "048483a0ac16"

serialized = serialize(to_serialize,prefix)
deserialized = deserialize(to_deserialize)

print("Serialize:",to_serialize,"-->", serialized)
print("Deserialize",to_deserialize, "-->",deserialized)
