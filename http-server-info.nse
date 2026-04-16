-- ============================================================
-- http-server-info.nse
-- CampusPe Cybersecurity Assignment - Section 5.2
--
-- Runs on HTTP ports (80, 8080)
-- Makes HTTP GET request to root page (/)
-- Extracts and displays:
--   • HTTP status code
--   • Server header
--   • Page title
--
-- Test:
--   nmap --script=./http-server-info.nse scanme.nmap.org
--   nmap --script=./http-server-info.nse -p 80,8080 <target>
-- ============================================================

description = [[
Connects to a web server on HTTP ports (80, 8080), sends a
GET / request, and reports the HTTP status code, Server header,
and HTML page title.
]]

author     = "CampusPe Cybersecurity Student"
license    = "Same as Nmap -- See https://nmap.org/book/man-legal.html"
categories = { "default", "discovery", "safe" }

-- ── Libraries ─────────────────────────────────────────────────
local http      = require "http"
local shortport = require "shortport"
local stdnse    = require "stdnse"

-- ── Port Rule ─────────────────────────────────────────────────
-- Script runs only on ports 80 and 8080
portrule = shortport.port_or_service(
    { 80, 8080 },
    { "http", "http-alt" },
    "tcp"
)

-- ── Helper: Extract <title> from HTML ─────────────────────────
local function get_title(body)
    if not body then return "N/A" end
    local t = body:match("<[Tt][Ii][Tt][Ll][Ee]>%s*(.-)%s*</[Tt][Ii][Tt][Ll][Ee]>")
    if t and #t > 0 then
        -- remove newlines/tabs from title
        t = t:gsub("[\r\n\t]", " ")
        t = t:gsub("%s+", " ")
        return t
    end
    return "No title found"
end

-- ── Helper: Get response header safely ────────────────────────
local function get_header(response, name)
    if response and response.header then
        local v = response.header[name:lower()]
        if v and #v > 0 then return v end
end
    return "Not present"
end

-- ── Action ────────────────────────────────────────────────────
action = function(host, port)

    -- Send HTTP GET request to /
    local response = http.get(host, port, "/")

    -- Handle failure
    if not response then
        return "ERROR: Could not connect to the server."
    end

    if not response.status then
        return "ERROR: No response received from server."
    end

    -- Extract all required fields
    local status_code = tostring(response.status)
    local server      = get_header(response, "Server")
    local title       = get_title(response.body)

    -- Format and return output
    return "\n" ..
           "  HTTP Status Code : " .. status_code .. "\n" ..
           "  Server           : " .. server      .. "\n" ..
           "  Page Title       : " .. title
end

