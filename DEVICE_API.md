#Airview2 device API documentation

Airview devices have an undocumented, but fairly simple text based API available 
over the USB CDC-ACM virtual serial port provided by the device.
            
Commands are simple ASCII strings followed by a linefeed byte ('\n').
            
For commands that return a response (some don't), the response format is a byte 
sequence that looks like this (linefeed added for clarity):
            
    stat|ST52342,initializing...done(\n)

In order, the format is:

* A response identifier
* A pipe ('|')
* Command-specific response information (?)
* A comma
* Command response data
* A linefeed byte ('\n').






###Commands

Currently I know just enough about the API commands to reliably use the device 
for its intended purpose. 

Due to the way these were discovered, and the fact that the device never returns 
errors for invalid commands, I have no way of knowing what other commands exist 
until I manage to hit one by getting a response or seeing something change.

As a result, there is also no way to tell the difference between commands that 
don't exist, and commands that exist and do something, but don't return a 
response (there is at least one found so far: `es`).




#####Initialize device 

    Command: 'init'
    
    Response identifier: 'stat'
        
    Command specific response info: 'ST52342'
        
    Response data: 'initializing...done'

------------------------------------------------------------

It seems the device and all the other commands work just fine whether this is
called or not, so it may just be running firmware routines that automatically 
run when the device is powered on. Those same routines might be provided as an 
external command to allow software to manually re-initialize the device in certain 
circumstances, perhaps after a long period of continuous use.
            
The response identifier is 'stat', so it would be reasonable to assume that 
means "status", and that the response data provided is the device status. There 
isn't any obvious meaning to the response numbers, but they seem to be constant 
over time even after unplugging the device.

It may run internal maintenance tasks, things like:

* Checking the firmware integrity
* Testing the radio
* Calibrating the device to account for ambient temperature

As a side effect of reinitializing the device, the `init` command is also capable 
of stopping an RSSI scan initiated with the `bs` command.


        
        
#####Get device info

    Command: 'gdi'

    Response identifier: 'devi'

    Command-specific response info: 'AirView USB' (might vary depending on HW model)

    Response data: probably varies too, but here's an example:

        0000-0241,1.0,1.0,2009/1/23 15:12:43 EST,1,2399.0 2485.0 0.5 173 -134
    
------------------------------------------------------------
        
This command returns basic information about the device. 
        
Some easily identifiable response data includes: 
        
* The USB device ID (0241 here)
* Two separate version numbers, perhaps hardware + firmware
* A very specific date, again either hardware or firmware related (compile date?)
* Two obvious RF frequencies that designate a range starting around 2.4GHz

The last segment is all numbers, and it appears to contain things like:

* Channel spacing (0.5MHz)
* The number of distinct frequencies it hops when scanning the RF range (173)

So putting that together, on my own device it appears to start at 2399.0MHz, 
hop 0.5Mhz at a time up to 2485.0MHz, and provide exactly 173 RSSI values. This
will very likely be different on the 5GHz model, so if anyone can test one and
provide the command response to me I'll make a table with models and values here.

The very last number in the response is negative and I don't know what it means 
at the moment.

*Side note: Finding this API was quite helpful in determining how to use the RSSI info.*





#####Begin RF scan

    Command: 'bs'

    Response identifier: 'scan'

    Response data: sequence of RSSI values separated by spaces

------------------------------------------------------------
            
This starts a full-spectrum RSSI scan inside the device, and continuously streams 
groups of results back over the serial connection until the device is told to
stop. 

To stop the scan, send the 'es' or "end scan" command. Sending the 'init' command 
also stops it, though it may have other unknown side effects.

To use the RSSI list returned by this command, call `gdi` first and use the data
it returns to generate a list of corresponding frequencies.

*Side note: Originally I assumed 'bs' meant "background scan", but then I realized 
there isn't any reason to assume the letter "b" means background, rather it is 
more likely 'bs' simply means "begin scan", which makes more sense as an imperative
command. I confirmed that by starting a scan and testing to see if there was a 
corresponding 'es' or "end scan" command, and the scan immediately stopped.*





#####End RF scan

    Command: 'es'

    Response identifier: None

    Response data: None

------------------------------------------------------------
            
This command ends an RF RSSI scan that was previously started with the `bs` command.

There is no response whatsoever, the scan just stops.

*Side note: This is the first discovered command that silently succeeds, providing 
proof that not all commands return a response, and that finding others may require
detecting changes rather than just reading responses.*

