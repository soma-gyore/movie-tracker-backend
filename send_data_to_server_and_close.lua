def_hotkey=113 -- q key
-- Extension description
function descriptor()
    return { 
	title = "Send data to the server and quit";
        version = "1.0" ;
        author = "Soma Gyore" ;
        url = 'http://';
        shortdesc = "Send data to the server and quit";
        description = "Send data to the server and quit" ;
        capabilities = { }
	}
end

function read_config()
--
end

function read_file(path)
    local file = open(path, "rb") -- r read mode and b binary mode
    if not file then return nil end
    local content = file:read "*a" -- *a or *all reads the whole file
    file:close()
    return content
end

-- Activation hook
function activate()
	local input = vlc.object.input()
	local last_position = vlc.var.get(input, "time")
	
	-- get duration in seconds
	local duration = vlc.input.item():duration()
	
	local item = vlc.input.item()

	local title = item:name()
	-- local file_name_len = string.len("send_data_to_server_and_close.lua")
	
	local pwd = string.sub(debug.getinfo(1).source, 2, -34)
	
	local file = io.open(pwd .. "config.txt", "r")
	io.input(file)
	local server_url = io.read()
	local api_key = io.read()
	io.close(file)

	vlc.msg.info("curl --max-time 3 -H \"Content-Type: application/json\" -H \"x-api-key: " .. api_key .. "\" -X POST -d \"{\"closeTimeStamp\": " .. os.time() .. ", \"title\": \"" .. title .. "\", \"lastPosition\": " .. math.floor(last_position) .. ", \"duration\": " .. math.floor(duration) .. "}\" " .. server_url)
	os.execute("curl --max-time 3 -H \"Content-Type: application/json\" -H \"x-api-key: " .. api_key .. "\" -X POST -d \"{\\\"closeTimeStamp\\\": " .. os.time() .. ", \\\"title\\\": \\\"" .. title .. "\\\", \\\"lastPosition\\\": " .. math.floor(last_position) .. ", \\\"duration\\\": " .. math.floor(duration) .. "}\" " .. server_url)

	os.exit(0)
end

function send_request()

end

-- Deactivation hook
function deactivate()
    --
end

