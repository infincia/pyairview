#Airview2 device API documentation

Airview devices have an undocumented, but fairly simple text based API available 
over the USB CDC-ACM virtual serial port provided by the device.
            
Commands are simple ASCII strings followed by carriage return + linefeed ('\r\n').
            
Responses come back as a byte sequence in a well defined format. 

In order:

* A response identifier
* A pipe ('|')
* Command-specific response information (?)
* A comma
* Command response data
* A linefeed byte ('\n').

A simple example is the response to 'init' (linefeed added for clarity):
            
    stat|ST52342,initializing...done(\n)




###Commands

Currently I know just enough about the API commands to reliably use the device 
for its intended purpose. 

Due to the way these were discovered, and the fact that the device never returns 
errors for invalid commands, I have no way of knowing what other commands exist 
until I manage to hit one by getting a response.

As a result, there is also no way to tell the difference between commands that 
don't exist, and commands that might not return a response. Since there are no 
errors, I might have hit a few correct commands that simply didn't return any 
response without knowing it.

I'm definitely interested in any commands that represent undocumented features
or alternate device modes, some of those might not return a response if they do
exist.




#####Initialize device 

    Command: 'init'
    
    Response identifier: 'stat'
        
    Command specific response info: 'ST52342'
        
    Response data: 'initializing...done'

------------------------------------------------------------
            
This must(?) be called before issuing other commands, and also between commands to 
stop the previously issued command, particularly background scan which will run
forever until initialize is called again.
                    
I don't currently know what the numbers mean, they seem to be constant over time 
even after unplugging the device, and possibly also constant on all devices of 
the same model. But they could also indicate firmware status, device state, who
knows at this point.
                    


        
        
#####Get device info

    Command: 'gdi'

    Response identifier: 'devi'

    Command-specific response info: 'AirView USB' (might vary depending on HW model)

    Response data: probably varies too, but here's an example:

        0000-0241,1.0,1.0,2009/1/23 15:12:43 EST,1,2399.0 2485.0 0.5 173 -134
    
------------------------------------------------------------
        
This command returns basic information about the device. Finding this API assisted 
greatly in determining how to parse the radio RSSI data stream.

If you need to know how to interpret the background scan RSSI list, call this
command first to determine the frequencies.
        
Some easily identifiable response data includes: 
        
* The USB device ID (0241 here)
* Two separate version numbers, perhaps hardware + firmware
* A very specific date, again either hardware or firmware related (compile date?)
* Two obvious RF frequencies that make a range starting around 2.4GHz

As we know this specific model is a 2.4GHz device, it's a safe bet that it's 
providing the exact RF range it can receive on.

The last segment is all numbers, and it appears to contain things like:

* Channel spacing (0.5MHz)
* The number of distinct frequencies it checks when scanning the RF range (173)

So putting that together, on my own device it appears to start at 2399.0MHz, 
hop 0.5Mhz at a time up to 2485.0MHz, and provide exactly 173 RSSI values. This
will very likely be different on the 5GHz model, if anyone can test one and
provide the command response to me I'll make a table with models and values here.

The very last number in the response is negative and I don't know what it means 
at the moment.





#####Start streaming RSSI scan

    Command: 'bs'

    Response identifier: 'scan'

    Response data: sequence of RSSI values separated by spaces

------------------------------------------------------------
            
This starts a constant RSSI scan inside the device, and then returns RSSI levels 
as a continuous stream, one group at a time.

This command does not require multiple calls, it continues until the device is
unplugged or the 'init' command is sent again, which will stop it.