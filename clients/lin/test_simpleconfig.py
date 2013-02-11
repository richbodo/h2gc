import SimpleConfig

conf = SimpleConfig('myapp')   # Load configuration file if it exists                                                              
conf['foo'] = '3'              # Set a value                                                                                       
conf.save()                    # Save the configuration file on disk                                                               
conf.delete()                  # Delete file, it was just an example                                                               
                                                                                    
