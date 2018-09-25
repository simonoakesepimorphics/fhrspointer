#FHRS Pointy Thing

###Run parameters

Parameter   | Type       | Meaning | Default
------------|------------|---------|--------
--test      | Non-valued | Run the application in test mode, so that commands are logged in the console instead of being sent over the network.||
--lat_home  | float      | Set the latitude of the "home" point where the pointer is located. | 51.480332 |
--lat_home  | float      | Set the longitude of the "home" point where the pointer is located. | -2.768165 |
--idle      | Non-valued | Run the application's idle routine when it hasn't received a request in a while ||
--idle_delay| float      | Set the number of seconds to wait for a request before going into the idle routine.|30|

