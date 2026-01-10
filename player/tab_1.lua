b64_table = '"!@#$%&*()_=[]^~,.<>;:?|{}abcdefghijklmnopqrstuvwxyz0123456789+/'


-- base64 decoder
function decode_frame()
    local frame = frame_data[frame_idx]
    local buffer = ''
    
    if #frame == 0 then
        dont_update = 1
        return
    end
    
    decoded = {}

    for i = 1, #frame do
        char = frame[i]
        
        if char == ' ' then
            for i = 2, #frame do
                dont_update += 1
            end
            dont_update += 1
            return
        end
        
        if char ~= '-' then
            local n = getstr_idx(char)-1
            
            buffer ..= bin(n)
            
            if #buffer >= 8 then
                decoded[#decoded+1] = frombin(sub(buffer,1,8))
                buffer = sub(buffer, 9)
            end
        
        else
            if #buffer > 0 then
                buffer = sub(buffer, 9)
            end
            
        end
    end
    
    return decoded
end


function getstr_idx(char)
    for i = 1, 64 do
        if b64_table[i] == char then
            return i
        end
    end
end


function bin(num)
    local out = ''
    
    for i = 1, 6 do
        out = (num & 1) .. out
        num >>= 1
        num = flr(num)
    end
    
    return out
end


function frombin(num)
    local out = 0
    
    for i=1,#num do
        out <<= 1
        if num[i] == '1' then
            out += 1
        end
    end
    
    return out
end
