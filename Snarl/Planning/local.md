------------------------------------------------------------------------------------------------------------------------
              send
    Server <-------------------------------> Client
    |                             receive      |
    |                                          |
    |                              receive     |
    Adversary Data --------------------------->|
    |                                          |
    |                                          |
    |                       send               |
    Player Location <----------------------- Player       
    Player Data (Health, etc.)                 |
    |                                          |
    |                                          |
    |                                          |
    Envoronment Data   send                    |
    (Player loc/data, <--------------------> Environment
    game object loc/data,           receive
    adversaries loc/data)                             
                                        
