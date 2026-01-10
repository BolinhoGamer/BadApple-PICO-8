frame_idx = 0
skip = 0
dont_update = 0


function _update60()
    if skip == 0 then
        skip = 16
        frame_idx += 1
        if dont_update > 0 then
            dont_update -= 1
        end
    end
    skip -= 1
end


function _draw()
    if frame_idx <= #frame_data then
        if dont_update == 0 then
            local frame = decode_frame()
            if dont_update == 0 then
                cls()
                render_frame(frame)
            end
        end
    end
    
    print(flr(frame_idx/#frame_data*100)..'%',0,120,0)
    print(flr(frame_idx/#frame_data*100)..'%',0,120,6)
end
