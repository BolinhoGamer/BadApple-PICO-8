function render_frame(frame)
    local idx = 1
    local pos = 0
    
    repeat
        local size = frame[idx]+1
        local tile = frame[idx+1]
        
        idx += 2
        
        for i=1,size do
            local x = pos%16
            local y = flr(pos/16)
            
            spr(tile,x*8,y*8+16)
            
            pos += 1
        end
    until idx > #frame
end
